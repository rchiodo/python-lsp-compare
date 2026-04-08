"""Download LSP server binaries from GitHub releases."""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

from .server_configs import ConfiguredServer


GITHUB_API_BASE = "https://api.github.com"

_VERSION_CHECK_INTERVAL_SECONDS = 86400  # 24 hours


def _default_cache_dir() -> Path:
    return Path(__file__).resolve().parents[2] / ".python-lsp-compare" / "servers"


@dataclass(slots=True)
class ServerSpec:
    """Specification for downloading a server from GitHub releases."""

    id: str
    display_name: str
    repo: str  # e.g. "microsoft/pyright"
    kind: str  # "node-wrapper" or "native-exe"
    asset_pattern: dict[str, str]  # {platform_key: asset_name}
    executable_name: str  # Filename to search for after extraction
    launch_args: list[str] = field(default_factory=list)
    benchmark_args: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PypiServerSpec:
    """Specification for a server installed from PyPI packages into an isolated venv."""

    id: str
    display_name: str
    packages: list[str]  # e.g. ["python-lsp-server", "pylsp-mypy"]
    executable_name: str  # Script name installed by the packages, e.g. "pylsp"
    kind: str = "pypi-venv"
    launch_args: list[str] = field(default_factory=list)
    benchmark_args: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _detect_platform() -> str:
    """Return a platform key like 'windows-x86_64' or 'macos-arm64'."""
    import platform as _platform

    if sys.platform == "win32":
        os_key = "windows"
    elif sys.platform == "darwin":
        os_key = "macos"
    else:
        os_key = "linux"

    machine = _platform.machine().lower()
    if machine in ("x86_64", "amd64"):
        arch_key = "x86_64"
    elif machine in ("aarch64", "arm64"):
        arch_key = "arm64"
    else:
        arch_key = "x86_64"

    return f"{os_key}-{arch_key}"


def _exe(name: str) -> str:
    """Append .exe on Windows."""
    return f"{name}.exe" if sys.platform == "win32" else name


# ---------------------------------------------------------------------------
# Server specifications
# ---------------------------------------------------------------------------

PYRIGHT_SPEC = ServerSpec(
    id="pyright",
    display_name="Pyright",
    repo="microsoft/pyright",
    kind="node-wrapper",
    asset_pattern={
        "windows-x86_64": "pyright.tgz",
        "windows-arm64": "pyright.tgz",
        "linux-x86_64": "pyright.tgz",
        "linux-arm64": "pyright.tgz",
        "macos-x86_64": "pyright.tgz",
        "macos-arm64": "pyright.tgz",
    },
    executable_name="pyright-langserver.js",
    launch_args=["--stdio"],
    notes=["Requires Node.js to be installed."],
)

TY_SPEC = ServerSpec(
    id="ty",
    display_name="Ty",
    repo="astral-sh/ty",
    kind="native-exe",
    asset_pattern={
        "windows-x86_64": "ty-x86_64-pc-windows-msvc.zip",
        "windows-arm64": "ty-aarch64-pc-windows-msvc.zip",
        "linux-x86_64": "ty-x86_64-unknown-linux-gnu.tar.gz",
        "linux-arm64": "ty-aarch64-unknown-linux-gnu.tar.gz",
        "macos-x86_64": "ty-x86_64-apple-darwin.tar.gz",
        "macos-arm64": "ty-aarch64-apple-darwin.tar.gz",
    },
    executable_name=_exe("ty"),
    launch_args=["server"],
)

PYREFLY_SPEC = ServerSpec(
    id="pyrefly",
    display_name="Pyrefly",
    repo="facebook/pyrefly",
    kind="native-exe",
    asset_pattern={
        "windows-x86_64": "pyrefly-windows-x86_64.zip",
        "windows-arm64": "pyrefly-windows-arm64.zip",
        "linux-x86_64": "pyrefly-linux-x86_64.tar.gz",
        "linux-arm64": "pyrefly-linux-arm64.tar.gz",
        "macos-x86_64": "pyrefly-macos-x86_64.tar.gz",
        "macos-arm64": "pyrefly-macos-arm64.tar.gz",
    },
    executable_name=_exe("pyrefly"),
    launch_args=["lsp", "--indexing-mode", "lazy-blocking", "--build-system-blocking"],
)

