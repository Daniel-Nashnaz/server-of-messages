import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()


def send_email(recipient_email: str, subject: str, body: str) -> bool:
    """
    Sends an email message to the specified recipient.

    Args:
        recipient_email (str): The email address of the recipient.
        subject (str): The subject line of the email.
        body (str): The body of the email.

    Returns:
        A boolean indicating whether the email was sent successfully.
    """
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = os.environ.get('EMAIL_FROM')
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Add message to container
    msg.attach(MIMEText(body, 'html'))

    try:
        # Connect to SMTP server
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()

        # Login to SMTP server
        server.login(os.environ.get('EMAIL_FROM'), os.environ.get('EMAIL_PASSWORD'))

        # Send email
        server.sendmail(os.environ.get('EMAIL_FROM'), recipient_email, msg.as_string())

        # Close connection to SMTP server
        server.quit()

        return True
    except Exception as e:
        print("Error sending email:", e)
        return False
