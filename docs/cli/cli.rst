Command Line Options
====================

The CLI supports various parameters to customize report generation, formatting, delivery, and behavior across CI or local workflows.

Overview
--------
.. list-table:: CLI Options
   :header-rows: 1
   :widths: 20 40 15 40

   * - **Option**
     - **Description**
     - **Default**
     - **Use Case**
   * - ``--json-report``
     - Path to save individual JSON test reports
     - ``final_report.json``
     - Use in CI to parse/export test metadata
   * - ``--capture-screenshots``
     - When to capture screenshots
     - ``failed``
     - Useful in flaky UI tests to get screenshots on failure
   * - ``--html-output``
     - Directory for HTML output
     - ``report_output``
     - Customize output directory per CI job
   * - ``--send-email``
     - Send HTML report via email
     - ``False``
     - Enable in scheduled test runs (nightly builds)
   * - ``--should-open-report``
     - Auto-open report after run
     - ``failed``
     - Open only when failures occur locally
   * - ``--generate-xml``
     - Generate a combined XML for CI/coverage
     - ``False``
     - Integrate with CI tools expecting JUnit XML
   * - ``--xml-report``
     - Path for XML report
     - ``None``
     - Useful when generating multiple output types


Detailed Option Usage
---------------------

For detailed information, examples, and best practices for each parameter, see:

.. toctree::
   :maxdepth: 1
   :caption: CLI Flags Explained

   cli/json-report
   cli/capture-screenshots
   cli/html-output
   cli/send-email
   cli/should-open-report
   cli/generate-xml
   cli/xml-report
