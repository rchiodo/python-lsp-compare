from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from python_lsp_compare.cli import main


class CliTests(unittest.TestCase):
    def test_list_scenarios(self) -> None:
        exit_code = main(["list-scenarios"])
        self.assertEqual(exit_code, 0)

    def test_run_writes_report(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "report.json"
            exit_code = main(
                [
                    "run",
                    "--server-command",
                    sys.executable,
                    "--server-arg",
                    str(server_script),
                    "--scenario",
                    "hover",
                    "--output",
                    str(output_path),
                ]
            )
            self.assertEqual(exit_code, 0)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(report["requested_scenarios"], ["hover"])
            self.assertEqual(report["scenario_reports"][0]["name"], "hover")
            self.assertTrue(report["scenario_reports"][0]["success"])

    def test_list_benchmarks(self) -> None:
        exit_code = main(["list-benchmarks", "--benchmark-root", str(Path(__file__).parent / "fixtures")])
        self.assertEqual(exit_code, 0)

    def test_list_servers_marks_configured_baseline_inline(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "servers.json"
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

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["list-servers", "--config", str(config_path)])

            self.assertEqual(exit_code, 0)
            output = stdout.getvalue()
            self.assertIn("baseline-server: Baseline Server (enabled, baseline)", output)
            self.assertIn("other-server: Other Server (enabled)", output)


if __name__ == "__main__":
    unittest.main()
