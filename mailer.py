#!/usr/bin/env python3

import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pbconf import(
	archive_path,
	m_fromaddr,
	m_toaddr,
	m_server,
	m_user,
	m_pass
	)
	
print("Starting Mailer")

now = time.strftime("%Y-%m-%d-%H-%M-%S")
msg = MIMEMultipart()
msg['From'] = m_fromaddr
msg['To'] = m_toaddr
msg['Subject'] = "It's your PhotoBooth Picture!"
body = 'Here is your picture taken at ' + now
msg.attach(MIMEText(body, 'plain'))

filename = "photobooth.jpg"
attachment = open(archive_path + "photobooth.jpg", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(part)
print("Contacting Server")
server = smtplib.SMTP(m_server, 587)
server.starttls()
server.login(m_user, m_pass)
text = msg.as_string()
print("Sending email")
server.sendmail(m_fromaddr, m_toaddr, text)
server.quit()
print("Done eMailing")
 
