Contributing
============

We welcome pull requests, issues, and feature suggestions from the community.
Please take a moment to review this guide and our `Code of Conduct <code_of_conduct.html>`_ before contributing.

Setting Up the Project
----------------------

**Prerequisites:** Docker must be installed on your machine.

.. code-block:: bash

   make build-with-dev-dependencies   # build the dev container (includes dev dependencies)

That's it. All development happens inside the container — no need to manage Python versions or Poetry locally.

Useful commands:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Command
     - Description
   * - ``make build-with-dev-dependencies``
     - Build the dev Docker image
   * - ``make test``
     - Run the full test suite
   * - ``make lint``
     - Check for lint errors (ruff)
   * - ``make fix``
     - Auto-fix lint and formatting issues
   * - ``make shell``
     - Drop into the container for debugging

.. _similar-errors-development:

Similar Errors development
--------------------------

See :doc:`Features/similar-errors` for configuration, matching behavior, and
report navigation. The following demos intentionally fail and are for manual
inspection only.

Preview with intentional failures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The intentional-failure demos are commented out by default. For manual badge
inspection, first uncomment the marked block in
``tests/dummy_tests/demo_similar_errors.py``, then run the Docker demo:

.. code-block:: bash

   make demo-similar-errors

Open ``report_output_similar_errors/report.html``. Four matching failures display
a layers icon with **3** each; two matching setup errors display a layers icon
with **1** each. An unrelated failure and a passing test have no badge. Click a badge to
navigate to another matching test.

The enabled demo exits with a nonzero status by design. Comment the block out
again after inspection. Automated feature coverage remains active in
``tests/unit/test_similar_errors.py`` and
``tests/unit/test_similar_errors_copy_links.py``.

For setup, call, and teardown retry scenarios, the separately commented demo in
``tests/unit/test_similar_errors_retry_lifecycle.py`` includes its own enable/run
instructions. Do not leave it enabled in the normal unit suite.

To run the basic demo directly in your Python environment after uncommenting it:

.. code-block:: bash

   pytest tests/dummy_tests/demo_similar_errors.py --plus-similar-errors=true --html-output=report_output_similar_errors

.. _similar-errors-benchmarks:

Historical benchmarks
~~~~~~~~~~~~~~~~~~~~~

Measured on 2026-10-27 using macOS ARM64 (Darwin 25.4.0), Python 3.14.4.
These historical HTML sizes predate the layers icon and group-copy control;
rerun the benchmark below to measure the current report output.
The dataset mixes identical assertions, unrelated errors, object memory-address
variants, and long Playwright messages with varying executable paths. Two
matching groups contain 50% of the tests; differing executable paths remain
separate. Full messages are processed without a Playwright-specific shortcut.

.. list-table:: Additional cost of similarity analysis
   :header-rows: 1

   * - Failed tests
     - Enabled (ms)
     - Disabled (ms)
     - Added JSON (bytes)
     - Added HTML (bytes)
     - Peak analysis allocations (bytes)
   * - 100
     - 1.964
     - 0.000083
     - 4,369
     - 15,505
     - 100,325
   * - 1,000
     - 21.517
     - 0.000167
     - 42,169
     - 122,205
     - 839,048
   * - 10,000
     - 202.230
     - 0.000459
     - 424,669
     - 1,198,205
     - 8,422,081

Times are medians of seven runs of the post-processing stage, excluding fixture
copying, aggregation, serialization, and HTML generation. Disabled timing measures
only the skipped conditional; no fingerprints are computed. These sub-microsecond
values reflect timer and branch overhead, not total report-generation time.

Size increases compare actual UTF-8 output with and without similarity metadata
and badges; JSON uses the merger's two-space indentation. Memory is peak Python
allocation measured separately with ``tracemalloc`` during analysis, excluding
the input report. It is not total process memory (RSS).

Group membership is stored once in each output format. HTML also adds a button
per matched test; popover links are created only when opened. Large groups can
still take time to render. These measurements do not benchmark browser interaction
or establish performance on other hardware.

Reproduce from the repository root:

.. code-block:: bash

   poetry run python -m benchmarks.similar_errors

Branching & PR Policy
---------------------

We use version branches for releases. Each published release has its own branch,
and all new PRs must target the **next upcoming version branch** — never ``main``.

**Example:**

- Current released version is ``0.4.0``
- Your PR's base branch should be ``0.4.1``

Can't find the upcoming branch? Open an issue asking us to create it.

Semantic Versioning
-------------------

We follow `Semantic Versioning <https://semver.org>`_:

.. list-table::
   :widths: 20 30 50
   :header-rows: 1

   * - Type
     - Example
     - When to use
   * - ``PATCH``
     - ``0.4.1``
     - Bug fixes, docs, performance improvements
   * - ``MINOR``
     - ``0.5.0``
     - New features, backwards-compatible changes
   * - ``MAJOR``
     - ``1.0.0``
     - Breaking changes

PR Checklist
------------

Before submitting your PR, make sure you've done the following:

**Branch**

- PR is targeting the correct upcoming version branch (e.g. ``0.4.1``), not ``main``

**Code**

- Ran ``make lint`` with no errors
- Ran ``make test`` and all tests pass
- Added or updated tests for any new or changed behavior

**Docs**

- Updated README if user-facing behavior changed
- Updated this documentation if applicable

**Changelog**

- Added a short entry under the upcoming version in ``CHANGELOG.md``

**General**

- PR description explains *what* changed and *why*
- Linked the related issue using ``Closes #123`` (if one exists)

Release Flow (Maintainers Only)
--------------------------------

.. note::
   This section is for maintainers only. External contributors do not need to worry about this.

1. Merge approved PRs into the upcoming version branch (e.g. ``0.4.1``)
2. Run the full test suite one final time: ``make test``
3. Tag and publish the release from that branch
4. Create the next upcoming version branch (e.g. ``0.4.2``) immediately after

Questions?
----------

Open an issue or start a `Discussion <https://github.com/reporterplus/pytest-html-plus/discussions>`_ on GitHub.