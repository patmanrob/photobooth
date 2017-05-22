#!/usr/bin/env python3

import smtplib
import time
#import pbconf
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
print("Starting Mailer")
fromaddr = "takeyourownphoto@thepatman.co.uk"
toaddr = "rob@eaglesfield.name"
now = time.strftime("%Y-%m-%d-%H-%M-%S")
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "It's your PhotoBooth Picture!"
body = 'Here is your picture taken at ' + now
msg.attach(MIMEText(body, 'plain'))

filename = "facebook.jpg"
attachment = open("/home/pi/PB_archive/facebook.jpg", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(part)
print("Contacting Server")
server = smtplib.SMTP('auth.smtp.1and1.co.uk', 587)
server.starttls()
server.login("mail@thepatman.co.uk", "5p0ttyd0g")
text = msg.as_string()
print("Sending email")
server.sendmail(fromaddr, toaddr, text)
server.quit()
print("Done eMailing")
 
