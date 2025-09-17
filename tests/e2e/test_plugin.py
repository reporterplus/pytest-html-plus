import json
import os
import subprocess
import tempfile

import pytest

@pytest.mark.skip("optionally skipped")
def test_plugin_logs_expected_results():
    with tempfile.TemporaryDirectory() as tmpdir:
        report_path = os.path.join(tmpdir, "report.json")

        result = subprocess.run(
            [
                "poetry", "run", "pytest",
                "tests/dummy_tests",
                "--capture-screenshots=none",
                f"--json-report={report_path}",
            ],
            capture_output=True,
            text=True
        )

        print("STDOUT IS:", result.stdout)
        print("STDERR IS:", result.stderr)

        assert os.path.exists(report_path), "Report not generated"

        with open(report_path) as f:
            tests = json.load(f)

        expected = {
            "test_pass": "passed",
            "test_fail": "skipped",
            "test_skip": "skipped",
        }

        for test in tests["results"]:
            name = test["test"]
            expected_status = expected.get(name)
            if expected_status:
                assert test["status"] == expected_status, (
                    f"{name} should be {expected_status}, got {test['status']}"
                )

                assert "stdout" in test
                assert "stderr" in test
                assert "logs" in test
                assert "links" in test
                assert "flaky" in test
