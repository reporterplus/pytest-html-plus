Similar errors
==============

Similar Errors is enabled by default and identifies matching final error
messages. Disable it with ``pytest --plus-similar-errors=false`` or TOML:

.. code-block:: toml

   [tool.pytest-html-plus]
   similar_errors = false

Named profiles also accept ``similar_errors = true`` or ``false``. Explicit CLI values take
precedence over profile values, which take precedence over the top-level setting.

Matching behavior and limitations
---------------------------------

After worker aggregation, failed and error results are grouped by exception type
and normalized message. Passed (including flaky), skipped, xfailed and xpassed
results are excluded. Retry attempts do not increase counts.

Matching describes similar messages, not shared root causes. It is deterministic and
conservative: exception summaries must contain a useful message; ANSI formatting,
whitespace and hexadecimal addresses in ``object at 0x...`` representations are
normalized. Other hexadecimal identifiers, such as transaction IDs, remain distinct. Paths, numbers and
meaningful message differences are preserved. Identical messages with different
worker or installation paths remain separate; this intentionally favors missed
matches over grouping unrelated failures. Bare exception types and context-free
timeout messages do not form groups. Tracebacks
and retry history are not used as fallback signals, so some equivalent failures
will remain unmatched. No external services or new runtime dependencies are used.

Badge and navigation
--------------------

A transparent badge after the worker shows a layers icon and the number of other matching tests,
excluding the current test. For a count of 3, its tooltip is
``3 tests with similar failure messages`` and its accessible label is
``Show 3 tests with similar failure messages``. Click it to open links; links
reuse the report's existing expand, reveal, scroll and highlight behavior, clearing
active filters/search. Escape closes the popover and returns focus to its badge.
Clicking outside, moving focus outside, or navigating also closes it.

Sharing links
-------------

The copy-link icon in the popover header copies every test in the group, including
the current test, in group order, with each test included once. The output is
plain text: each entry contains the displayed test name, a space, an em dash,
another space, and its individual deep-link URL. Entries are separated by a
newline (``\n``), not commas. Newlines within test names become spaces.
For example (illustrative anchors):

.. code-block:: text

   test_login — https://ci.example.com/report.html?run=42#test-abc
   test_checkout — https://ci.example.com/report.html?run=42#test-def

These are the same individual links used by the test cell's copy-link button;
no group-level URL is created. Existing query parameters are preserved and the
fragment is replaced with the destination test's anchor. Opening a copied link
uses the existing reveal, expand, scroll, and highlight behavior for one test.

The icon briefly shows a check mark on success or a cross if clipboard
access is unavailable or denied, matching individual link copying. Its tooltip
explains that all tests in the group are included. Copying leaves the popover open
and does not navigate. Recipients need access to the same report;
local ``file://`` links point to the sender's machine and are not shareable as-is.
The clipboard text is built only when clicked, without additional group metadata.

JSON metadata
-------------

JSON consumers can read ``similar_error_group`` on matched results and
``similar_error_groups`` at report level. Each group contains ``message`` and a
``nodeids`` list, stored once. IDs are local to the report. Disabled runs add no
metadata and perform no fingerprinting. Direct Python merger calls remain opt-in: pass
``merge_json_reports(..., similar_errors=True)`` for JSON-only generation; this
checkout does not provide a ``--plus-no-html`` option.

Developer reference
-------------------

See :ref:`similar-errors-development` for intentional-failure demos and retry
lifecycle setup, and :ref:`similar-errors-benchmarks` for the full historical
measurements, methodology, limitations, and reproduction command.
