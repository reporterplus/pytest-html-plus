"""
Tests for --worker-json-dir, the directory where pytest-xdist workers write
their partial JSON reports before the controller merges them.

The historical location (.pytest_worker_jsons relative to the cwd) cannot be
created when the cwd is read-only, e.g. in Kubernetes containers with
readOnlyRootFilesystem, so it has to be configurable.
"""

import json
import os
import stat
import subprocess
import sys

import pytest

pytest.importorskip("xdist")

SAMPLE_TESTS = """
def test_one():
    assert True


def test_two():
    assert True
"""

# Variables that would make the inner pytest run think it is an xdist worker
# when this suite itself runs under xdist.
_LEAKY_ENV_VARS = (
    "PYTEST_XDIST_WORKER",
    "PYTEST_XDIST_WORKER_COUNT",
    "PYTEST_XDIST_TESTRUNUID",
    "PYTEST_ADDOPTS",
    "PYTEST_CURRENT_TEST",
)


def make_project(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    (project / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (project / "test_sample.py").write_text(SAMPLE_TESTS, encoding="utf-8")
    return project


def run_pytest_with_xdist(cwd, *extra_args):
    env = {k: v for k, v in os.environ.items() if k not in _LEAKY_ENV_VARS}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-n",
            "2",
            "-p",
            "no:cacheprovider",
            "--should-open-report=never",
            *extra_args,
        ],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )


def assert_run_passed(result):
    assert result.returncode == 0, f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"


def test_worker_jsons_are_written_to_configured_dir(tmp_path):
    project = make_project(tmp_path)
    worker_dir = tmp_path / "out" / "worker-jsons"

    result = run_pytest_with_xdist(
        project,
        f"--worker-json-dir={worker_dir}",
        f"--html-output={tmp_path / 'out' / 'report'}",
    )

    assert_run_passed(result)
    assert not (project / ".pytest_worker_jsons").exists()
    assert list(worker_dir.glob("gw*.json"))


def test_controller_merges_worker_jsons_from_configured_dir(tmp_path):
    project = make_project(tmp_path)
    html_output = tmp_path / "out" / "report"

    result = run_pytest_with_xdist(
        project,
        f"--worker-json-dir={tmp_path / 'out' / 'worker-jsons'}",
        f"--html-output={html_output}",
    )

    assert_run_passed(result)
    report = json.loads((html_output / "final_report.json").read_text())
    assert sorted(t["test"] for t in report["results"]) == ["test_one", "test_two"]


def test_worker_json_dir_defaults_to_pytest_worker_jsons_in_cwd(tmp_path):
    project = make_project(tmp_path)

    result = run_pytest_with_xdist(
        project, f"--html-output={tmp_path / 'out' / 'report'}"
    )

    assert_run_passed(result)
    assert list((project / ".pytest_worker_jsons").glob("gw*.json"))


@pytest.mark.skipif(
    sys.platform == "win32" or os.geteuid() == 0,
    reason="read-only directories are not enforced on Windows or for root",
)
def test_xdist_run_succeeds_in_read_only_cwd(tmp_path):
    project = make_project(tmp_path)
    writable = tmp_path / "writable"
    html_output = writable / "report"

    project.chmod(stat.S_IRUSR | stat.S_IXUSR)
    try:
        result = run_pytest_with_xdist(
            project,
            f"--worker-json-dir={writable / 'worker-jsons'}",
            f"--html-output={html_output}",
            f"--screenshots={writable / 'screenshots'}",
        )
    finally:
        project.chmod(stat.S_IRWXU)

    assert_run_passed(result)
    assert (html_output / "report.html").exists()
    assert sorted(os.listdir(project)) == ["pytest.ini", "test_sample.py"]
