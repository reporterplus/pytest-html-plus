Pytest HTML Plus Action
=======================

Run pytest inside GitHub Actions with **rich HTML/JSON/XML reports and screenshots**,
powered by `pytest-html-plus <https://pypi.org/project/pytest-html-plus/>`_.

This action is designed to be lightweight: it does not install your project dependencies,
but layers report generation on top of your existing pytest setup (pip or Poetry).

.. contents::
   :local:
   :depth: 2

Introduction
------------

``pytest-html-plus-action`` is a GitHub Action that lets you:

* Generate HTML, JSON, and XML reports from pytest runs.
* Capture screenshots automatically (``failed`` / ``all`` / ``none``).
* Integrate seamlessly with projects using **pip** or **Poetry**.
* Upload reports as workflow artifacts for later review.

Installation & Setup
--------------------

Add the action to your workflow after you install your project dependencies:

.. code-block:: yaml

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: "3.11"

         # Install project dependencies (choose one)
         - run: pip install -r requirements.txt
         # or
         - run: poetry install --with dev

         # Run pytest with HTML Plus reports
         - uses: reporterplus/pytest-html-plus-action@v1
           with:
             testpath: "tests/"
             htmloutput: "report_output"
             capturescreenshots: "all"
             usepoetry: "true"

         # Upload artifacts
         - uses: actions/upload-artifact@v4
           with:
             name: pytest-reports
             path: |
               report_output/
               screenshots/

Inputs Reference
----------------

Inputs Reference
----------------

The action accepts the following inputs. All values map directly to
pytest-html-plus plugin options.

.. list-table::
   :header-rows: 1
   :widths: 20 60 20

   * - Input
     - Description
     - Default
   * - ``testpath``
     - Path to test files/folders (e.g. ``tests/``). If empty, pytest auto-discovers tests.
     - ``""`` (discovery)
   * - ``pytestargs``
     - Extra pytest arguments (e.g. coverage, reruns).
     - ``""``
   * - ``jsonreport``
     - Path for JSON report.
     - ``final_report.json``
   * - ``htmloutput``
     - Directory to save HTML report.
     - ``report_output``
   * - ``screenshots``
     - Directory to save screenshots.
     - ``screenshots``
   * - ``capturescreenshots``
     - When to capture screenshots (``failed``, ``all``, ``none``).
     - ``failed``
   * - ``plusemail``
     - Send HTML report via email. (future use)
     - ``false``
   * - ``shouldopenreport``
     - When to open the report (``always``, ``failed``, ``never``).
     - ``failed``
   * - ``generatexml``
     - Generate JUnit-style XML report.
     - ``false``
   * - ``xmlreport``
     - Path to JUnit XML file.
     - ``""``
   * - ``usepoetry``
     - Run pytest through ``poetry run pytest``.
     - ``false``


Examples
--------

With Poetry
~~~~~~~~~~~

.. code-block:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       testpath: "tests/"
       htmloutput: "report_output"
       capturescreenshots: "all"
       usepoetry: "true"

With pip / requirements.txt
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       testpath: "tests/"
       htmloutput: "report_output"
       capturescreenshots: "failed"

Custom pytest args
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       testpath: "tests/"
       pytestargs: "--maxfail=1 --disable-warnings"

Artifacts and Reports
---------------------

After the action runs, you can expect the following outputs:

* ``report_output/`` — HTML report directory
* ``final_report.json`` — JSON report file
* ``screenshots/`` — screenshots (failed/all, depending on input)
* ``junit.xml`` — if ``generatexml: true``

These can be uploaded as artifacts using
``actions/upload-artifact``.

Troubleshooting
---------------

* **pytest not found** → Ensure you installed project dependencies (pip/Poetry).  
* **No INPUT_* variables** → Ensure you are using the correct release tag (e.g. ``v1``).  
* **Playwright browser errors** (if screenshots fail) → run::

    poetry run playwright install --with-deps

FAQ
---

**Q: Does this action install pytest for me?**  
No, you must install pytest in your workflow (pip or Poetry).

**Q: Can I use this without Poetry?**  
Yes, set ``usepoetry: false``.

**Q: How do I upload reports?**  
Use ``actions/upload-artifact`` in your workflow.

License
-------

MIT © 2025, reporterplus
