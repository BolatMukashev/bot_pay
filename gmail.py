#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version
import config


server = 'smtp.gmail.com'
sender = 'pdd.good.bot@gmail.com'

if config.DEBUG:
    password = config.GMAIL_WINDOWS_PASSWORD
else:
    password = config.GMAIL_LINUX_PASSWORD


file_path = "documents/site_preview.pdf"
base_name = os.path.basename(file_path)
file_size = os.path.getsize(file_path)

title = 'PDD GOOD BOT'
my_message = 'Прочти обязательно!'


def send_emails_to_schools(recipients_list, sub_title, html):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = sub_title
    msg['From'] = title
    msg['To'] = ', '.join(recipients_list)
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(my_message, 'plain')
    part_html = MIMEText(html, 'html')
    part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(base_name))
    part_file.set_payload(open(file_path, "rb").read())
    part_file.add_header('Content-Description', base_name)
    part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(base_name, file_size))
    encoders.encode_base64(part_file)

    msg.attach(part_text)
    msg.attach(part_html)
    msg.attach(part_file)

    mail = smtplib.SMTP_SSL(server)
    mail.login(sender, password)
    try:
        mail.sendmail(sender, recipients_list, msg.as_string())
        return 'Сообщения в автошколы были разосланы...'
    except smtplib.SMTPRecipientsRefused:
        return 'Список email-ов пуст'
    finally:
        mail.quit()
