pytest-html-plus-action
=======================

   Run pytest with `pytest-html-plus <https://reporterplus.io>`__ and
   get rich HTML reports, JSON outputs, step summaries, and PR comments
   — without adding the plugin to your project dependencies.


--------------

Overview
--------

This GitHub Action installs and runs ``pytest-html-plus`` in your CI
pipeline. It is designed for teams who want report generation handled
entirely by the action, keeping their ``pyproject.toml`` or
``requirements.txt`` clean.

**What it does:**

-  Installs ``pytest-html-plus`` and runs your test suite
-  Generates an HTML report and uploads it as a workflow artifact
-  Writes a test summary to the GitHub step summary page
-  Optionally posts a summary comment on pull requests
-  Exposes structured step outputs (``total``, ``passed``, ``failed``,
   ``skipped``, ``duration``) for downstream steps

--------------

Quick Start
-----------

.. code:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1

That’s it. With all defaults, this will:

-  Run ``pytest`` from the repo root
-  Generate ``final_report.json`` and an HTML report in
   ``report_output/``
-  Upload the HTML report as a workflow artifact named
   ``pytest-html-plus-report``
-  Write a summary to the GitHub step summary page

--------------

Inputs
------

+-----------------------+-----------------------+-----------------------+
| Input                 | Description           | Default               |
+=======================+=======================+=======================+
| ``test_path``         | Path or target for    | ``""``                |
|                       | pytest                |                       |
|                       | (e.g. ``tests/``). If |                       |
|                       | empty, pytest         |                       |
|                       | discovery runs from   |                       |
|                       | repo root.            |                       |
+-----------------------+-----------------------+-----------------------+
| ``pytest_args``       | Additional arguments  | ``""``                |
|                       | passed directly to    |                       |
|                       | pytest.               |                       |
+-----------------------+-----------------------+-----------------------+
| ``json_report``       | Path for the JSON     | ``final_report.json`` |
|                       | report file.          |                       |
+-----------------------+-----------------------+-----------------------+
| ``html_output``       | Directory to save the | ``report_output``     |
|                       | HTML report.          |                       |
+-----------------------+-----------------------+-----------------------+
| ``screenshots``       | Directory to save     | ``screenshots``       |
|                       | screenshots.          |                       |
+-----------------------+-----------------------+-----------------------+
| ``                    | When to capture       | ``failed``            |
| capture_screenshots`` | screenshots:          |                       |
|                       | ``failed``, ``all``,  |                       |
|                       | or ``none``.          |                       |
+-----------------------+-----------------------+-----------------------+
| `                     | When to auto-open the | ``failed``            |
| `should_open_report`` | report locally:       |                       |
|                       | ``always``,           |                       |
|                       | ``failed``, or        |                       |
|                       | ``never``.            |                       |
+-----------------------+-----------------------+-----------------------+
| ``generate_xml``      | Generate a            | ``false``             |
|                       | JUnit-style XML       |                       |
|                       | report.               |                       |
+-----------------------+-----------------------+-----------------------+
| ``xml_report``        | Path for the XML      | ``""``                |
|                       | report file.          |                       |
+-----------------------+-----------------------+-----------------------+
| ``plus_email``        | Send the HTML report  | ``false``             |
|                       | via email (requires   |                       |
|                       | email config in       |                       |
|                       | plugin).              |                       |
+-----------------------+-----------------------+-----------------------+
| ``use_poetry``        | Run pytest through    | ``false``             |
|                       | Poetry                |                       |
|                       | (``                   |                       |
|                       | poetry run pytest``). |                       |
|                       | Cannot be combined    |                       |
|                       | with ``use_uv``.      |                       |
+-----------------------+-----------------------+-----------------------+
| ``use_uv``            | Run pytest through uv | ``false``             |
|                       | (``uv run pytest``).  |                       |
|                       | Cannot be combined    |                       |
|                       | with ``use_poetry``.  |                       |
+-----------------------+-----------------------+-----------------------+
| ``git_branch``        | Git branch name to    | ``""``                |
|                       | embed in the report.  |                       |
+-----------------------+-----------------------+-----------------------+
| ``git_commit``        | Git commit SHA to     | ``""``                |
|                       | embed in the report.  |                       |
+-----------------------+-----------------------+-----------------------+
| ``post_pr_comment``   | Post a summary        | ``false``             |
|                       | comment on the pull   |                       |
|                       | request.              |                       |
+-----------------------+-----------------------+-----------------------+
| ``github_token``      | GitHub token for      | ``""``                |
|                       | posting PR comments.  |                       |
|                       | Required when         |                       |
|                       | ``post_pr_comment``   |                       |
|                       | is ``true``.          |                       |
+-----------------------+-----------------------+-----------------------+
| ``u                   | Upload the HTML       | ``true``              |
| pload_html_artifact`` | report as a GitHub    |                       |
|                       | Actions artifact.     |                       |
+-----------------------+-----------------------+-----------------------+
| `                     | Name of the uploaded  | ``pyte                |
| `html_artifact_name`` | artifact.             | st-html-plus-report`` |
+-----------------------+-----------------------+-----------------------+
| ``plugin_version``    | Version of            | ``""``                |
|                       | ``pytest-html-plus``  |                       |
|                       | to install. Defaults  |                       |
|                       | to latest.            |                       |
+-----------------------+-----------------------+-----------------------+

