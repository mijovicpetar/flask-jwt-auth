"""Email service."""

import smtplib
import traceback

from flask import current_app, render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:
    """Email service."""

    @classmethod
    def send_email(cls, receiver_email: str, subject: str, msg: str) -> bool:
        """Send email to receiver email address.

        Args:
            receiver_email (str): Target email.
            msg (str): Email content.

        Returns:
            bool: True if success, False otherwise.
        """
        return True
        # try:
        #     smtp_server = current_app.config["SMTP_EMAIL_SERVER"]
        #     sender_email = current_app.config["SENDER_EMAIL_ADDRESS"]
        #     sender_password = current_app.config["SENDER_EMAIL_PASS"]

        #     message = 'Subject: {}\n\n{}'.format(subject, msg)

        #     mail_server = smtplib.SMTP_SSL(smtp_server , 465)
        #     mail_server.login(sender_email , sender_password)
        #     mail_server.sendmail(sender_email, receiver_email, message)
        #     mail_server.quit()

        #     return True
        # except:
        #     traceback.print_exc()
        #     return False

    @classmethod
    def send_template_email(cls, receiver_email, subject, template_name, data):
        return True
        # try:
        #     smtp_server = current_app.config["SMTP_EMAIL_SERVER"]
        #     sender_email = current_app.config["SENDER_EMAIL_ADDRESS"]
        #     sender_password = current_app.config["SENDER_EMAIL_PASS"]

        #     msg = MIMEMultipart('alternative')
        #     msg['Subject'] = subject
        #     msg['From'] = sender_email
        #     msg['To'] = receiver_email

        #     text = subject # here we should insert the text from the template, but it will work anyways
        #     html = render_template(template_name, data=data)

        #     part1 = MIMEText(text, 'plain', 'utf-8')
        #     part2 = MIMEText(html, 'html', 'utf-8')

        #     msg.attach(part1)
        #     msg.attach(part2)

        #     mail_server = smtplib.SMTP_SSL(smtp_server , 465)
        #     mail_server.login(sender_email , sender_password)
        #     mail_server.sendmail(sender_email, receiver_email, msg.as_string())
        #     mail_server.quit()

        #     print('Email sent')

        #     return True
        # except:
        #     print('Error occured while sending email with template.')
        #     traceback.print_exc()
        #     return False
