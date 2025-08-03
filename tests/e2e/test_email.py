from email.message import EmailMessage

import pytest
from unittest.mock import patch, mock_open, MagicMock

from pytest_html_plus.send_email_report import EmailSender

@pytest.fixture
def config():
    return {
        "EMAIL_SENDER": "sender@example.com",
        "EMAIL_RECIPIENT": "recipient@example.com",
        "EMAIL_SUBJECT": "Test Report",
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": 587,
        "EMAIL_PASSWORD": "password",
        "smtp_username": "smtp_user",
        "EMAIL_USE_TLS": True,
        "use_ssl": False
    }


@patch("pytest_html_plus.send_email_report.EmailSender.zip_and_attach")
@patch("smtplib.SMTP")
def test_send_with_smtp(mock_smtp, mock_zip, config):
    mock_server = MagicMock()
    mock_smtp.return_value = mock_server
    mock_zip.return_value = "dummy.zip"

    sender = EmailSender(config, report_path="/fake/path")
    sender.send()

    mock_smtp.assert_called_with("smtp.example.com", 587)
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with("smtp_user", "password")
    mock_server.send_message.assert_called_once()
    mock_server.quit.assert_called_once()

@patch("pytest_html_plus.send_email_report.EmailSender.zip_and_attach")
@patch("smtplib.SMTP_SSL")
def test_send_with_ssl(mock_ssl, mock_zip, config):
    config["use_ssl"] = True
    mock_server = MagicMock()
    mock_ssl.return_value = mock_server
    mock_zip.return_value = "dummy.zip"

    sender = EmailSender(config, report_path="/fake/path")
    sender.send()

    mock_ssl.assert_called_with("smtp.example.com", 587)
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()
    mock_server.quit.assert_called_once()

