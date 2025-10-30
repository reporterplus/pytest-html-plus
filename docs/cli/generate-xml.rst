Generate JUnit XML Report (`--generate-xml`, `--xml-report`)
=============================================================

You can generate a combined JUnit-style XML test report from multiple runs using the `--generate-xml` flag. This is particularly useful for integrating with CI tools and test management systems.

Flags Overview
--------------

- ``--generate-xml``
  Enables generation of a combined XML report.
  **Default:** ``False``
  **Accepted Values:** ``True``, ``False``

- ``--xml-report``
  Specifies the path where the combined XML report should be written. Make sure the directory exists
  **Default:** ``None``
  **Accepted Values:** Any valid file path (e.g., ``report_output/final_report.xml``)

Usage Example
-------------

.. code-block:: bash

   pytest --generate-xml True --xml-report report_output/final_report.xml

This will aggregate the test results from all discovered test cases and output a single JUnit-compatible XML report to `report_output/final_report.xml`.

Use Cases
---------

- **CI/CD Pipelines**
  Upload the XML report as a test artifact or feed it directly into tools like:

  - Jenkins (via JUnit plugin)
  - GitLab CI (``junit`` reports)
  - CircleCI test summary
  - Azure DevOps test publishing

- **Test Management Tools**
  Export and import the XML report into platforms such as:

  - Testmo
  - TestRail
  - PractiTest
  - Zephyr

  These tools can parse the XML structure and associate results with test cases and runs automatically.

- **Dashboard Integrations**
  Many internal or third-party dashboards can consume XML test reports for test analytics and history tracking.

Report Contents
---------------

- The XML report includes:
  - Complete test case metadata (name, duration, result status)
  - Captured stdout, stderr output, `print()` statements
  - Loggers and traceback messages
  - Failure reasons and exception types

Important Notes
---------------

- The `--xml-report` flag **must be provided** when `--generate-xml` is set to `True`. Otherwise, the plugin will raise an error.
- The generated XML follows the widely accepted JUnit report schema and is compatible with most tools that support it.
- Useful when combining results from sharded or parallel test runs.