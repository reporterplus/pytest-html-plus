Email the HTML Report (`--send-email`)
======================================

The `--plus-send-email` flag allows you to automatically send the generated HTML test report via email. This is useful for test pipelines that need to share results with team members or stakeholders without manually downloading and forwarding reports.

SendGrid Setup Required
-----------------------

To use this feature, you must configure your own **SendGrid SMTP** account.

Steps to Set Up
---------------

1. **Create an `emailenv` File**

   In your project directory, create a file named `emailenv` with the following content:

   .. code-block:: bash

      sender_email=you@example.com
      recipient_email=team@example.com
      subject=Your Test Report
      smtp_server=smtp.sendgrid.net
      smtp_port=587
      email_password=your_sendgrid_api_key

   - `sender_email`: The email address used to send the report.
   - `recipient_email`: Comma-separated list of recipients.
   - `subject`: Subject line of the email.
   - `smtp_server`: Must be `smtp.sendgrid.net`
   - `smtp_port`: Typically `587` for TLS
   - `email_password`: Your SendGrid API key (used as SMTP password)

2. **Run Pytest with the Email Flag**

   .. code-block:: bash

      pytest --plus-send-email

   This will:
   - Generate the test report (requires `--html-output`)
   - Send the report to the recipients listed

Requirements
------------

- To use this feature, you must configure your own **SendGrid SMTP** account.
- The test framework will automatically read the `emailenv` file from the root directory.

Attachments
-----------

- `index.html` (HTML report)
- If `--capture-screenshots` is enabled, screenshots will be zipped and attached.

Use Cases
---------

- CI pipelines (nightly, regression, release runs)
- Teams who want automated test report delivery
- Scenarios where testers or leads need to review without pipeline access. All they need to do is download and extract the zip to view the highly actionable single page pytest-html-plus report

.. warning::

   Do **not** commit your `emailenv` file to version control. It contains sensitive credentials.
