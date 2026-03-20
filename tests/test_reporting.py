from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from python_lsp_compare.cli import main


class ReportingTests(unittest.TestCase):
    def test_bench_servers_writes_markdown_comparison_with_result_differences(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        benchmark_root = Path(__file__).parent / "fixtures"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_path = temp_path / "servers.json"
            output_dir = temp_path / "results"
            markdown_path = temp_path / "comparison.md"
            csv_path = temp_path / "comparison.csv"
            latest_results_path = temp_path / "latest-results.md"
            config_path.write_text(
                json.dumps(
                    {
                        "servers": [
                            {
                                "id": "small-results",
                                "displayName": "Small Results",
                                "launch": {
                                    "command": sys.executable,
                                    "args": [
                                        str(server_script),
                                        "--completion-items",
                                        "1",
                                        "--hover-text",
                                        "short",
                                    ],
                                },
                            },
                            {
                                "id": "large-results",
                                "displayName": "Large Results",
                                "launch": {
                                    "command": sys.executable,
                                    "args": [
                                        str(server_script),
                                        "--completion-items",
                                        "3",
                                        "--hover-text",
                                        "this is a much longer hover payload",
                                    ],
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            exit_code = main(
                [
                    "bench-servers",
                    "--config",
                    str(config_path),
                    "--benchmark-root",
                    str(benchmark_root),
                    "--output-dir",
                    str(output_dir),
                    "--markdown-output",
                    str(markdown_path),
                    "--csv-output",
                    str(csv_path),
                    "--baseline-server",
                    "large-results",
                ]
            )

            self.assertEqual(exit_code, 0)
            markdown = markdown_path.read_text(encoding="utf-8")
            self.assertIn("# Python LSP Benchmark Comparison", markdown)
            self.assertIn("Small Results", markdown)
            self.assertIn("Large Results", markdown)
            self.assertIn("Baseline server: Large Results (large-results)", markdown)
            self.assertIn("## Server Versions", markdown)
            self.assertIn("Completions found", markdown)
            self.assertIn("Avg measured ms", markdown)
            self.assertIn("Result Differences", markdown)
            self.assertIn("completion fixture: result differences detected", markdown)
            self.assertIn("Delta vs Large Results", markdown)
            self.assertNotIn("Avg result chars", markdown)

            csv_text = csv_path.read_text(encoding="utf-8")
            self.assertIn("baseline_server_id", csv_text)
            self.assertIn("large-results", csv_text)
            self.assertIn("completion_item_count", csv_text)
            self.assertNotIn("avg_result_chars", csv_text)
            self.assertTrue(latest_results_path.exists())
            latest_results = latest_results_path.read_text(encoding="utf-8")
            self.assertIn("# Python LSP Benchmark Comparison", latest_results)

            summary = json.loads(next(output_dir.glob("summary-*.json")).read_text(encoding="utf-8"))
            self.assertEqual(summary["baseline_server"], "large-results")
            self.assertIn("version", summary["servers"][0])
            report_path = output_dir / Path(summary["servers"][0]["output_path"]).name
            report = json.loads(report_path.read_text(encoding="utf-8"))
            completion_point = next(
                point
                for point in report["benchmark_reports"][0]["points"]
                if point["method"] == "textDocument/completion"
            )
            result_metrics = completion_point["summary"]["result_summary"]["metrics"]
            self.assertEqual(result_metrics["completion_item_count"]["mean"], 1.0)
            self.assertEqual(completion_point["summary"]["result_summary"]["non_empty_count"], 2)

    def test_render_report_rebuilds_markdown_from_summary_json(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        benchmark_root = Path(__file__).parent / "fixtures"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_path = temp_path / "servers.json"
            output_dir = temp_path / "results"
            summary_path = temp_path / "summary.json"
            markdown_path = temp_path / "rerendered.md"
            csv_path = temp_path / "rerendered.csv"
            latest_results_path = temp_path / "latest-results.md"
            config_path.write_text(
                json.dumps(
                    {
                        "servers": [
                            {
                                "id": "demo",
                                "displayName": "Demo",
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

            exit_code = main(
                [
                    "bench-servers",
                    "--config",
                    str(config_path),
                    "--benchmark-root",
                    str(benchmark_root),
                    "--output-dir",
                    str(output_dir),
                    "--summary-output",
                    str(summary_path),
                ]
            )
            self.assertEqual(exit_code, 0)

            render_exit = main(
                [
                    "render-report",
                    "--summary",
                    str(summary_path),
                    "--output",
                    str(markdown_path),
                    "--csv-output",
                    str(csv_path),
                    "--title",
                    "Custom Comparison",
                ]
            )
            self.assertEqual(render_exit, 0)
            markdown = markdown_path.read_text(encoding="utf-8")
            csv_text = csv_path.read_text(encoding="utf-8")
            self.assertIn("# Custom Comparison", markdown)
            self.assertIn("Demo", markdown)
            self.assertIn("Avg measured ms", markdown)
            self.assertIn("server_id", csv_text)
            self.assertIn("demo", csv_text)
            self.assertTrue(latest_results_path.exists())
            self.assertEqual(latest_results_path.read_text(encoding="utf-8"), markdown)


if __name__ == "__main__":
    unittest.main()
