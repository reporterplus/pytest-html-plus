JSON Report (`--json-report`)
=============================

The `--json-report` flag allows you to generate a JSON test report during test execution. This is particularly useful when running multiple test suites in a CI pipeline and needing to aggregate or analyze results programmatically.

Overview
--------

- **Default Output**: `final_report.json`
- **Type**: File Name
- **Usage Context**: CI pipelines, custom dashboards, post-processing

Example
-------

.. code-block:: bash

   pytest --json-report=test_report.json

This will generate a JSON report at the specified location.

Use Cases
---------

- **CI Pipelines**: When running multiple `pytest` commands in separate steps or jobs, each one can generate its own `--json-report`. These can be merged or parsed later for summarization.
- **Dashboards**: Feed the JSON into internal dashboards or analytics tools to visualize pass/fail rates, duration trends, or flaky tests.
- **Custom Post-Processing**: Build scripts or bots to analyze test results, auto-label flaky tests, or trigger alerts based on JSON content.

Integrations
------------

- Combine with `--generate-xml` and `--html-output` to produce a full suite of structured outputs.
- The JSON report includes metadata such as:

  - Test name
  - Status (pass/fail/skipped)
  - Duration
  - File location and line number

.. note::

   If you're running multiple pytest commands (e.g., across parallel jobs in CI), ensure each job outputs to a unique file path to avoid overwriting reports.

