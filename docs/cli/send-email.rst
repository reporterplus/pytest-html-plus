Email the HTML Report (`--send-email`)
======================================

The `--plus-email` flag allows you to automatically send the generated HTML test report via email. This is useful for test pipelines that need to share results with team members or stakeholders without manually downloading and forwarding reports.

SMTP Setup Required
-----------------------

To use this feature, you must configure your own **SMTP** account and TEMPORARY APP_PASSWORD of your email account.

Steps to Set Up
---------------

1. **Create an `emailenv` File**

   In your project directory, create a file named `emailenv` with the following content:

   .. code-block:: bash

        SMTP_SERVER=smtp.gmail.com
        SMTP_PORT=587
        EMAIL_USE_TLS=true
        EMAIL_SENDER=your@example.com
        EMAIL_PASSWORD=***************
        EMAIL_RECIPIENT=your@example.com
        EMAIL_SUBJECT=Your Report from SMTP


   - `EMAIL_SENDER`: The email address used to send the report.
   - `EMAIL_RECIPIENT`: The email address to who the report is to be sent.
   - `EMAIL_SUBJECT`: Subject line of the email.
   - `SMTP_SERVER`: Must be `smtp.gmail.net` or server of your email provider
   - `SMTP_PORT`: Typically `587` for TLS
   - `EMAIL_PASSWORD`: Your temporary password provided by your email service (used as SMTP password)

2. **Run Pytest with the Email Flag**

   .. code-block:: bash

      pytest --plus-email

   This will:
   - Generate the test report (requires `--html-output`)
   - Send the report to the recipients listed

Requirements
------------

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
