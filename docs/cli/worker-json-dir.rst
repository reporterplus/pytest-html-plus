Worker JSON Directory (`--worker-json-dir`)
===========================================

The `--worker-json-dir` flag defines where pytest-xdist workers write their partial JSON reports. After the run, the controller merges these files into the final report under `--html-output`.

Overview
--------

- **Default**: `.pytest_worker_jsons`
- **Type**: Directory path, relative to the current working directory or absolute
- **Usage Context**: Parallel runs with `pytest -n`, read-only file systems

Example
-------

.. code-block:: bash

   pytest -n auto --worker-json-dir=/tmp/pytest-worker-jsons

Read-only Containers
--------------------

In containers with a read-only root file system (for example Kubernetes pods with ``readOnlyRootFilesystem: true``), the default directory cannot be created in the test root. Point every directory the plugin writes to at a writable volume:

.. code-block:: bash

   pytest -n auto \
     --worker-json-dir=/tmp/pytest-html-plus/worker-jsons \
     --html-output=/tmp/pytest-html-plus/report \
     --screenshots=/tmp/pytest-html-plus/screenshots

.. note::

   The flag only has an effect when tests run with pytest-xdist. Without `-n`, no worker files are written.
