import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from twilio.rest import Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Notifier:
    def __init__(self, email_config=None, sms_config=None):
        """
        Initialize the Notifier with email and/or SMS configurations.

        :param email_config: Dictionary containing email configuration (optional)
        :param sms_config: Dictionary containing SMS configuration (optional)
        """
        self.email_config = email_config
        self.sms_config = sms_config
        logger.info("Notifier initialized")

    def send_email(self, to_address, subject, body, attachments=None):
        """
        Send an email notification.

        :param to_address: Recipient email address
        :param subject: Email subject
        :param body: Email body
        :param attachments: List of file paths to attach (optional)
        """
        if not self.email_config:
            logger.error("Email configuration not provided")
            return

        msg = MIMEMultipart()
        msg['From'] = self.email_config['from_address']
        msg['To'] = to_address
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        for attachment in attachments or []:
            try:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(attachment, 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={attachment}')
                msg.attach(part)
            except Exception as e:
                logger.error(f"Error attaching file {attachment}: {e}")

        try:
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['smtp_user'], self.email_config['smtp_password'])
                server.sendmail(self.email_config['from_address'], to_address, msg.as_string())
            logger.info(f"Email sent to {to_address}")
        except Exception as e:
            logger.error(f"Error sending email: {e}")

    def send_sms(self, to_number, message):
        """
        Send an SMS notification.

        :param to_number: Recipient phone number
        :param message: SMS message
        """
        if not self.sms_config:
            logger.error("SMS configuration not provided")
            return

        try:
            client = Client(self.sms_config['account_sid'], self.sms_config['auth_token'])
            client.messages.create(body=message, from_=self.sms_config['from_number'], to=to_number)
            logger.info(f"SMS sent to {to_number}")
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")

# Example usage:
if __name__ == "__main__":
    email_config = {
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'smtp_user': 'user@example.com',
        'smtp_password': 'password',
        'from_address': 'user@example.com'
    }

    sms_config = {
        'account_sid': 'your_account_sid',
        'auth_token': 'your_auth_token',
        'from_number': '+1234567890'
    }

    notifier = Notifier(email_config=email_config, sms_config=sms_config)

    # Send an email
    notifier.send_email(to_address='recipient@example.com', subject='Test Email', body='This is a test email.')

    # Send an SMS
    notifier.send_sms(to_number='+0987654321', message='This is a test SMS.')
