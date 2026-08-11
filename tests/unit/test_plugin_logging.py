import json
import subprocess
import sys
import textwrap

import pytest

# The plugin saves the JSON report inside the html-output folder
# (default: "report_output"), not at the cwd root.
REPORT_FILENAME = "report.json"
HTML_OUTPUT = "report_output"


def run_pytest(tmp_path, test_source, extra_args=None):
    """Run pytest in a subprocess using the current Python environment.

    --json-report only accepts a plain filename (not a path). The plugin
    writes the final JSON to <html-output>/<filename>, so the report lives at
    tmp_path / HTML_OUTPUT / REPORT_FILENAME.

    Args:
        tmp_path: Temporary directory where test files and outputs are created.
        test_source: Python source code for the test module to execute.
        extra_args: Optional list of additional command-line arguments to pass
            to pytest.
    """
    test_file = tmp_path / "test_sample.py"
    test_file.write_text(textwrap.dedent(test_source))

    # Register any custom marks used in test sources so that PYTHONWARNINGS=error
    # (set by CI) doesn't turn PytestUnknownMarkWarning into a fatal collection error.
    conftest = tmp_path / "conftest.py"
    conftest.write_text(
        textwrap.dedent(
            """\
        def pytest_configure(config):
            config.addinivalue_line("markers", "smoke: smoke tests")
            config.addinivalue_line("markers", "regression: regression tests")
    """
        )
    )

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
    """Load test results from a JSON report file.

    Args:
        report_file: Path object pointing to the JSON report file.

    Returns:
        A list of test result dictionaries from the report's "results" field.
        Returns an empty list if the field is missing.
    """
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


@pytest.mark.parametrize(
    ("policy", "should_include"),
    [
        (None, True),
        ("all", True),
        ("failed-only", False),
        ("none", False),
    ],
)
def test_plus_output_policy_for_passing_test(tmp_path, policy, should_include):
    extra_args = [f"--plus-output={policy}"] if policy else []
    result, report_file = run_pytest(
        tmp_path,
        """
        import sys

        def test_passes():
            print("stdout from pass")
            print("stderr from pass", file=sys.stderr)
            assert True
        """,
        extra_args=extra_args,
    )

    assert result.returncode == 0, f"Pytest failed:\n{result.stderr}\n{result.stdout}"
    test = next(
        test
        for test in load_results(report_file)
        if test["nodeid"].endswith("test_passes")
    )

    if should_include:
        assert "stdout from pass" in test["stdout"]
        assert "stderr from pass" in test["stderr"]
    else:
        assert test["stdout"] == ""
        assert test["stderr"] == ""


@pytest.mark.parametrize(
    ("policy", "should_include"),
    [
        ("all", True),
        ("failed-only", True),
        ("none", False),
    ],
)
def test_plus_output_policy_for_failing_test(tmp_path, policy, should_include):
    result, report_file = run_pytest(
        tmp_path,
        """
        import sys

        def test_fails():
            print("stdout from failure")
            print("stderr from failure", file=sys.stderr)
            assert False, "intentional failure"
        """,
        extra_args=[f"--plus-output={policy}"],
    )

    assert result.returncode != 0
    test = next(
        test
        for test in load_results(report_file)
        if test["nodeid"].endswith("test_fails")
    )

    if should_include:
        assert "stdout from failure" in test["stdout"]
        assert "stderr from failure" in test["stderr"]
    else:
        assert test["stdout"] == ""
        assert test["stderr"] == ""

    assert test["error"]
    assert test["trace"]
    assert test["attempts"][0]["error"]
    assert test["attempts"][0]["trace"]


def test_failed_only_keeps_setup_failure_output(tmp_path):
    result, report_file = run_pytest(
        tmp_path,
        """
        import sys

        import pytest

        @pytest.fixture
        def broken_fixture():
            print("setup stdout")
            print("setup stderr", file=sys.stderr)
            raise RuntimeError("setup failed")

        def test_setup_failure(broken_fixture):
            pass
        """,
        extra_args=["--plus-output=failed-only"],
    )

    assert result.returncode != 0
    test = next(
        test
        for test in load_results(report_file)
        if test["nodeid"].endswith("test_setup_failure")
    )

    assert test["status"] == "error"
    assert "setup stdout" in test["stdout"]
    assert "setup stderr" in test["stderr"]


def test_failed_only_keeps_xfail_output(tmp_path):
    result, report_file = run_pytest(
        tmp_path,
        """
        import sys

        import pytest

        @pytest.mark.xfail(reason="known issue")
        def test_expected_failure():
            print("xfail stdout")
            print("xfail stderr", file=sys.stderr)
            assert False
        """,
        extra_args=["--plus-output=failed-only"],
    )

    assert result.returncode == 0
    test = next(
        test
        for test in load_results(report_file)
        if test["nodeid"].endswith("test_expected_failure")
    )

    assert test["status"] == "skipped"
    assert "xfail stdout" in test["stdout"]
    assert "xfail stderr" in test["stderr"]