Outputs
-------

============ ====================================
Output       Description
============ ====================================
``total``    Total number of tests
``passed``   Number of passed tests
``failed``   Number of failed or errored tests
``skipped``  Number of skipped tests
``duration`` Sum of all test durations in seconds
============ ====================================

--------------

Use Cases
---------

1. Minimal — zero config
~~~~~~~~~~~~~~~~~~~~~~~~

Run pytest with full report generation and artifact upload, no
configuration needed.

.. code:: yaml

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: "3.12"
         - run: pip install -r requirements.txt
         - uses: reporterplus/pytest-html-plus-action@v1

--------------

2. Run a specific test directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       test_path: tests/unit

--------------

3. Pass additional pytest arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Coverage, reruns, markers, and any other pytest flags go in
``pytest_args``.

.. code:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       test_path: tests/
       pytest_args: >-
         --cov=mypackage
         --cov-fail-under=80
         --cov-report=term
         --reruns 2
         --ignore=tests/browser

--------------

4. Poetry project
~~~~~~~~~~~~~~~~~

.. code:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       use_poetry: "true"
       test_path: tests/

Make sure ``poetry install`` has already run in a previous step.

--------------

5. uv project
~~~~~~~~~~~~~

``uv`` is not pre-installed on GitHub-hosted runners, so install it
first with the official setup action.

.. code:: yaml

   - uses: astral-sh/setup-uv@v5

   - name: Install dependencies
     run: uv sync

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       use_uv: "true"
       test_path: tests/

``use_uv`` and ``use_poetry`` are mutually exclusive — setting both to
``true`` will fail the step with a clear error before pytest runs.

--------------

6. Post a summary comment on pull requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       post_pr_comment: "true"
       github_token: ${{ secrets.GITHUB_TOKEN }}

The comment includes total, passed, failed, skipped, duration, and a
list of up to 5 failed test cases.

--------------

7. Embed git context in the report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Useful when sharing reports outside of GitHub — the report itself shows
which branch and commit it was generated from.

.. code:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       git_branch: ${{ github.ref_name }}
       git_commit: ${{ github.sha }}

--------------

8. Generate a JUnit XML report alongside HTML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Useful for integrating with tools that consume JUnit XML (e.g. test
analytics platforms, SonarQube).

.. code:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       generate_xml: "true"
       xml_report: reports/junit.xml

--------------

9. Use step outputs to conditionally fail or notify
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1
     id: pytest
     with:
       test_path: tests/

   - name: Print test summary
     run: |
       echo "Total: ${{ steps.pytest.outputs.total }}"
       echo "Passed: ${{ steps.pytest.outputs.passed }}"
       echo "Failed: ${{ steps.pytest.outputs.failed }}"

   - name: Notify on failure
     if: ${{ steps.pytest.outputs.failed > 0 }}
     run: echo "::warning::${{ steps.pytest.outputs.failed }} test(s) failed"

