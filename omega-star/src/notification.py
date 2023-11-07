from os import environ
import smtplib
from email.message import EmailMessage


def send_email(sender: str, to: str, subject: str, contents: str):
    email_user = environ.get("EMAIL_USER")
    email_pass = environ.get("EMAIL_PASS")

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.set_content(contents)

    server = smtplib.SMTP('172.17.0.1', 1025)
    server.login(email_user, email_pass)
    server.send_message(msg)
    server.quit()
