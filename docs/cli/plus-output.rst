Captured Output (``--plus-output``)
===================================

The ``--plus-output`` option controls whether captured stdout and stderr are
included in generated JSON, HTML, and XML reports. It can reduce artifact size
for suites where passing tests produce large amounts of output.

Modes
-----

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Behavior
   * - ``all``
     - Include stdout and stderr for every reported test. This is the default.
   * - ``failed-only``
     - Include stdout and stderr only for failed tests and setup/teardown errors.
   * - ``none``
     - Do not include captured stdout or stderr in generated reports.

Command-line usage
------------------

.. code-block:: bash

   pytest --plus-output=failed-only

Profile configuration
---------------------

The policy can also be included in a reusable profile:

.. code-block:: toml

   [tool.pytest-html-plus.profiles.ci]
   output = "failed-only"

Then activate it with:

.. code-block:: bash

   pytest --plus-profile=ci

An explicit ``--plus-output`` value overrides the selected profile. The
default value is ``all`` when neither a CLI option nor a profile is supplied.

Retry information
-----------------

This option controls only the top-level ``stdout`` and ``stderr`` fields. Retry
attempt status, error, and trace information remains unchanged. Individual
attempts do not store stdout or stderr.
