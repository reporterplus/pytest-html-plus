Usage Guide
===========

This guide explains how to use the plugin effectively both during local development and in Continuous Integration (CI) pipelines.

Quick Start
-----------

Install the plugin using pip:

.. code-block:: bash

   pip install pytest-html-plus

Like your usual approach, run your pytest

.. code-block:: bash

   pytest (OR)
   pytest -n auto (OR)
   pytest -n auto --reruns 1

This will:
- Generate a combined JSON test report called final_report.json
- Create a visual HTML report inside the `report_output/` folder

The JSON report (`final_report.json`)
--------------------------------------

The JSON file contains rich, structured test metadata that you can use beyond HTML reporting:

Use Cases:
^^^^^^^^^^

- 📊 **Internal Dashboards**:
  - Feed data into tools like Grafana, Tableau, or custom React dashboards.
  - Track test pass/fail trends over time, flaky test rates, test durations, and more.
  - Combine with Git metadata (commit hash, branch, author) to analyze test health by developer or feature area.

- 🔁 **Automated Analytics**:
  - Run periodic jobs to parse the JSON and detect:
    - Slow tests
    - Most flaky tests
    - Recently added tests with high failure rates
    - Tag-based trends (e.g., `@smoke`, `@login`, etc.)

- ⚠️ **Slack/Email Notifications**:
  - Send summaries directly from JSON (e.g., “3 failures in checkout flow”).
  - Include direct links to Playwright traces or screenshots in messages.

- 📂 **Storing Historical Test Data**:
  - Archive reports from each CI run into S3, GCS, or internal storage.
  - Useful for audits, traceability, or debugging intermittent failures over time.

- 🔌 **Custom Integrations**:
  - Push data into test case management systems (e.g., TestRail, Xray).
  - Trigger Jira ticket creation when critical tests fail.

Structure Preview:
^^^^^^^^^^^^^^^^^^
The report has a structure like:

.. code-block:: json

   {
  "filters": {
    "skipped": 3,
    "untracked": 43,
    "flaky": 1,
    "total": 45,
    "passed": 42,
    "marker_counts": {
      "xfail": 1,
      "link": 2,
      "flaky": 2,
      "skip": 2,
      "parametrize": 5
    }
  },
  "results": [
    {
      "test": "test_fail",
      "nodeid": "tests/dummy_tests/test_cases.py::test_fail",
      "status": "skipped",
      "duration": 0.00022258399999997014,
      "error": null,
      "markers": [
        "xfail",
        "link",
        "flaky"
      ],
      "file": "tests/dummy_tests/test_cases.py",
      "line": 5,
      "stdout": "stdout from fail\n",
      "stderr": "stderr from fail\n",
      "timestamp": "2025-07-25T16:31:27.507785Z",
      "screenshot": "screenshots",
      "logs": [],
      "worker": "main",
      "links": [
        "https://example.com/fail-trace"
      ],
      "flaky": false
    }]

You can easily parse this using Python, JavaScript, or any JSON-compatible tool.