PYLSP_MYPY_SPEC = PypiServerSpec(
    id="pylsp-mypy",
    display_name="pylsp-mypy",
    packages=["python-lsp-server", "pylsp-mypy"],
    executable_name=_exe("pylsp"),
    launch_args=[],
    notes=[
        "Uses python-lsp-server (pylsp) with the pylsp-mypy plugin.",
        "LSP features like hover and completion are provided by pylsp/jedi, not mypy.",
        "mypy contributes diagnostics only.",
    ],
)

ALL_SERVER_SPECS: list[ServerSpec] = [PYRIGHT_SPEC, TY_SPEC, PYREFLY_SPEC]
ALL_PYPI_SERVER_SPECS: list[PypiServerSpec] = [PYLSP_MYPY_SPEC]


# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------

def _github_json(url: str) -> object:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
    with urllib.request.urlopen(req) as resp:  # noqa: S310 – URL is constructed from trusted constants
        return json.loads(resp.read())


def get_latest_release_tag(repo: str, asset_name: str | None = None) -> str:
    """Query the GitHub API for the latest usable release tag of *repo*."""
    latest_url = f"{GITHUB_API_BASE}/repos/{repo}/releases/latest"
    data = _github_json(latest_url)
    if not isinstance(data, dict) or "tag_name" not in data:
        raise RuntimeError(f"Unexpected GitHub release payload for {repo}: {data!r}")

    latest_tag = data["tag_name"]
    if asset_name is None:
        return latest_tag

    latest_assets = data.get("assets") or []
    if any(isinstance(asset, dict) and asset.get("name") == asset_name for asset in latest_assets):
        return latest_tag

    releases_url = f"{GITHUB_API_BASE}/repos/{repo}/releases?per_page=10"
    releases = _github_json(releases_url)
    if isinstance(releases, list):
        for release in releases:
            if not isinstance(release, dict):
                continue
            if release.get("draft") or release.get("prerelease"):
                continue
            assets = release.get("assets") or []
            if any(isinstance(asset, dict) and asset.get("name") == asset_name for asset in assets):
                fallback_tag = release.get("tag_name")
                if isinstance(fallback_tag, str):
                    if fallback_tag != latest_tag:
                        print(
                            f"  Latest release {latest_tag} for {repo} does not contain {asset_name}; "
                            f"falling back to {fallback_tag}"
                        )
                    return fallback_tag

    return latest_tag


def _versions_path(cache_dir: Path) -> Path:
    return cache_dir / "versions.json"


