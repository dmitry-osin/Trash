#!/usr/bin/env python
import smtplib
mail_server = 'smtp.acidnation.ru'
mail_server_port = 465
 
from_addr = 'justz@acidnation.ru'
to_addr = 'admin@acidnation.ru'
 
from_header = 'From: %s\r\n' % from_addr
to_header = 'To: %s\r\n\r\n' % to_addr
subject_header = 'Subject: Testing SMTP Authentication'
 
body = 'This mail tests SMTP Authentication'
 
email_message = '%s\n%s\n%s\n\n%s' % (from_header, to_header, subject_header, body)
 
s = smtplib.SMTP(mail_server, mail_server_port)
s.set_debuglevel(1)
s.starttls()
s.login("fatalbert", "mysecretpassword")
s.sendmail(from_addr, to_addr, email_message)
s.quit()