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
user = 'pdd.good.bot@gmail.com'
if config.DEBUG:
    password = config.GMAIL_WINDOWS_PASSWORD
else:
    password = config.GMAIL_LINUX_PASSWORD

recipients = ['ya.ne.angel.kimi@gmail.com', 'm-bolat@mail.ru']
sender = user
subject = 'Тема сообщения'
text = 'Текст сообщения'

html_message = [
    '<html><head></head><body>',
    '<p>' + text + '</p>',
    '<p><img src="https://avatarko.ru/img/kartinka/33/multfilm_lyagushka_32117.jpg" alt="Письма мастера дзен"></p>',
    '</body></html>'
]

html = ''.join(html_message)
filepath = "Kazakhstan_gory_2.jpg"
basename = os.path.basename(filepath)
filesize = os.path.getsize(filepath)

msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = 'PDD GOOD BOT'
msg['To'] = ', '.join(recipients)
msg['Reply-To'] = sender
msg['Return-Path'] = sender
msg['X-Mailer'] = 'Python/' + (python_version())

part_text = MIMEText(text, 'plain')
part_html = MIMEText(html, 'html')
part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
part_file.set_payload(open(filepath, "rb").read())
part_file.add_header('Content-Description', basename)
part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
encoders.encode_base64(part_file)

msg.attach(part_text)
msg.attach(part_html)
msg.attach(part_file)

mail = smtplib.SMTP_SSL(server)
mail.login(user, password)
mail.sendmail(sender, recipients, msg.as_string())
mail.quit()
