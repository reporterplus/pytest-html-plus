HTML Output Directory (`--html-output`)
=======================================

The `--html-output` flag defines the directory where the final HTML report will be saved. This is useful for organizing output per test suite, CI job, or developer machine.

Overview
--------

- **Default**: `report_output`
- **Type**: Directory path
- **Usage Context**: CI pipelines, test result review, team collaboration

Example
-------

.. code-block:: bash

   pytest --html-output=reports/ui-smoke

This command will generate the HTML report under the `reports/ui-smoke/` directory.

Use Cases
---------

- **CI Pipelines**: Use a unique folder per job (`html-output=reports/$JOB_NAME`) to avoid conflicts across parallel runs.
- **Local Runs**: Developers can store their reports separately to avoid overwriting shared output.
- **Multiple Test Suites**: Organize results by suite, e.g., `unit/`, `integration/`, `ui/`.

Report Contents
---------------

- The directory will contain:

  - `index.html`: Main interactive report file.
  - `screenshots/`: Embedded screenshots (if `--capture-screenshots` is used).
  - `metadata.json`: Optional test metadata

Integration
-----------

- Automatically works with:

  - `--capture-screenshots`: embeds screenshots in the report.
  - `--plus-email`: attaches this directory for delivery.
  - `--should-open-report`: opens `index.html` after run.

.. note::

   Ensure the target directory exists or the framework will create it. You may also use relative or absolute paths as needed.