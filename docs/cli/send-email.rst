Emailing the HTML Report
========================

Send your generated HTML report automatically by email after a test run.
No code changes are required — just provide your email settings once.

Quick Start
-----------

1. **Create an ``emailenv`` file** at your project root (this is required):

   .. code-block:: none

      EMAIL_SENDER=qa-bot@example.com
      EMAIL_RECIPIENT=team@example.com
      EMAIL_SUBJECT=Automated Test Report
      SMTP_SERVER=smtp.office365.com or your own smtp server
      SMTP_PORT=587
      EMAIL_PASSWORD=your_smtp_or_app_password
      EMAIL_USE_TLS=true

   .. note::

      If using **SendGrid**, set:

      .. code-block:: none

         SMTP_SERVER=smtp.sendgrid.net
         SMTP_PORT=587
         EMAIL_PASSWORD=your_sendgrid_api_key   # must start with SG.
         EMAIL_SENDER=qa-bot@example.com
         EMAIL_RECIPIENT=team@example.com
         EMAIL_SUBJECT=Automated Test Report

      For SendGrid, the username is always ``apikey`` (no changes needed in the file).

2. **Run pytest** with email sending enabled:

   .. code-block:: bash

      pytest --plus-send-email

The plugin will zip your report folder and email it to the recipient.

Configuration
-------------

``emailenv`` file (mandatory)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Place an ``emailenv`` file in the project root with the following keys:

- ``EMAIL_SENDER`` – From address (e.g., ``qa-bot@example.com``)
- ``EMAIL_RECIPIENT`` – To address (single or comma-separated)
- ``EMAIL_SUBJECT`` – Subject line
- ``SMTP_SERVER`` – SMTP host (e.g., ``smtp.gmail.com``, ``smtp.office365.com``, ``smtp.sendgrid.net``)
- ``SMTP_PORT`` – SMTP port (usually ``587`` for TLS or ``465`` for SSL)
- ``EMAIL_PASSWORD`` – SMTP/App password or SendGrid API key
- ``EMAIL_USE_TLS`` – ``true``/``false`` (default: ``true``)
- ``use_ssl`` – ``true``/``false`` (default: ``false``; set ``true`` for port 465 setups)

Provider Notes
--------------

- **Gmail:** use an **App Password**; server ``smtp.gmail.com``, port ``587``, TLS on.
- **Microsoft 365/Outlook:** ``smtp.office365.com``, port ``587``, TLS on.
- **SendGrid:** ``smtp.sendgrid.net``, port ``587``, username ``apikey``, password is your API key (starts with ``SG.``).
- **Generic SMTP:** use the host/port provided by your IT; toggle TLS/SSL to match.

Common Questions
----------------

**Do I need to change my tests?**
No — just create the ``emailenv`` file and run with ``--plus-send-email``.

**What gets sent?**
A **zipped** copy of your HTML report output folder.

**Multiple recipients?**
Use a comma-separated list in ``EMAIL_RECIPIENT``.

**Matrix builds (multiple Python versions)?**
Add the version to your subject in ``EMAIL_SUBJECT`` to avoid confusion.

Troubleshooting
---------------

- **Authentication errors:** for Gmail, use an app password; for SendGrid, ensure your API key starts with ``SG.``.
- **TLS/SSL errors:** switch between ``EMAIL_USE_TLS=true`` (port 587) and ``use_ssl=true`` (port 465) per provider docs.
- **No email received:** check spam/junk folders, verify addresses, and ensure your CI allows outbound SMTP.
