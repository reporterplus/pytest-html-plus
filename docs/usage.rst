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

Output Capture Policy
---------------------

By default, captured stdout and stderr are included for every reported test.
To reduce JSON and HTML report size for verbose suites, select an output policy
with ``--plus-output``.

The supported values are:

* ``all``: Include stdout and stderr for every test. This is the default and
  preserves the existing behavior.
* ``failed-only``: Include stdout and stderr only for failed tests,
  setup/teardown errors, and expected failures (XFAIL). Ordinary skips and
  passing tests do not include captured output.
* ``none``: Do not include captured stdout or stderr in the generated reports.

The policy controls the top-level ``stdout`` and ``stderr`` report fields. It
does not change retry attempt errors or traces.

For example:

.. code-block:: bash

   pytest --plus-output=failed-only

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
   output = "failed-only"
   generate-xml = true
   xml-report = "ci.xml"

.. code-block:: bash

   pytest --plus-profile=ci

Profile keys must match existing ``pytest-html-plus`` CLI option names without
the leading ``--``. Regular CLI flags still win, so you can override a profile
for a specific run:

.. code-block:: bash

   pytest --plus-profile=ci --json-report=override.json

An explicit CLI option overrides the selected profile. If neither is supplied,
the default value is ``all``.

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

.. _json-report-structure:

Report structure
^^^^^^^^^^^^^^^^

The consolidated ``final_report.json`` contains the following fields. This is a
field reference for the generated report, not a versioned JSON Schema validation
contract. Consumers should tolerate additional fields and omitted optional fields.

Top-level fields
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Field
     - JSON type
     - Meaning
   * - ``filters``
     - object
     - Summary counts and marker counts for the consolidated results.
   * - ``results``
     - array of objects
     - Test results after worker aggregation, grouped by test identity (``nodeid``).
   * - ``similar_error_groups``
     - object (optional)
     - Map of report-local group IDs to matching-message groups. Present when Similar Errors is enabled, including ``{}`` when no matches exist; absent when disabled.

Filter fields
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Field
     - JSON type
     - Meaning
   * - ``total``
     - integer
     - Number of consolidated test results.
   * - ``failed``
     - integer (optional)
     - Failed results excluding flaky tests.
   * - ``error``
     - integer (optional)
     - Results with error status, including setup/teardown errors.
   * - ``skipped``
     - integer (optional)
     - Results with skipped status.
   * - ``flaky``
     - integer (optional)
     - Results marked flaky.
   * - ``untracked``
     - integer (optional)
     - Results without external links; displayed as “Without links” in the report.
   * - ``passed``
     - integer
     - Computed as total minus failed, skipped, and error counts; not a separate count of only literal ``passed`` statuses.
   * - ``marker_counts``
     - object
     - Map of marker names to integer counts.

Count keys other than ``total`` and ``passed`` may be omitted when zero.
Treat missing count keys as zero.

Result fields
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Field
     - JSON type
     - Meaning
   * - ``test / nodeid``
     - string
     - Display name / pytest test identity, including parameter IDs where applicable.
   * - ``status``
     - string
     - Recorded result status, such as ``passed``, ``failed``, ``error``, ``skipped``, ``xfailed``, or ``xpassed``.
   * - ``duration``
     - number
     - Recorded duration in seconds.
   * - ``trace / error``
     - string or null
     - Diagnostic trace and error text when available.
   * - ``markers``
     - array of strings
     - Names of pytest markers.
   * - ``file / line``
     - string or null / integer or null
     - Source file and pytest-reported line index (zero-based).
   * - ``stdout / stderr``
     - string or null
     - Captured output; content depends on the output-capture policy.
   * - ``timestamp``
     - string
     - UTC ISO 8601 timestamp, normally ending in ``Z``.
   * - ``screenshot``
     - string or null
     - Screenshot path or configured screenshot directory. A non-null value does not guarantee a captured image; the example contains the directory ``screenshots``.
   * - ``logs``
     - string or array
     - Captured log text when present; normally ``[]`` when no logs are recorded.
   * - ``worker``
     - string or null
     - Worker identifier, for example ``main`` or ``gw0``.
   * - ``links``
     - array of strings or null
     - External links associated with the test.
   * - ``attempts``
     - array of objects
     - Recorded attempts in order; see the attempt fields below.
   * - ``attempt_count``
     - integer
     - Length of ``attempts``.
   * - ``attempt_statuses``
     - array of strings
     - Recorded statuses in attempt order.
   * - ``flaky``
     - boolean
     - True when the final attempt passed after a prior failed or error attempt.
   * - ``first_failure_index``
     - integer or null
     - Zero-based index of the first failed or error attempt; null if none.
   * - ``first_failure``
     - object or null
     - The corresponding attempt object; null if no failed/error attempt exists.
   * - ``similar_error_group``
     - string (optional)
     - Reference to a key in ``similar_error_groups``. Only matched final failed/error results receive this field.

Attempt fields
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Field
     - JSON type
     - Meaning
   * - ``status``
     - string
     - Status recorded for the attempt.
   * - ``trace / error``
     - string or null
     - Attempt-specific diagnostics.
   * - ``duration``
     - number
     - Attempt duration in seconds.
   * - ``timestamp``
     - string
     - UTC ISO 8601 timestamp for the recorded attempt.

