import os
import smtplib
from email.message import EmailMessage
from pytest_html_plus.utils import zip_report_folder


class EmailSender:
    def __init__(self, config: dict, report_path=None):
        self.sender = config.get("EMAIL_SENDER") or os.getenv("EMAIL_FROM")
        self.recipient = config.get("EMAIL_RECIPIENT") or os.getenv("EMAIL_TO")
        self.subject = config.get("EMAIL_SUBJECT")
        self.report_path = report_path
        self.smtp_server = config.get("SMTP_SERVER") or os.getenv("SMTP_HOST")
        self.smtp_port = int(config.get("SMTP_PORT") or os.getenv("SMTP_PORT", "587"))
        self.password = config.get("EMAIL_PASSWORD") or os.getenv("SMTP_PASSWORD")
        self.username = config.get("smtp_username") or self.sender or os.getenv("SMTP_USERNAME")
        self.use_tls = str(config.get("EMAIL_USE_TLS", True)).lower() == "true"
        self.use_ssl = str(config.get("use_ssl", False)).lower() == "true"

    def zip_and_attach(self, msg: EmailMessage) -> str:
        zip_path = zip_report_folder(self.report_path, f"{self.report_path}_zipped.zip")
        filename = os.path.basename(zip_path)
        with open(zip_path, "rb") as f:
            report_data = f.read()
        msg.add_attachment(report_data, maintype="application", subtype="zip", filename=filename)
        return filename

    def send(self):
        msg = EmailMessage()
        msg["Subject"] = self.subject
        msg["From"] = self.sender
        msg["To"] = self.recipient
        msg.set_content(self.subject)
        self.zip_and_attach(msg)

        try:
            if "sendgrid" in self.smtp_server.lower():
                self._send_via_sendgrid(msg)
            else:
                self._send_via_smtp(msg)
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {e}") from e

    def _send_via_sendgrid(self, msg: EmailMessage):
        if not self.password.startswith("SG."):
            print("Invalid SendGrid API Key: should start with 'SG.'")
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            if self.use_tls:
                server.starttls()
            server.login("apikey", self.password)
            server.send_message(msg)

    def _send_via_smtp(self, msg: EmailMessage):
        if self.use_ssl:
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        else:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            if self.use_tls:
                server.starttls()
        server.login(self.username, self.password)
        server.send_message(msg)
        server.quit()
