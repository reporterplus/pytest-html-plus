Contributing
============

We welcome pull requests, issues, and feature suggestions from the community.
Before contributing, please take a moment to review our contribution guidelines and code of conduct.

Setting Up the Project
-----------------------

Setting up the project is pretty simple:

.. code-block:: bash

    docker build -t pytest-html-plus .
    docker run -it pytest-html-plus /bin/bash
    poetry run pytest tests/ --reruns 1

Branching & PR Policy
---------------------

We use **version branches** for releases. Each published release has its own branch,
and **all new PRs must target the *next* upcoming version branch**.

- If the **current released version** is ``0.4.0``, your PR’s **base branch** should be ``0.4.1``.
- Can’t find the upcoming branch (e.g., ``0.4.1``)? **Open an issue** asking us to create it.
- We follow **Semantic Versioning**:

  - ``MAJOR`` (breaking) → e.g., ``1.0.0``
  - ``MINOR`` (features, backwards-compatible) → e.g., ``0.5.0``
  - ``PATCH`` (fixes, docs, perf) → e.g., ``0.4.1``

PR Checklist
~~~~~~~~~~~~

- Target the correct **upcoming version branch** (not ``main``).
- Add/adjust **tests** for new behavior.
- Run the test suite locally
- Update **README / docs** if user-facing behavior changes.
- Add a short **changelog entry** (under the upcoming version).

Release Flow (for maintainers)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Merge PRs into the upcoming version branch (e.g., ``0.4.1``).
- When ready, tag and publish from that branch, then create the next branch (e.g., ``0.4.2``).