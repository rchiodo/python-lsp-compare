from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from python_lsp_compare.server_download import get_latest_release_tag


class _FakeResponse:
    def __init__(self, payload: object) -> None:
        self._payload = payload

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


class ServerDownloadTests(unittest.TestCase):
    def test_get_latest_release_tag_falls_back_to_latest_release_with_asset(self) -> None:
        seen_urls: list[str] = []

        def fake_urlopen(req):
            url = req.full_url if hasattr(req, "full_url") else req
            seen_urls.append(url)
            if url.endswith("/releases?per_page=10"):
                return _FakeResponse(
                    [
                        {"tag_name": "0.60.0", "assets": []},
                        {
                            "tag_name": "0.59.1",
                            "assets": [{"name": "pyrefly-linux-x86_64.tar.gz"}],
                        },
                    ]
                )
            return _FakeResponse({"tag_name": "0.60.0", "assets": []})

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            tag = get_latest_release_tag("facebook/pyrefly", asset_name="pyrefly-linux-x86_64.tar.gz")

        self.assertEqual(tag, "0.59.1")
        self.assertTrue(any(url.endswith("/releases?per_page=10") for url in seen_urls))


if __name__ == "__main__":
    unittest.main()
