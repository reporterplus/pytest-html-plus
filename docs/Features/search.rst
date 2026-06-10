# Universal Test Search + Smart Traceability

The `pytest-html-plus` report includes a powerful search bar that instantly filters tests as you type, helping you quickly locate failures, trace coverage, and navigate linked references.

## Search and Navigate

Simply start typing, and the dashboard will filter tests in real time based on:

✅ **Test names**

✅ **Linked external IDs** — such as JIRA, Testmo, Notion, or any quoted references you attach (for example `JIRA-123`, `DOC-456`, etc.)

✅ **Custom URLs or keywords** — any meaningful text or link in associated references will be indexed

✅ **Error messages and trace snippets** — quickly find tests sharing similar failures, assertion messages, or exception types

.. tip::

This smart search helps you **trace coverage**, **group tests by external references**, and **identify related failures** with ease.

## Examples

* Search `JIRA-123` to display all tests linked to that issue.
* Search `TimeoutError` to locate tests failing due to timeouts.
* Search `NoSuchElementException` to identify Selenium or Playwright locator failures.
* Search `expected 200` to find API assertions with matching error messages.

This makes it easy to investigate patterns, correlate failures, and navigate large reports efficiently.