def _load_versions(cache_dir: Path) -> dict:
    path = _versions_path(cache_dir)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _save_versions(cache_dir: Path, data: dict) -> None:
    path = _versions_path(cache_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _resolve_version(
    spec: ServerSpec,
    cache_dir: Path,
    *,
    asset_name: str | None = None,
    force: bool = False,
) -> str:
    """Return the version to use, querying GitHub only if the cache is stale (>24h)."""
    versions = _load_versions(cache_dir)
    entry = versions.get(spec.id)
    now = time.time()

    if not force and entry is not None:
        checked_at = entry.get("checked_at", 0)
        version = entry.get("version")
        has_cached_binary = isinstance(version, str) and _find_executable(
            cache_dir / spec.id / version,
            spec.executable_name,
        ) is not None
        if now - checked_at < _VERSION_CHECK_INTERVAL_SECONDS and has_cached_binary:
            print(f"  {spec.display_name}: using cached version {version} (checked <24h ago)")
            return version
        if now - checked_at < _VERSION_CHECK_INTERVAL_SECONDS and isinstance(version, str):
            print(f"  {spec.display_name}: cached version {version} is incomplete; rechecking releases")

    print(f"Fetching latest release tag for {spec.repo}...")
    version = get_latest_release_tag(spec.repo, asset_name=asset_name)
    print(f"  Latest version: {version}")

    versions[spec.id] = {"version": version, "checked_at": now}
    _save_versions(cache_dir, versions)
    return version


def _download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:  # noqa: S310
        with open(dest, "wb") as f:
            shutil.copyfileobj(resp, f)


def _safe_extract_tar(tf: tarfile.TarFile, dest_dir: Path) -> None:
    dest_resolved = str(dest_dir.resolve())
    for member in tf.getmembers():
        member_path = (dest_dir / member.name).resolve()
        if not str(member_path).startswith(dest_resolved + os.sep) and str(member_path) != dest_resolved:
            raise ValueError(f"Path traversal detected in tar member: {member.name}")
    if sys.version_info >= (3, 12):
        tf.extractall(dest_dir, filter="data")
    else:
        tf.extractall(dest_dir)


def _safe_extract_zip(zf: zipfile.ZipFile, dest_dir: Path) -> None:
    dest_resolved = str(dest_dir.resolve())
    for info in zf.infolist():
        member_path = (dest_dir / info.filename).resolve()
        if not str(member_path).startswith(dest_resolved + os.sep) and str(member_path) != dest_resolved:
            raise ValueError(f"Path traversal detected in zip member: {info.filename}")
    zf.extractall(dest_dir)


def _extract_archive(archive_path: Path, dest_dir: Path) -> None:
    name = archive_path.name.lower()
    if name.endswith(".tar.gz") or name.endswith(".tgz"):
        with tarfile.open(archive_path, "r:gz") as tf:
            _safe_extract_tar(tf, dest_dir)
    elif name.endswith(".zip"):
        with zipfile.ZipFile(archive_path, "r") as zf:
            _safe_extract_zip(zf, dest_dir)
    else:
        raise ValueError(f"Unknown archive format: {archive_path.name}")


def _find_executable(search_dir: Path, name: str) -> Path | None:
    """Recursively search for a file named *name* under *search_dir*."""
    for path in search_dir.rglob(name):
        if path.is_file():
            return path
    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def download_server(
    spec: ServerSpec,
    *,
    version: str | None = None,
    cache_dir: Path | None = None,
    force: bool = False,
) -> tuple[Path, str]:
    """Download a server binary and return the path to the executable and version.

    Skips the download when the binary is already present in *cache_dir*
    unless *force* is set.
    """
    if cache_dir is None:
        cache_dir = _default_cache_dir()

    platform_key = _detect_platform()
    if platform_key not in spec.asset_pattern:
        raise RuntimeError(f"No {spec.display_name} binary available for platform {platform_key}")

    asset_name = spec.asset_pattern[platform_key]

    if version is None:
        version = _resolve_version(spec, cache_dir, asset_name=asset_name, force=force)

    server_dir = cache_dir / spec.id / version

    # Check cache
    cached = _find_executable(server_dir, spec.executable_name)
    if cached is not None and not force:
        print(f"  {spec.display_name} {version} already cached at {cached}")
        return cached, version

    # Download
    download_url = f"https://github.com/{spec.repo}/releases/download/{version}/{asset_name}"
    print(f"  Downloading {asset_name}...")

    with tempfile.TemporaryDirectory() as tmp:
        archive_path = Path(tmp) / asset_name
        _download_file(download_url, archive_path)
        server_dir.mkdir(parents=True, exist_ok=True)
        _extract_archive(archive_path, server_dir)

    # Make executable on Unix
    exe_path = _find_executable(server_dir, spec.executable_name)
    if exe_path is None:
        extracted = sorted(str(p.relative_to(server_dir)) for p in server_dir.rglob("*") if p.is_file())[:20]
        raise RuntimeError(
            f"Expected to find {spec.executable_name} after extracting {asset_name} "
            f"but it was not found.  Extracted files: {extracted}"
        )

    if sys.platform != "win32":
        exe_path.chmod(exe_path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    print(f"  Installed {spec.display_name} {version} -> {exe_path}")
    return exe_path, version


def install_pypi_server(
    spec: PypiServerSpec,
    *,
    cache_dir: Path | None = None,
    force: bool = False,
) -> tuple[Path, str | None]:
    """Install PyPI packages into an isolated venv and return the executable path and version.

    Re-uses an existing venv when the packages are already installed unless
    *force* is set.
    """
    if cache_dir is None:
        cache_dir = _default_cache_dir()

    server_dir = cache_dir / spec.id
    venv_dir = server_dir / "venv"
    scripts_dir = venv_dir / ("Scripts" if sys.platform == "win32" else "bin")
    exe_path = scripts_dir / spec.executable_name

    if exe_path.exists() and not force:
        print(f"  {spec.display_name} already installed at {exe_path}")
        version = _get_pypi_package_version(spec, scripts_dir)
        return exe_path, version

    # Create a fresh venv
    print(f"  Creating venv for {spec.display_name}...")
    if venv_dir.exists():
        shutil.rmtree(venv_dir)
    subprocess.run(
        [sys.executable, "-m", "venv", str(venv_dir)],
        check=True,
        capture_output=True,
    )

    # Install packages
    pip_exe = str(scripts_dir / _exe("pip"))
    print(f"  Installing {', '.join(spec.packages)}...")
    subprocess.run(
        [pip_exe, "install", *spec.packages],
        check=True,
        capture_output=True,
    )

    if not exe_path.exists():
        installed = sorted(str(p.name) for p in scripts_dir.iterdir() if p.is_file())[:30]
        raise RuntimeError(
            f"Expected to find {spec.executable_name} after installing {spec.packages} "
            f"but it was not found.  Scripts dir contents: {installed}"
        )

    print(f"  Installed {spec.display_name} -> {exe_path}")
    version = _get_pypi_package_version(spec, scripts_dir)
    return exe_path, version


def _get_pypi_package_version(spec: PypiServerSpec, scripts_dir: Path) -> str | None:
    """Query the installed version of the first package in the spec's venv."""
    pip_exe = str(scripts_dir / _exe("pip"))
    for pkg in spec.packages:
        try:
            result = subprocess.run(
                [pip_exe, "show", pkg],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
                check=True,
            )
            for line in result.stdout.splitlines():
                if line.startswith("Version:"):
                    return line.split(":", 1)[1].strip()
        except (OSError, subprocess.SubprocessError):
            continue
    return None


def make_configured_server(spec: ServerSpec | PypiServerSpec, executable_path: Path, version_label: str | None = None) -> ConfiguredServer:
    """Build a :class:`ConfiguredServer` from a *spec* and the on-disk *executable_path*."""
    exe_str = str(executable_path)
    if isinstance(spec, ServerSpec) and spec.kind == "node-wrapper":
        command = "node"
        args = [exe_str, *spec.launch_args]
    else:
        command = exe_str
        args = list(spec.launch_args)
    return ConfiguredServer(
        id=spec.id,
        display_name=spec.display_name,
        command=command,
        args=args,
        benchmark_args=list(spec.benchmark_args),
        enabled=True,
        kind=spec.kind,
        notes=list(spec.notes),
        source_path=exe_str,
        version_label=version_label,
    )


def download_all_servers(
    *,
    cache_dir: Path | None = None,
    force: bool = False,
    server_ids: list[str] | None = None,
) -> list[ConfiguredServer]:
    """Download servers and return :class:`ConfiguredServer` objects.

    When *server_ids* is ``None`` all known servers are downloaded.
    """
    all_ids = {s.id for s in ALL_SERVER_SPECS} | {s.id for s in ALL_PYPI_SERVER_SPECS}
    specs = ALL_SERVER_SPECS if server_ids is None else [s for s in ALL_SERVER_SPECS if s.id in server_ids]
    pypi_specs = ALL_PYPI_SERVER_SPECS if server_ids is None else [s for s in ALL_PYPI_SERVER_SPECS if s.id in server_ids]
    servers: list[ConfiguredServer] = []
    for spec in specs:
        try:
            exe_path, version = download_server(spec, cache_dir=cache_dir, force=force)
            servers.append(make_configured_server(spec, exe_path, version_label=version))
        except Exception as exc:
            print(f"  Warning: failed to download {spec.display_name}: {exc}")
    for spec in pypi_specs:
        try:
            exe_path, version = install_pypi_server(spec, cache_dir=cache_dir, force=force)
            servers.append(make_configured_server(spec, exe_path, version_label=version))
        except Exception as exc:
            print(f"  Warning: failed to install {spec.display_name}: {exc}")
    return servers


def write_downloaded_config(servers: list[ConfiguredServer], config_path: Path) -> None:
    """Persist downloaded server info as a JSON config file."""
    config_data = {
        "version": 1,
        "baselineServer": "pyright",
        "servers": [
            {
                "id": s.id,
                "displayName": s.display_name,
                "enabled": s.enabled,
                "kind": s.kind,
                "sourcePath": s.source_path,
                "launch": {
                    "command": s.command,
                    "args": list(s.args),
                    **({"benchmarkArgs": list(s.benchmark_args)} if s.benchmark_args else {}),
                },
                "notes": list(s.notes),
            }
            for s in servers
        ],
    }
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config_data, indent=2) + "\n", encoding="utf-8")
