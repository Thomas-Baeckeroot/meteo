#!/usr/bin/env python3
# Expected to work with python2 also but using "3" for development...

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(receiver_address, subject_line, mail_content):
    # The mail addresses and password
    smtp_server = "smtp.gmail.com"  # default value for SMTP server
    smtp_port = 587  # default value for SMTP server port
    sender_address = "Sender.Username@gmail.com"  # Should be overwritten in smtp.account.config.py
    sender_pass = "Sender address and password should be defined in non-committed file smtp.account.config.py."
    exec(open(os.path.dirname(os.path.abspath(__file__)) + "/smtp.account.config.py").read())

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject_line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP(smtp_server, smtp_port)
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print("Mail Sent")


if __name__ == "__main__":
    mail_content = '''Hello,
    This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
    Thank You
    '''

    send(receiver_address="Recipient.Username@gmail.com",
         subject_line="A test mail sent by Python. It has an attachment.",
         mail_content=mail_content
         )
