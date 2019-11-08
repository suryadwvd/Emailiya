import time
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_user = 'yourusername@gmail.com'
with open('Contents.txt' , 'r')as c:

    subject = c.readline()
    body = c.read()

msg = MIMEMultipart()
msg['From'] = email_user
msg['Subject'] = subject

msg.attach(MIMEText(body , 'plain'))
filename = 'Document.txt'
attachment = open(filename,'rb')

part = MIMEBase('application' , 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition' , "attachment; filename= " + filename)

msg.attach(part)
text = msg.as_string()
c = 0

with open('EmailAccounts.txt' , 'r') as f:
    for line in f:
        msg['To']=line
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user , 'password')

        server.sendmail(email_user , line , text)
        server.quit()
        c+=1
        time.sleep(0.02)
        print(+c+' emails sent.')
