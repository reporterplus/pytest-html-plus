Share a Direct Link to a Test
=============================

Each test in the HTML report has a stable link that can be copied and shared.
The link opens the report at that test, making it easier for teammates to
investigate a specific result without searching through the full run.

Copying a test link
-------------------

Select the **Copy link to test** button beside the test node ID. The copied URL
contains the current report address and a test-specific fragment:

.. code-block:: text

   https://reports.example.com/build-842/index.html#test-a13f...

When the link is opened, the report:

* reveals the test if report filters would otherwise hide it;
* expands its details;
* scrolls the test into view; and
* applies a subtle highlight so the referenced result is easy to identify.

The link does not change the test result or the report data.

Sharing a hosted report
-----------------------

Upload the generated report to a CI artifact service, internal web server, or
other location that serves it as HTML. Open the hosted report and use its
**Copy link to test** button. This ensures the copied link contains the hosted
address rather than a local ``file://`` path.

The ``#test-...`` part of the URL is processed by JavaScript in the report. It
is not sent to the hosting server, and pytest-html-plus does not require a
reporting backend or any additional service.

For recipients to use the link:

* they must be able to access the hosted report;
* the host must serve the report as HTML instead of forcing a download;
* the report must remain available at the shared address; and
* any authentication or redirect flow should preserve the URL fragment.

If authentication is required, the recipient may need to sign in before the
report opens. Access remains controlled entirely by the service hosting the
report.

Link stability
--------------

The test fragment is derived deterministically from the pytest node ID. Links
remain stable when the same test appears in another generated report with the
same node ID. If the test is renamed, moved in a way that changes its node ID,
or absent from the shared report, that report cannot navigate to the original
test.

.. note::

   A link copied from a locally opened report points to that local file and
   normally cannot be opened by another person. Host the report first, then
   copy the test link from the hosted version.
