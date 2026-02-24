Contributing
============

We welcome pull requests, issues, and feature suggestions from the community.
Please take a moment to review this guide and our `Code of Conduct <code_of_conduct.html>`_ before contributing.

Setting Up the Project
----------------------

**Prerequisites:** Docker must be installed on your machine.

.. code-block:: bash

   make build-dev   # build the dev container (includes dev dependencies)

That's it. All development happens inside the container — no need to manage Python versions or Poetry locally.

Useful commands:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Command
     - Description
   * - ``make build-dev``
     - Build the dev Docker image
   * - ``make test``
     - Run the full test suite
   * - ``make lint``
     - Check for lint errors (ruff)
   * - ``make fix``
     - Auto-fix lint and formatting issues
   * - ``make shell``
     - Drop into the container for debugging

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