Similarity group fields
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Field
     - JSON type
     - Meaning
   * - ``message``
     - string
     - Normalized diagnostic message used for display; matching also considers exception type.
   * - ``nodeids``
     - array of strings
     - Distinct test identities in this group, including the current test. A group contains at least two tests.

Group IDs such as ``similar-1`` are local to one report and should not be used as
stable identifiers across runs. A result's badge count is the group's number of
``nodeids`` minus one. Retries do not increase that count. Passed (including flaky),
skipped, xfailed, xpassed, and unmatched results have no ``similar_error_group``.
When disabled, neither report-level nor result-level similarity fields are added.
See :doc:`Features/similar-errors` for matching rules and configuration.

Example report
~~~~~~~~~~~~~~

This compact example is derived from a report with matching failures. It retains
two matching results and one passing result, with recomputed counts and shortened
traces. The passing result illustrates nullable diagnostics and omitted group
membership. Reports without matches use an empty ``similar_error_groups`` object
when the feature is enabled.

.. code-block:: json

   {
     "filters": {
       "failed": 2,
       "untracked": 3,
       "total": 3,
       "passed": 1,
       "marker_counts": {
         "parametrize": 2
       }
     },
     "results": [
       {
         "test": "test_matching_account_errors[login]",
         "nodeid": "tests/dummy_tests/demo_similar_errors.py::test_matching_account_errors[login]",
         "status": "failed",
         "duration": 4.9e-05,
         "trace": "raise ValueError(\"Account service returned an invalid response\")",
         "error": "E       ValueError: Account service returned an invalid response",
         "markers": [
           "parametrize"
         ],
         "file": "tests/dummy_tests/demo_similar_errors.py",
         "line": 11,
         "stdout": "",
         "stderr": "",
         "timestamp": "2026-10-26T16:51:24.424182Z",
         "screenshot": "screenshots",
         "logs": [],
         "worker": "main",
         "links": [],
         "attempts": [
           {
             "status": "failed",
             "trace": "raise ValueError(\"Account service returned an invalid response\")",
             "error": "E       ValueError: Account service returned an invalid response",
             "duration": 4.9e-05,
             "timestamp": "2026-10-26T16:51:24.424192Z"
           }
         ],
         "attempt_count": 1,
         "flaky": false,
         "attempt_statuses": [
           "failed"
         ],
         "first_failure_index": 0,
         "first_failure": {
           "status": "failed",
           "trace": "raise ValueError(\"Account service returned an invalid response\")",
           "error": "E       ValueError: Account service returned an invalid response",
           "duration": 4.9e-05,
           "timestamp": "2026-10-26T16:51:24.424192Z"
         },
         "similar_error_group": "similar-1"
       },
       {
         "test": "test_matching_account_errors[checkout]",
         "nodeid": "tests/dummy_tests/demo_similar_errors.py::test_matching_account_errors[checkout]",
         "status": "failed",
         "duration": 0.001287,
         "trace": "raise ValueError(\"Account service returned an invalid response\")",
         "error": "E       ValueError: Account service returned an invalid response",
         "markers": [
           "parametrize"
         ],
         "file": "tests/dummy_tests/demo_similar_errors.py",
         "line": 11,
         "stdout": "",
         "stderr": "",
         "timestamp": "2026-10-26T16:51:24.430781Z",
         "screenshot": "screenshots",
         "logs": [],
         "worker": "main",
         "links": [],
         "attempts": [
           {
             "status": "failed",
             "trace": "raise ValueError(\"Account service returned an invalid response\")",
             "error": "E       ValueError: Account service returned an invalid response",
             "duration": 0.001287,
             "timestamp": "2026-10-26T16:51:24.430788Z"
           }
         ],
         "attempt_count": 1,
         "flaky": false,
         "attempt_statuses": [
           "failed"
         ],
         "first_failure_index": 0,
         "first_failure": {
           "status": "failed",
           "trace": "raise ValueError(\"Account service returned an invalid response\")",
           "error": "E       ValueError: Account service returned an invalid response",
           "duration": 0.001287,
           "timestamp": "2026-10-26T16:51:24.430788Z"
         },
         "similar_error_group": "similar-1"
       },
       {
         "test": "test_passing_control",
         "nodeid": "tests/dummy_tests/demo_similar_errors.py::test_passing_control",
         "status": "passed",
         "duration": 0.000255,
         "trace": null,
         "error": null,
         "markers": [],
         "file": "tests/dummy_tests/demo_similar_errors.py",
         "line": 35,
         "stdout": "",
         "stderr": "",
         "timestamp": "2026-10-26T16:51:24.447904Z",
         "screenshot": "screenshots",
         "logs": [],
         "worker": "main",
         "links": [],
         "attempts": [
           {
             "status": "passed",
             "trace": null,
             "error": null,
             "duration": 0.000255,
             "timestamp": "2026-10-26T16:51:24.447918Z"
           }
         ],
         "attempt_count": 1,
         "flaky": false,
         "attempt_statuses": [
           "passed"
         ],
         "first_failure_index": null,
         "first_failure": null
       }
     ],
     "similar_error_groups": {
       "similar-1": {
         "message": "Account service returned an invalid response",
         "nodeids": [
           "tests/dummy_tests/demo_similar_errors.py::test_matching_account_errors[login]",
           "tests/dummy_tests/demo_similar_errors.py::test_matching_account_errors[checkout]"
         ]
       }
     }
   }

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
