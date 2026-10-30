Similar errors
==============

Similar Errors is enabled by default and identifies matching final error
messages. Disable it with ``pytest --plus-similar-errors=false`` or TOML:

.. code-block:: toml

   [tool.pytest-html-plus]
   similar_errors = false

Named profiles also accept ``similar_errors = true`` or ``false``. Explicit CLI values take
precedence over profile values, which take precedence over the top-level setting.

After worker aggregation, failed and error results are grouped by exception type
and normalized message. Passed (including flaky), skipped, xfailed and xpassed
results are excluded. Retry attempts do not increase counts. A transparent badge
after the worker shows a layers icon and the number of other matching tests,
excluding the current test. For a count of 3, its tooltip is
``3 tests with similar failure messages`` and its accessible label is
``Show 3 tests with similar failure messages``. Click it to open links; links
reuse the report's existing expand, reveal, scroll and highlight behavior, clearing
active filters/search. Escape closes the popover and returns focus to its badge.
Clicking outside, moving focus outside, or navigating also closes it.

Sharing links
-------------

The copy-link icon in the popover header copies every test in the group, including
the current test, in group order. Each line contains the test name followed by
its individual deep-link URL. Existing query parameters are preserved and the
fragment is replaced with the destination test's anchor. Opening a copied link
uses the existing reveal, expand, scroll, and highlight behavior for one test.

The icon briefly shows a check mark on success or a cross if clipboard
access is unavailable or denied, matching individual link copying. Its tooltip
explains that all tests in the group are included. Copying leaves the popover open
and does not navigate. Recipients need access to the same report;
local ``file://`` links point to the sender's machine and are not shareable as-is.
The clipboard text is built only when clicked, without additional group metadata.

JSON metadata and matching
--------------------------

JSON consumers can read ``similar_error_group`` on matched results and
``similar_error_groups`` at report level. Each group contains ``message`` and a
``nodeids`` list, stored once. IDs are local to the report. Disabled runs add no
metadata and perform no fingerprinting. Direct Python merger calls remain opt-in: pass
``merge_json_reports(..., similar_errors=True)`` for JSON-only generation; this
checkout does not provide a ``--plus-no-html`` option.

Matching describes similar messages, not shared root causes. It is intentionally
conservative: exception summaries must contain a useful message; ANSI formatting,
whitespace and hexadecimal addresses in ``object at 0x...`` representations are
normalized. Other hexadecimal identifiers, such as transaction IDs, remain distinct. Paths, numbers and
meaningful message differences are preserved. Identical messages with different
worker or installation paths remain separate; this intentionally favors missed
matches over grouping unrelated failures. Bare exception types and context-free
timeout messages do not form groups. Tracebacks
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

Benchmarks
----------

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
