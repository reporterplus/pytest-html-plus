Similar errors
==============

Use ``pytest --plus-similar-errors=true`` to identify matching final error
messages. The default is disabled. Explicit ``--plus-similar-errors=false``
overrides TOML configuration:

.. code-block:: toml

   [tool.pytest-html-plus]
   similar_errors = true

Named profiles also accept ``similar_errors = true``. Explicit CLI values take
precedence over profile values, which take precedence over the top-level setting.

After worker aggregation, failed and error results are grouped by exception type
and normalized message. Passed (including flaky), skipped, xfailed and xpassed
results are excluded. Retry attempts do not increase counts. A neutral badge after
the worker shows the number of other matching tests. Click it to open links; links
reuse the report's existing expand, reveal, scroll and highlight behavior, clearing
active filters/search. Escape closes the popover and returns focus to its badge.
Clicking outside, moving focus outside, or navigating also closes it.

JSON consumers can read ``similar_error_group`` on matched results and
``similar_error_groups`` at report level. Each group contains ``message`` and a
``nodeids`` list, stored once. IDs are local to the report. Disabled runs add no
metadata and perform no fingerprinting. The Python merger accepts
``merge_json_reports(..., similar_errors=True)`` for JSON-only generation; this
checkout does not provide a ``--plus-no-html`` option.

Matching describes similar messages, not shared root causes. It is intentionally
conservative: exception summaries must contain a useful message; ANSI formatting,
whitespace, object memory addresses and missing Playwright executable paths are
normalized. Other paths, numbers and message differences are preserved. Tracebacks
and retry history are not used as fallback signals, so some equivalent failures
will remain unmatched. No external services or new runtime dependencies are used.

Preview with intentional failures
---------------------------------

The intentional-failure demos are commented out by default. For manual badge
inspection, first uncomment the marked block in
``tests/dummy_tests/demo_similar_errors.py``, then run the Docker demo:

.. code-block:: bash

   make demo-similar-errors

Open ``report_output_similar_errors/report.html``. Four matching failures display
**3 similar errors** each; two matching setup errors display **1 similar error**
each. An unrelated failure and a passing test have no badge. Click a badge to
navigate to another matching test.

The enabled demo exits with a nonzero status by design. Comment the block out
again after inspection. Automated feature coverage remains active in
``tests/unit/test_similar_errors.py``.

For setup, call, and teardown retry scenarios, the separately commented demo in
``tests/unit/test_similar_errors_retry_lifecycle.py`` includes its own enable/run
instructions. Do not leave it enabled in the normal unit suite.

To run the basic demo directly in your Python environment after uncommenting it:

.. code-block:: bash

   pytest tests/dummy_tests/demo_similar_errors.py --plus-similar-errors=true --html-output=report_output_similar_errors

Benchmarks
----------

Measured on 2026-10-27 using macOS ARM64 (Darwin 25.4.0), Python 3.14.4.
The dataset mixes identical assertions, unrelated errors, object memory-address
variants, and long Playwright messages with varying executable paths. Three
matching groups contain 75% of the tests.

.. list-table:: Additional cost of similarity analysis
   :header-rows: 1

   * - Failed tests
     - Enabled (ms)
     - Disabled (ms)
     - Added JSON (bytes)
     - Added HTML (bytes)
     - Peak analysis allocations (bytes)
   * - 100
     - 0.374
     - 0.000083
     - 6,568
     - 21,399
     - 17,267
   * - 1,000
     - 4.013
     - 0.000084
     - 63,268
     - 186,174
     - 103,867
   * - 10,000
     - 36.700
     - 0.000250
     - 637,018
     - 1,847,424
     - 1,071,047

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
