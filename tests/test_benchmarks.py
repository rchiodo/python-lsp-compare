from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from python_lsp_compare.benchmark_suites import discover_benchmark_suites
from python_lsp_compare.environments import cleanup_benchmark_environment, prepare_benchmark_environment
from python_lsp_compare.cli import main
from python_lsp_compare.runner import run_benchmarks


class BenchmarkSuiteTests(unittest.TestCase):
    def test_discover_bundled_benchmark_suites(self) -> None:
        suites = discover_benchmark_suites()
        self.assertTrue({"sqlalchemy", "web", "data_science", "django", "pandas", "transformers", "tsp_core", "tsp_semantic"}.issubset(suites))

        django_suite = suites["django"]
        self.assertEqual(django_suite.requirements_file.name, "requirements.txt")
        self.assertIn("textDocument/hover", django_suite.points_by_method)
        self.assertIn("textDocument/completion", django_suite.points_by_method)
        self.assertIn("textDocument/definition", django_suite.points_by_method)

        pandas_suite = suites["pandas"]
        self.assertIn("textDocument/definition", pandas_suite.points_by_method)

        transformers_suite = suites["transformers"]
        self.assertIn("textDocument/hover", transformers_suite.points_by_method)
        self.assertIn("textDocument/completion", transformers_suite.points_by_method)

    def test_discover_benchmark_suite(self) -> None:
        suites = discover_benchmark_suites(Path(__file__).parent / "fixtures")
        self.assertIn("fixture_suite", suites)
        suite = suites["fixture_suite"]
        self.assertEqual(suite.iterations, 2)
        self.assertEqual(suite.warmup_iterations, 1)
        self.assertIn("textDocument/hover", suite.points_by_method)
        self.assertIn("textDocument/references", suite.points_by_method)

    def test_discover_tsp_benchmark_suite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            suite_root = temp_path / "tsp_fixture"
            source_dir = suite_root / "src"
            source_dir.mkdir(parents=True, exist_ok=True)
            (source_dir / "flow.py").write_text(
                "value: int | str = 1\nif isinstance(value, int):\n    narrowed = value\n",
                encoding="utf-8",
            )
            (suite_root / "config.json").write_text(
                json.dumps(
                    {
                        "name": "tsp_fixture",
                        "description": "Fixture TSP benchmark suite.",
                        "protocol": "tsp",
                        "workspace_dir": "src",
                        "iterations": 2,
                        "warmup_iterations": 1,
                        "tsp_points": [
                            {
                                "label": "narrowed type",
                                "request": "typeServer/getComputedType",
                                "file": "src/flow.py",
                                "start_line": 2,
                                "start_character": 15,
                                "end_line": 2,
                                "end_character": 20,
                                "validation": {"requireNonEmpty": True, "minSizeChars": 10},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            suites = discover_benchmark_suites(temp_path)
            self.assertIn("tsp_fixture", suites)
            suite = suites["tsp_fixture"]
            self.assertEqual(suite.protocol, "tsp")
            self.assertEqual(len(suite.tsp_points), 1)
            self.assertEqual(suite.tsp_points[0].request, "typeServer/getComputedType")

    def test_run_benchmark_suite(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        report = run_benchmarks(
            command=[sys.executable, str(server_script)],
            benchmark_names=["fixture_suite"],
            benchmark_root=Path(__file__).parent / "fixtures",
            timeout_seconds=2.0,
        )
        self.assertEqual(report.requested_benchmarks, ["fixture_suite"])
        self.assertEqual(len(report.benchmark_reports), 1)
        suite_report = report.benchmark_reports[0]
        self.assertTrue(suite_report.success)
        self.assertEqual(len(suite_report.points), 5)
        self.assertIn("textDocument/hover", suite_report.summary["by_method"])
        hover_point = next(point for point in suite_report.points if point.method == "textDocument/hover")
        self.assertEqual(hover_point.measured_iterations, 2)
        self.assertEqual(hover_point.warmup_iterations, 1)
        self.assertEqual(hover_point.summary["request_count"], 2)
        self.assertEqual(hover_point.summary["result_summary"]["non_empty_count"], 2)
        self.assertEqual(hover_point.summary["result_summary"]["metrics"]["hover_text_char_count"]["mean"], 10.0)

        completion_point = next(point for point in suite_report.points if point.method == "textDocument/completion")
        self.assertEqual(completion_point.summary["result_summary"]["metrics"]["completion_item_count"]["mean"], 1.0)

    def test_run_benchmark_suite_excludes_environment_setup_from_total_duration(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        import python_lsp_compare.runner as runner_module

        original_prepare = runner_module.prepare_benchmark_environment

        def slow_prepare(*args, **kwargs):
            import time

            time.sleep(0.75)
            return original_prepare(*args, **kwargs)

        with patch.object(runner_module, "prepare_benchmark_environment", side_effect=slow_prepare):
            report = run_benchmarks(
                command=[sys.executable, str(server_script)],
                benchmark_names=["fixture_suite"],
                benchmark_root=Path(__file__).parent / "fixtures",
                timeout_seconds=2.0,
            )

        suite_report = report.benchmark_reports[0]
        self.assertTrue(suite_report.success)
        self.assertLess(suite_report.total_duration_ms, 750.0)

    def test_run_tsp_benchmark_suite(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            suite_root = temp_path / "tsp_fixture"
            source_dir = suite_root / "src"
            source_dir.mkdir(parents=True, exist_ok=True)
            (source_dir / "flow.py").write_text(
                "value: int | str = 1\nif isinstance(value, int):\n    narrowed = value\n",
                encoding="utf-8",
            )
            (suite_root / "config.json").write_text(
                json.dumps(
                    {
                        "name": "tsp_fixture",
                        "description": "Fixture TSP benchmark suite.",
                        "protocol": "tsp",
                        "workspace_dir": "src",
                        "iterations": 2,
                        "warmup_iterations": 1,
                        "tsp_points": [
                            {
                                "label": "narrowed type",
                                "request": "typeServer/getComputedType",
                                "file": "src/flow.py",
                                "start_line": 2,
                                "start_character": 15,
                                "end_line": 2,
                                "end_character": 20,
                                "validation": {
                                    "requireNonEmpty": True,
                                    "expectedTypeKinds": ["Class"],
                                    "minSizeChars": 10,
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            report = run_benchmarks(
                command=[sys.executable, str(server_script)],
                benchmark_names=["tsp_fixture"],
                benchmark_root=temp_path,
                timeout_seconds=2.0,
            )

            self.assertEqual(report.requested_benchmarks, ["tsp_fixture"])
            suite_report = report.benchmark_reports[0]
            self.assertTrue(suite_report.success)
            self.assertEqual(len(suite_report.points), 1)
            self.assertEqual(suite_report.points[0].method, "typeServer/getComputedType")
            self.assertEqual(
                suite_report.points[0].summary["result_summary"]["metrics"]["type_name"]["representative"],
                "int",
            )
            self.assertTrue(suite_report.points[0].summary["validation"]["passed"])

    def test_run_tsp_edit_benchmark_suite(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            suite_root = temp_path / "tsp_edit_fixture"
            source_dir = suite_root / "src"
            source_dir.mkdir(parents=True, exist_ok=True)
            (source_dir / "flow.py").write_text(
                "value: int | str = 1\nif isinstance(value, int):\n    narrowed = value\n",
                encoding="utf-8",
            )
            (suite_root / "config.json").write_text(
                json.dumps(
                    {
                        "name": "tsp_edit_fixture",
                        "description": "Fixture TSP edit benchmark suite.",
                        "protocol": "tsp",
                        "workspace_dir": "src",
                        "iterations": 2,
                        "warmup_iterations": 1,
                        "tsp_edit_points": [
                            {
                                "label": "edit then computed type",
                                "request": "typeServer/getComputedType",
                                "file": "src/flow.py",
                                "edit_line": 0,
                                "edit_text": "value = 1",
                                "query_start_line": 2,
                                "query_start_character": 15,
                                "query_end_line": 2,
                                "query_end_character": 20,
                                "validation": {"requireNonEmpty": True, "minSizeChars": 10},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            report = run_benchmarks(
                command=[sys.executable, str(server_script)],
                benchmark_names=["tsp_edit_fixture"],
                benchmark_root=temp_path,
                timeout_seconds=2.0,
            )

            suite_report = report.benchmark_reports[0]
            self.assertTrue(suite_report.success)
            self.assertEqual(len(suite_report.points), 1)
            self.assertEqual(suite_report.points[0].method, "typeServer/getComputedType")
            self.assertIn("edit+getComputedType", suite_report.points[0].label)

    def test_run_tsp_semantic_tokens_benchmark_suite(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            suite_root = temp_path / "tsp_semantic_fixture"
            source_dir = suite_root / "src"
            source_dir.mkdir(parents=True, exist_ok=True)
            (source_dir / "sample.py").write_text(
                "from pathlib import Path\n\n"
                "def load_name(path: Path) -> str:\n"
                "    return path.name\n\n"
                "value = load_name(Path('.'))\n",
                encoding="utf-8",
            )
            (suite_root / "config.json").write_text(
                json.dumps(
                    {
                        "name": "tsp_semantic_fixture",
                        "description": "Fixture TSP semantic tokens benchmark suite.",
                        "protocol": "tsp",
                        "workspace_dir": "src",
                        "iterations": 2,
                        "warmup_iterations": 1,
                        "tsp_points": [
                            {
                                "label": "semantic tokens full file",
                                "request": "typeServer/semanticTokens",
                                "file": "src/sample.py",
                                "start_line": 0,
                                "start_character": 0,
                                "end_line": 5,
                                "end_character": 0,
                                "validation": {"requireNonEmpty": True, "minSizeChars": 10},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            report = run_benchmarks(
                command=[sys.executable, str(server_script)],
                benchmark_names=["tsp_semantic_fixture"],
                benchmark_root=temp_path,
                timeout_seconds=2.0,
            )

            suite_report = report.benchmark_reports[0]
            self.assertTrue(suite_report.success)
            self.assertEqual(len(suite_report.points), 1)
            self.assertEqual(suite_report.points[0].method, "typeServer/semanticTokens")
            metrics = suite_report.points[0].summary["result_summary"]["metrics"]
            self.assertGreater(metrics["semantic_token_count"]["mean"], 0)
            self.assertGreater(metrics["type_query_count"]["mean"], 0)

    def test_tsp_benchmark_validation_fails_on_unexpected_type_name(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            suite_root = temp_path / "tsp_invalid"
            source_dir = suite_root / "src"
            source_dir.mkdir(parents=True, exist_ok=True)
            (source_dir / "flow.py").write_text(
                "value: int | str = 1\nif isinstance(value, int):\n    narrowed = value\n",
                encoding="utf-8",
            )
            (suite_root / "config.json").write_text(
                json.dumps(
                    {
                        "name": "tsp_invalid",
                        "description": "Invalid TSP validation fixture.",
                        "protocol": "tsp",
                        "workspace_dir": "src",
                        "iterations": 2,
                        "warmup_iterations": 1,
                        "tsp_points": [
                            {
                                "label": "wrong type expectation",
                                "request": "typeServer/getComputedType",
                                "file": "src/flow.py",
                                "start_line": 2,
                                "start_character": 15,
                                "end_line": 2,
                                "end_character": 20,
                                "validation": {
                                    "requireNonEmpty": True,
                                    "expectedTypeNames": ["str"],
                                    "requireDeclarationNode": True,
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            report = run_benchmarks(
                command=[sys.executable, str(server_script)],
                benchmark_names=["tsp_invalid"],
                benchmark_root=temp_path,
                timeout_seconds=2.0,
            )

            suite_report = report.benchmark_reports[0]
            self.assertFalse(suite_report.success)
            self.assertIn("type_name", suite_report.points[0].error_message)

    def test_prepare_benchmark_environment_writes_pyrightconfig_for_suite_venv(self) -> None:
        suite = discover_benchmark_suites(Path(__file__).parent / "fixtures")["fixture_suite"]
        environment = prepare_benchmark_environment(
            suite=suite,
            command=[sys.executable],
            environment_mode="isolated",
            base_python_executable=sys.executable,
            install_requirements=True,
        )
        try:
            config_path = suite.root_path / "pyrightconfig.json"
            self.assertTrue(config_path.exists())
            config = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(config["venv"], ".venv")
            self.assertEqual(config["venvPath"], ".")
            self.assertEqual(config["include"], ["src"])
            self.assertEqual(environment.workspace_root, suite.root_path)
            self.assertEqual(environment.workspace_settings["python"]["venv"], ".venv")
            self.assertEqual(environment.workspace_settings["python"]["pythonPath"], environment.python_executable)
        finally:
            cleanup_benchmark_environment(environment)
            self.assertFalse((suite.root_path / "pyrightconfig.json").exists())

    def test_prepare_benchmark_environment_current_mode_sets_python_path(self) -> None:
        suite = discover_benchmark_suites(Path(__file__).parent / "fixtures")["fixture_suite"]
        environment = prepare_benchmark_environment(
            suite=suite,
            command=[sys.executable],
            environment_mode="current",
            base_python_executable=sys.executable,
            install_requirements=False,
        )
        self.assertEqual(environment.workspace_settings["python"]["pythonPath"], sys.executable)
        self.assertEqual(environment.workspace_settings["python"]["defaultInterpreterPath"], sys.executable)

    def test_run_benchmark_suite_handles_workspace_configuration_request(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            config_capture = Path(temp_dir) / "workspace-config.json"
            report = run_benchmarks(
                command=[
                    sys.executable,
                    str(server_script),
                    "--request-workspace-config-output",
                    str(config_capture),
                ],
                benchmark_names=["fixture_suite"],
                benchmark_root=Path(__file__).parent / "fixtures",
                timeout_seconds=2.0,
                environment_mode="isolated",
            )

            suite_report = report.benchmark_reports[0]
            self.assertTrue(suite_report.success)
            response = json.loads(config_capture.read_text(encoding="utf-8"))
            self.assertEqual(response[0]["pythonPath"], suite_report.python_executable)
            self.assertEqual(response[1], suite_report.python_executable)
            self.assertEqual(response[2], suite_report.python_executable)

    def test_run_benchmark_cli_writes_report(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "benchmarks.json"
            exit_code = main(
                [
                    "run-benchmark",
                    "--server-command",
                    sys.executable,
                    "--server-arg",
                    str(server_script),
                    "--benchmark-root",
                    str(Path(__file__).parent / "fixtures"),
                    "--output",
                    str(output_path),
                ]
            )
            self.assertEqual(exit_code, 0)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(report["requested_benchmarks"], ["fixture_suite"])
            self.assertEqual(report["benchmark_reports"][0]["name"], "fixture_suite")
            self.assertTrue(report["benchmark_reports"][0]["success"])

    def test_run_benchmark_cli_logs_workspace_configuration_requests(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "benchmarks.json"
            config_capture = Path(temp_dir) / "workspace-config.json"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "run-benchmark",
                        "--server-command",
                        sys.executable,
                        "--server-arg",
                        str(server_script),
                        "--server-arg=--request-workspace-config-output",
                        "--server-arg",
                        str(config_capture),
                        "--benchmark-root",
                        str(Path(__file__).parent / "fixtures"),
                        "--output",
                        str(output_path),
                    ]
                )

            self.assertEqual(exit_code, 0)
            output = stdout.getvalue()
            self.assertIn("workspace/didChangeConfiguration", output)
            self.assertIn("workspace/configuration request", output)

    def test_benchmark_validation_fails_on_empty_results(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            suite_root = temp_path / "invalid_suite"
            source_dir = suite_root / "src"
            source_dir.mkdir(parents=True, exist_ok=True)
            (source_dir / "app.py").write_text("value = 1\nvalue\n", encoding="utf-8")
            (suite_root / "config.json").write_text(
                json.dumps(
                    {
                        "name": "invalid_suite",
                        "workspace_dir": "src",
                        "iterations": 2,
                        "warmup_iterations": 1,
                        "completion_points": [
                            {
                                "label": "completion validation",
                                "file": "src/app.py",
                                "line": 1,
                                "character": 3,
                                "validation": {"minCompletionItems": 1},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            report = run_benchmarks(
                command=[sys.executable, str(server_script), "--completion-items", "0"],
                benchmark_names=["invalid_suite"],
                benchmark_root=temp_path,
                timeout_seconds=2.0,
            )

            suite_report = report.benchmark_reports[0]
            self.assertFalse(suite_report.success)
            point_report = suite_report.points[0]
            self.assertFalse(point_report.success)
            self.assertFalse(point_report.summary["validation"]["passed"])
            self.assertIn("completion_item_count=0", point_report.error_message)

    def test_isolated_environment_creates_suite_venv_and_rewrites_python_command(self) -> None:
        server_script = Path(__file__).parent / "fixtures" / "fake_lsp_server.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            env_capture = Path(temp_dir) / "env.json"
            report = run_benchmarks(
                command=[sys.executable, str(server_script), "--write-env", str(env_capture)],
                benchmark_names=["fixture_suite"],
                benchmark_root=Path(__file__).parent / "fixtures",
                timeout_seconds=2.0,
                environment_mode="isolated",
                environment_root=Path(temp_dir) / "envs",
            )
            suite_report = report.benchmark_reports[0]
            self.assertTrue(suite_report.success)
            self.assertEqual(suite_report.environment_mode, "isolated")
            self.assertIsNotNone(suite_report.environment_path)
            self.assertTrue(Path(suite_report.environment_path).exists())

            env_data = json.loads(env_capture.read_text(encoding="utf-8"))
            self.assertEqual(Path(env_data["virtual_env"]), Path(suite_report.environment_path))
            self.assertEqual(Path(env_data["sys_executable"]), Path(suite_report.python_executable))
            bin_dir = "Scripts" if sys.platform == "win32" else "bin"
            self.assertTrue(env_data["path"].startswith(str(Path(suite_report.environment_path) / bin_dir)))


if __name__ == "__main__":
    unittest.main()