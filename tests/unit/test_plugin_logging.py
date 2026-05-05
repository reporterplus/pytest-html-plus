import json
import subprocess
import sys
import textwrap

# The plugin saves the JSON report inside the html-output folder
# (default: "report_output"), not at the cwd root.
REPORT_FILENAME = "report.json"
HTML_OUTPUT = "report_output"


def run_pytest(tmp_path, test_source, extra_args=None):
    """Run pytest in a subprocess using the current Python environment.

    --json-report only accepts a plain filename (not a path). The plugin
    writes the final JSON to <html-output>/<filename>, so the report lives at
    tmp_path / HTML_OUTPUT / REPORT_FILENAME.
    """
    test_file = tmp_path / "test_sample.py"
    test_file.write_text(textwrap.dedent(test_source))

    # Actual path where the plugin will write the report
    report_file = tmp_path / HTML_OUTPUT / REPORT_FILENAME

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(test_file),
        f"--json-report={REPORT_FILENAME}",
        f"--html-output={HTML_OUTPUT}",
        "--tb=short",
        "-p",
        "no:cacheprovider",
    ]
    if extra_args:
        cmd.extend(extra_args)

    result = subprocess.run(cmd, cwd=str(tmp_path), capture_output=True, text=True)
    return result, report_file


def load_results(report_file):
    data = json.loads(report_file.read_text())
    return data.get("results", [])


def test_passing_test_is_logged_in_json_report(tmp_path):
    result, report_file = run_pytest(
        tmp_path,
        """
        def test_always_passes():
            assert True
    """,
    )

    assert result.returncode == 0, f"Pytest failed:\n{result.stderr}\n{result.stdout}"
    assert report_file.exists(), f"Report file not created. stdout:\n{result.stdout}"

    results = load_results(report_file)
    found = any(t["nodeid"].endswith("test_always_passes") for t in results)
    assert found, "Passing test not logged in JSON report"


def test_failing_test_is_logged_with_error(tmp_path):
    result, report_file = run_pytest(
        tmp_path,
        """
        def test_always_fails():
            assert False, "intentional failure"
    """,
    )

    assert result.returncode != 0
    assert report_file.exists(), f"Report file not created. stdout:\n{result.stdout}"

    results = load_results(report_file)
    test = next((t for t in results if t["nodeid"].endswith("test_always_fails")), None)

    assert test is not None, "Failing test not logged in JSON report"
    assert test["status"] == "failed"
    assert test.get("error") is not None


def test_skipped_test_is_logged(tmp_path):
    result, report_file = run_pytest(
        tmp_path,
        """
        import pytest

        @pytest.mark.skip(reason="skipping on purpose")
        def test_skipped():
            pass
    """,
    )

    assert report_file.exists(), f"Report file not created. stdout:\n{result.stdout}"

    results = load_results(report_file)
    test = next((t for t in results if t["nodeid"].endswith("test_skipped")), None)

    assert test is not None, "Skipped test not logged in JSON report"
    assert test["status"] == "skipped"


def test_markers_are_captured_in_report(tmp_path):
    result, report_file = run_pytest(
        tmp_path,
        """
        import pytest

        @pytest.mark.smoke
        @pytest.mark.regression
        def test_with_markers():
            assert True
    """,
    )

    assert report_file.exists(), f"Report file not created. stdout:\n{result.stdout}"

    results = load_results(report_file)
    test = next((t for t in results if t["nodeid"].endswith("test_with_markers")), None)

    assert test is not None
    assert "smoke" in test.get("markers", [])
    assert "regression" in test.get("markers", [])


def test_report_file_contains_filters(tmp_path):
    result, report_file = run_pytest(
        tmp_path,
        """
        def test_one(): assert True
        def test_two(): assert False
    """,
    )

    assert report_file.exists(), f"Report file not created. stdout:\n{result.stdout}"

    data = json.loads(report_file.read_text())
    assert "filters" in data
    assert "total" in data["filters"]
    assert data["filters"]["total"] == 2
