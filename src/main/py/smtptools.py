#!/usr/bin/env python3
# Expected to work with python2 also but using "3" for development...

import configparser
import os
import smtplib
# import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_config_parser():
    config_file = os.path.abspath(__file__).replace("src/main/py/smtptools.py", "meteo.ini")
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return config_parser


def send(receiver_address, subject_line, mail_content):
    config = get_config_parser()

    # The mail addresses and password
    smtp_server = config.get("SMTP", "server", fallback="smtp.gmail.com")  # default value for SMTP server
    smtp_port = int(config.get("SMTP", "port", fallback=587))  # default value for SMTP server port
    sender_address = config.get("SMTP", "sender_address", fallback="Sender.Username@gmail.com")
    sender_name = config.get("SMTP", "sender_name", fallback=None)
    sender_pass = config.get("SMTP", "sender_pass",
                             fallback="Sender address and password should be defined in meteo.ini")
    # print("DEBUG - SMTP to " + sender_address + " at " + smtp_server + ":" + smtp_port)
    if sender_name is None:
        sender_name = sender_address
    else:
        sender_name = sender_name + " <" + sender_address + ">"

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_name
    message['To'] = receiver_address
    message['Subject'] = subject_line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP(smtp_server, smtp_port)
    session.starttls()  # enable security
    try:
        session.login(sender_address, sender_pass)  # login with mail_id and password
    except smtplib.SMTPAuthenticationError:
        print("Failed to connect with user '" + sender_address + "', check configuration file meteo.ini")
        # traceback.print_exc()
        return
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print("Mail '" + subject_line + "' sent to " + receiver_address)


if __name__ == "__main__":
    send(
        get_config_parser().get("SMTP", "receiver_address", fallback="Recipient.Username@gmail.com"),
        "A test mail sent by Python. It has an attachment.",
        '''Hello,
        This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
        Thank You'''
    )
