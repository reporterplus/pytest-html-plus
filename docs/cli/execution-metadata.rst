Version Control & Environment Metadata (``--git-branch``, ``--git-commit``, ``--env``, --rp-env, --environment)
=======================================================================================

These flags allow you to inject version control and environment metadata directly into
your test execution report. This is particularly useful for CI/CD integrations, manual test
runs, or ensuring traceability when Git information is not automatically detectable.

Flags Overview
--------------

- ``--git-branch``
  Specifies the Git branch name to display in the report.
  **Default:** ``NA``
  **Accepted Values:** Any string (e.g., ``main``, ``feature/login-ui``)
  Useful when running tests manually or in CI systems that do not automatically expose a branch name.

- ``--git-commit``
  Specifies the Git commit SHA to display in the report.
  **Default:** ``NA``
  **Accepted Values:** Any valid commit hash (e.g., ``5bb4c87e9da4ff1780540b25a04725ade5c3bc37``)
  Helps ensure full traceability of test runs, especially in detached HEAD mode.

-  ``--env`` and ``--environment`` are **not owned or defined by pytest-html-plus**.
  If these options are already provided by your test suite, plugins, or CI setup,
  pytest-html-plus will capture and display their values in the report metadata
  when they are available.

  If your project does **not** define ``--env`` or ``--environment`` and you want
  to explicitly add environment context (for example ``staging``, ``production``,
  ``BUILD_ID``, or a CI job identifier), use ``--rp-env``, which is **owned and fully
  supported by pytest-html-plus**.

Usage Examples
--------------

**Specify branch and commit explicitly:**

.. code-block:: bash

   pytest --git-branch main --git-commit 5bb4c87

**Include a CI environment variable in the metadata:**

.. code-block:: bash

   pytest --env BUILD_ID
   pytest --environment BUILD_ID
   pytest --rp-env BUILD_ID

If ``BUILD_ID`` is set in your environment, the report will include:


**Combine all three flags for complete control:**

.. code-block:: bash

   export REPORT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
   export REPORT_COMMIT="$(git rev-parse HEAD)"

   pytest --git-branch "$REPORT_BRANCH" --git-commit "$REPORT_COMMIT"
          --env CI_JOB_ID

Use Cases
---------

- **CI/CD Pipelines**
  Pass branch, commit, or pipeline identifiers directly into your reports for accurate mapping
  of test runs to code snapshots.

- **Manual Test Execution**
  Useful when running tests outside a Git repository, inside a Docker container, or from
  distributed artifacts where Git metadata may be unavailable.

- **Build & Release Tracking**
  Supply values like ``BUILD_ID``, ``RUN_NUMBER``, or ``PIPELINE_ID`` so downstream systems
  can correlate test results with deployments.

Report Contents
---------------

- When supplied, branch and commit information will be added to the report header.
- The value of the environment variable provided through ``--env`` or ``--environment`` or ``--rp-env`` will appear as a key/value
  entry under execution metadata.
- If the given environment variable does not exist, its value will be shown as ``NA``.

Important Notes
---------------

- If not provided, both ``--git-branch`` and ``--git-commit`` default to ``NA``.
- The ``--env`` or ``--environment`` or ``--rp-env`` flag accepts **only one environment variable key per usage**.
  If you need to include multiple variables, specify the flag multiple times.
- Avoid using ``--env`` or ``--environment`` or ``--rp-env`` to expose sensitive information such as API tokens or passwords.