--------------

10. Pin the plugin version for reproducible CI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       plugin_version: "1.2.0"

Recommended for teams with strict dependency policies or those who want
to upgrade the plugin intentionally rather than automatically picking up
the latest release.

--------------

11. Custom artifact name per matrix leg
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When running a test matrix (e.g. multiple OS or Python versions), give
each artifact a unique name so they don’t overwrite each other.

.. code:: yaml

   jobs:
     test:
       strategy:
         matrix:
           os: [ubuntu-latest, windows-latest]
           python-version: ["3.11", "3.12"]
       runs-on: ${{ matrix.os }}
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: ${{ matrix.python-version }}
         - run: pip install -r requirements.txt
         - uses: reporterplus/pytest-html-plus-action@v1
           with:
             html_artifact_name: report-${{ matrix.os }}-py${{ matrix.python-version }}

--------------

12. Screenshot capture on failure (browser/UI tests)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For projects using Playwright or Selenium, screenshots of failed tests
are captured automatically and included in the HTML report.

.. code:: yaml

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       test_path: tests/browser
       capture_screenshots: failed
       screenshots: test-screenshots

Set ``capture_screenshots: all`` to capture every test regardless of
outcome.

--------------

13. PYTHONWARNINGS — treat warnings as errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The action has no dedicated input for environment variables, but any
variable written to ``$GITHUB_ENV`` in a prior step persists into the
action’s environment.

.. code:: yaml

   - name: Configure Python warnings
     run: echo "PYTHONWARNINGS=error" >> $GITHUB_ENV

   - uses: reporterplus/pytest-html-plus-action@v1
     with:
       test_path: tests/
       xml_report: reports/junit_warnings.xml
       html_output: report_output_warnings

--------------

14. Full production setup
~~~~~~~~~~~~~~~~~~~~~~~~~

A complete example combining git context, PR comments, XML output,
coverage, and reruns.

.. code:: yaml

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - uses: actions/setup-python@v5
           with:
             python-version: "3.12"

         - name: Install dependencies
           run: pip install -r requirements.txt

         - uses: reporterplus/pytest-html-plus-action@v1
           id: pytest
           with:
             use_poetry: "false"
             test_path: tests/
             pytest_args: >-
               --cov=mypackage
               --cov-fail-under=75
               --cov-report=term
               --reruns 1
             git_branch: ${{ github.ref_name }}
             git_commit: ${{ github.sha }}
             generate_xml: "true"
             xml_report: reports/junit.xml
             html_output: report_output
             html_artifact_name: test-report-${{ github.run_id }}
             post_pr_comment: "true"
             github_token: ${{ secrets.GITHUB_TOKEN }}

         - name: Fail with context if tests failed
           if: ${{ steps.pytest.outputs.failed > 0 }}
           run: |
             echo "${{ steps.pytest.outputs.failed }} of ${{ steps.pytest.outputs.total }} tests failed"
             exit 1

--------------

Notes
-----

**Windows runners:** The action uses a bash entrypoint and is not
compatible with Windows runners. Use ``ubuntu-latest`` or
``macos-latest``.

**Self-hosted runners:** Ensure Python and pip are available on the
runner. The action installs ``pytest-html-plus`` at runtime via pip.

**Air-gapped environments:** If your runner cannot reach PyPI,
pre-install ``pytest-html-plus`` in your runner image and set
``plugin_version`` to the pre-installed version to avoid the install
step attempting to upgrade.

**PR comments accumulate:** Each push to a PR branch posts a new comment
rather than updating the previous one. If comment volume is a concern,
delete previous bot comments in a prior step using the GitHub API.

**uv runners:** ``uv`` is not pre-installed on GitHub-hosted runners.
Add ``astral-sh/setup-uv@v5`` and ``uv sync`` as steps before the
action. ``use_uv`` and ``use_poetry`` cannot both be ``true`` — the
action will exit with an error before pytest runs if both are set.

**Rerun compatibility:** ``pytest-rerunfailures`` works transparently —
the JSON report and step outputs reflect the final state after all
retries have been exhausted.

--------------

License
-------

MIT