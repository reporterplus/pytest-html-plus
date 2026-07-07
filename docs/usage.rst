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

Reusable Profiles
-----------------

If you want to reuse the same reporting options across local runs and CI jobs,
define a named profile in ``pyproject.toml`` and activate it with
``--plus-profile``.

.. code-block:: toml

   [tool.pytest-html-plus.profiles.ci]
   html-output = "ci-report"
   json-report = "ci.json"
   capture-screenshots = "failed"
   generate-xml = true
   xml-report = "ci.xml"

.. code-block:: bash

   pytest --plus-profile=ci

Profile keys must match existing ``pytest-html-plus`` CLI option names without
the leading ``--``. Regular CLI flags still win, so you can override a profile
for a specific run:

.. code-block:: bash

   pytest --plus-profile=ci --json-report=override.json

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
       "skipped": 1,
       "untracked": 75,
       "failed": 5,
       "total": 77,
       "passed": 71,
       "marker_counts": {
         "skip": 1,
         "parametrize": 5,
         "jira": 1,
         "link": 1
       }
     },
     "results": [
       {
         "test": "test_skipped_example",
         "nodeid": "tests/unit/test_convert_json_to_junit_xml.py::test_skipped_example",
         "status": "skipped",
         "duration": 0.0001316650000262598,
         "trace": null,
         "error": null,
         "markers": [
           "skip"
         ],
         "file": "tests/unit/test_convert_json_to_junit_xml.py",
         "line": 13,
         "stdout": "",
         "stderr": "",
         "timestamp": "2026-07-07T06:16:43.404084Z",
         "screenshot": "screenshots",
         "logs": [],
         "worker": "gw0",
         "links": [],
         "attempts": [
           {
             "status": "skipped",
             "trace": null,
             "error": null,
             "duration": 0.0001316650000262598,
             "timestamp": "2026-07-07T06:16:43.404107Z"
           }
         ],
         "attempt_count": 1,
         "flaky": false,
         "attempt_statuses": [
           "skipped"
         ],
         "first_failure_index": null,
         "first_failure": null
       }
     ]
   }

You can easily parse this using Python, JavaScript, or any JSON-compatible tool.

Retry / flaky metadata
~~~~~~~~~~~~~~~~~~~~~~

Each test result includes retry-aware metadata:

* ``attempts``: List of recorded attempts for the test.
* ``attempt_count``: Total number of attempts made for the test.
* ``attempt_statuses``: Status of each attempt in order.
* ``flaky``: ``true`` when the test failed in an earlier attempt but eventually passed.
* ``first_failure_index``: Index of the first failed attempt, or ``null`` if the test never failed.
* ``first_failure``: Failure details from the first failed attempt, or ``null`` if unavailable.

Metadata Schema
^^^^^^^^^^^^^^^

Alongside the main JSON report, the plugin writes a lightweight metadata file
named ``plus_metadata.json`` (in the root directory). This captures
high-value, actionable context for the run and is also rendered at the top of
the HTML report.

**File:** ``<root>/plus_metadata.json``

Example
~~~~~~~

.. code-block:: json

   {
     "report_title": "report_output",
     "environment": "staging",
     "branch": "feature/login-flow",
     "commit": "e1b6737f858a7ceb1da88de2ed5d368ee6206408",
     "python_version": "3.11.7",
     "pytest_version": "8.3.3",
     "generated_at": "2025-08-20T12:34:56.123456"
   }

Fields
~~~~~~

- ``report_title`` (string)
  The title shown in the HTML header. By default this is derived from the
  ``--html-output`` folder name (e.g., ``report_output``). Can be overridden with
  ``--html-output``.

- ``environment`` (string)
  Target environment (e.g., ``staging``, ``prod-sim``). Auto-detected from common
  CLI flags if present (``--env`` or ``--environment``). Defaults to ``"NA"`` unless additionally `--rp-env`` if
  not provided.

- ``branch`` (string)
  Git branch at test time.
  Falls back to ``"NA"`` if git info isn’t available (e.g., not a repo).

- ``commit`` (string)
  Full commit SHA for traceability. Falls back to ``"NA"`` if unavailable.


- ``python_version`` (string)
  Python interpreter version used for the run (e.g., ``3.11.7``).

- ``generated_at`` (ISO 8601 string)
  Timestamp when metadata was created, e.g., ``2025-08-20T12:34:56.123456``.

Behavior & Notes
~~~~~~~~~~~~~~~~

- **Zero-config:** All fields are collected automatically where possible.
- **Overrides:**
  - Title: ``--plus-report-title="My Nightly Report"``
  - Environment: pass your usual flag (``--env`` or ``--environment``); if your project has it already, the plugin will pick it up, else pass --rp-env
- **Non-git folders / CI without checkout:** Branch/commit gracefully become ``"NA"`` (no failures).
- **xdist:** Metadata is written **once** (on the controller), not per worker.
- **Portability:** The HTML report reads this file at render time and shows a compact,
  copy-ready “Run Metadata” section at the top.

Tip
~~~

Keep metadata lean and high-value. We intentionally avoid low-actionability fields
(e.g., full ``pip freeze`` or OS package lists) to keep reports **fast**, **portable**, and
**CI-artifact friendly**.
