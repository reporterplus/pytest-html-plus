import pytest

from pytest_html_plus.send_email_report import send_email_from_env, load_email_env
from unittest.mock import patch, MagicMock

@patch("smtplib.SMTP")
def test_send_email_success(mock_smtp, tmp_path):
    report_dir = tmp_path / "report_output"
    report_dir.mkdir()
    report_file = report_dir / "report.html"
    report_file.write_text("<h1>Test Report</h1>")

    config = {
        "sender_email": "sender@example.com",
        "recipient_email": "recipient@example.com",
        "report_path": str(report_dir),
        "subject": "Test Subject",
        "smtp_server": "smtp.sendgrid.net",
        "smtp_port": "587",
        "email_password": "SG.fakekeyforunittesting"
    }

    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    send_email_from_env(config)

    mock_smtp.assert_called_with("smtp.sendgrid.net", 587)
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with("apikey", "SG.fakekeyforunittesting")
    mock_server.send_message.assert_called_once()


@patch("smtplib.SMTP")
def test_invalid_sendgrid_key_warning(mock_smtp, capsys, tmp_path):
    report_dir = tmp_path / "report_output"
    report_dir.mkdir()
    (report_dir / "report.html").write_text("test")

    config = {
        "sender_email": "sender@example.com",
        "recipient_email": "recipient@example.com",
        "report_path": str(report_dir),
        "subject": "Invalid Key Test",
        "smtp_server": "smtp.sendgrid.net",
        "smtp_port": "587",
        "email_password": "not_sendgrid_key"
    }

    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    send_email_from_env(config)
    captured = capsys.readouterr()
    assert "SendGrid API key looks invalid" in captured.out


def test_load_email_env_file_not_found():
    with pytest.raises(FileNotFoundError, match="emailenv file not found!"):
        load_email_env("non_existent_file.env")


from unittest import mock

def test_send_email_handles_exception(tmp_path):
    report_dir = tmp_path / "report_output"
    report_dir.mkdir()
    (report_dir / "report.html").write_text("<html><body>Fake report</body></html>")

    config = {
        "sender_email": "test@example.com",
        "recipient_email": "recipient@example.com",
        "report_path": str(report_dir),
        "subject": "Test Report",
        "smtp_server": "smtp.sendgrid.net",
        "smtp_port": "587",
        "email_password": "SG.fakekey"
    }

    with mock.patch("smtplib.SMTP", side_effect=Exception("SMTP Error")):
        with pytest.raises(RuntimeError, match="Failed to send email: SMTP Error"):
            send_email_from_env(config)


def test_warns_on_invalid_sendgrid_key(tmp_path):
    report_dir = tmp_path / "report_output"
    report_dir.mkdir()
    (report_dir / "report.html").write_text("<html><body>Hi</body></html>")

    config = {
        "sender_email": "me@example.com",
        "recipient_email": "you@example.com",
        "report_path": str(report_dir),
        "subject": "Fake Subject",
        "smtp_server": "smtp.sendgrid.net",
        "smtp_port": "587",
        "email_password": "INVALID_KEY"
    }

    with mock.patch("smtplib.SMTP", side_effect=Exception("SMTP failed")):
        with pytest.raises(RuntimeError, match="Failed to send email: SMTP failed"):
            send_email_from_env(config)


def test_load_email_env_parses_file_correctly(tmp_path):
    env_file = tmp_path / "emailenv"
    env_file.write_text("sender_email=me@example.com\nrecipient_email=you@example.com\n")

    config = load_email_env(str(env_file))

    assert config["sender_email"] == "me@example.com"
    assert config["recipient_email"] == "you@example.com"
