Generate JUnit XML Report (`--generate-xml`, `--xml-report`)
=============================================================

You can generate a combined JUnit-style XML test report from your test run using the
``--generate-xml`` flag. This is particularly useful for integrating with CI tools and
test management systems.

Flags Overview
--------------

- ``--generate-xml``
  Enables generation of a combined XML report. This is a boolean switch — include the
  flag to enable it, omit it to disable it. It does not take a value.

  **Default:** disabled (XML is not generated unless the flag is passed)

  **Usage:** ``--generate-xml`` (do not pass ``True``/``False`` after it)

- ``--xml-report``
  Specifies the **filename** of the XML report (not a path). The file is always written
  inside the directory set by ``--html-output``, so only a bare filename is accepted —
  passing a path (e.g. ``report_output/final_report.xml``) will raise a
  ``pytest.UsageError``.

  **Default:** ``final_xml.xml``

  **Accepted Values:** any valid filename, e.g. ``final_report.xml``

Usage Example
-------------

.. code-block:: bash

   pytest --generate-xml --html-output report_output --xml-report final_report.xml

This will aggregate the test results from the run and write a single JUnit-compatible
XML report to ``report_output/final_report.xml`` or the folder chosen in ``--html-output``

If ``--xml-report`` is omitted, the file defaults to ``final_xml.xml`` inside the
``--html-output`` directory:

.. code-block:: bash

   pytest --generate-xml --html-output report_output
   # -> report_output/final_xml.xml

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

  These tools can parse the XML structure and associate results with test cases and runs
  automatically.

- **Dashboard Integrations**
  Many internal or third-party dashboards can consume XML test reports for test
  analytics and history tracking.

Report Contents
---------------

- The XML report includes:

  - Complete test case metadata (name, duration, result status)
  - Captured stdout, stderr output, ``print()`` statements
  - Loggers and traceback messages
  - Failure reasons and exception types

Important Notes
---------------

- ``--generate-xml`` is a boolean flag with no value — passing ``--generate-xml True``
  is invalid and will not behave as expected.
- ``--xml-report`` must be a **bare filename**, not a path. The file is always placed
  inside the ``--html-output`` directory. Passing a path will raise
  ``pytest.UsageError: --xml-report must be a filename, not a path``.
- ``--xml-report`` is **optional**. If omitted, the report defaults to
  ``final_xml.xml`` inside the ``--html-output`` directory — no error is raised.
- The generated XML follows the widely accepted JUnit report schema and is compatible
  with most tools that support it.
- The XML is generated from the merged JSON report, so it reflects combined results
  from sharded or parallel (``pytest-xdist``) runs as well as single-worker runs.