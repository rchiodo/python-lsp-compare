from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from python_lsp_compare.cli import main
from python_lsp_compare.server_configs import load_server_config_file, load_server_configs


class ServerConfigTests(unittest.TestCase):
    def test_load_server_configs_resolves_relative_args(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir) / "configs"
            config_dir.mkdir(parents=True, exist_ok=True)
            launcher = Path(temp_dir) / "launcher.js"
            launcher.write_text("", encoding="utf-8")
            config_path = config_dir / "servers.json"
            config_path.write_text(
                json.dumps(
                    {
                        "servers": [
                            {
                                "id": "demo",
                                "displayName": "Demo",
                                "launch": {
                                    "command": sys.executable,
                                    "args": ["../launcher.js"],
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            servers = load_server_configs(config_path)
            self.assertEqual(len(servers), 1)
            self.assertEqual(servers[0].args[0], str(launcher.resolve()))

    def test_load_server_config_file_reads_baseline_server(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "servers.json"
            config_path.write_text(
                json.dumps(
                    {
                        "baselineServer": "demo",
                        "servers": [
                            {
                                "id": "demo",
                                "launch": {
                                    "command": sys.executable,
                                    "args": [],
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            config = load_server_config_file(config_path)
            self.assertEqual(config.baseline_server, "demo")
            self.assertEqual(len(config.servers), 1)

    def test_run_servers_uses_local_config(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "servers.json"
            output_dir = Path(temp_dir) / "results"
            config_path.write_text(
                json.dumps(
                    {
                        "servers": [
                            {
                                "id": "fake-one",
                                "displayName": "Fake One",
                                "launch": {
                                    "command": sys.executable,
                                    "args": [str(server_script)],
                                },
                            },
                            {
                                "id": "fake-two",
                                "displayName": "Fake Two",
                                "launch": {
                                    "command": sys.executable,
                                    "args": [str(server_script)],
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            exit_code = main(
                [
                    "run-servers",
                    "--config",
                    str(config_path),
                    "--scenario",
                    "hover",
                    "--output-dir",
                    str(output_dir),
                ]
            )
            self.assertEqual(exit_code, 0)
            summary_files = list(output_dir.glob("summary-*.json"))
            self.assertEqual(len(summary_files), 1)
            summary = json.loads(summary_files[0].read_text(encoding="utf-8"))
            self.assertEqual([item["id"] for item in summary["servers"]], ["fake-one", "fake-two"])
            self.assertTrue(all(item["success"] for item in summary["servers"]))
            report_files = list(output_dir.glob("fake-*.json"))
            self.assertEqual(len(report_files), 2)

    def test_run_servers_defaults_to_all_scenarios_when_cli_omits_scenarios(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "servers.json"
            output_dir = Path(temp_dir) / "results"
            config_path.write_text(
                json.dumps(
                    {
                        "servers": [
                            {
                                "id": "preset-server",
                                "displayName": "Preset Server",
                                "launch": {
                                    "command": sys.executable,
                                    "args": [str(server_script)],
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            exit_code = main([
                "run-servers",
                "--config",
                str(config_path),
                "--output-dir",
                str(output_dir),
            ])
            self.assertEqual(exit_code, 0)
            summary = json.loads(next(output_dir.glob("summary-*.json")).read_text(encoding="utf-8"))
            self.assertEqual(summary["servers"][0]["requested_scenarios"], ["hover", "completion", "document_symbols"])

    def test_bench_servers_defaults_to_all_benchmarks_and_shared_suite_env(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "servers.json"
            output_dir = Path(temp_dir) / "results"
            benchmark_root = Path(__file__).parent / "fixtures"
            env_capture = Path(temp_dir) / "env.json"
            config_path.write_text(
                json.dumps(
                    {
                        "servers": [
                            {
                                "id": "bench-server",
                                "displayName": "Bench Server",
                                "launch": {
                                    "command": sys.executable,
                                    "args": [str(server_script), "--write-env", str(env_capture)],
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            exit_code = main([
                "bench-servers",
                "--config",
                str(config_path),
                "--benchmark-root",
                str(benchmark_root),
                "--output-dir",
                str(output_dir),
            ])
            self.assertEqual(exit_code, 0)
            summary = json.loads(next(output_dir.glob("summary-*.json")).read_text(encoding="utf-8"))
            self.assertEqual(summary["servers"][0]["requested_benchmarks"], ["fixture_suite"])
            self.assertTrue(summary["servers"][0]["success"])
            env_data = json.loads(env_capture.read_text(encoding="utf-8"))
            self.assertTrue(env_data["virtual_env"].endswith("benchmark_suite\\.venv"))
            report_files = list(output_dir.glob("bench-server-*.json"))
            self.assertEqual(len(report_files), 1)

    def test_bench_servers_uses_configured_baseline_when_cli_omits_it(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "servers.json"
            output_dir = Path(temp_dir) / "results"
            benchmark_root = Path(__file__).parent / "fixtures"
            config_path.write_text(
                json.dumps(
                    {
                        "baselineServer": "baseline-server",
                        "servers": [
                            {
                                "id": "baseline-server",
                                "displayName": "Baseline Server",
                                "launch": {
                                    "command": sys.executable,
                                    "args": [str(server_script)],
                                },
                            },
                            {
                                "id": "other-server",
                                "displayName": "Other Server",
                                "launch": {
                                    "command": sys.executable,
                                    "args": [str(server_script)],
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            exit_code = main([
                "bench-servers",
                "--config",
                str(config_path),
                "--benchmark-root",
                str(benchmark_root),
                "--output-dir",
                str(output_dir),
            ])
            self.assertEqual(exit_code, 0)
            summary = json.loads(next(output_dir.glob("summary-*.json")).read_text(encoding="utf-8"))
            self.assertEqual(summary["baseline_server"], "baseline-server")


if __name__ == "__main__":
    unittest.main()