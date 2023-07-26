import smtplib

import email.message

from email.mime.text import MIMEText

def sendEmail(email_content, receiver_email, subject):

    server = smtplib.SMTP('smtp.gmail.com: 587')

    msg = email.message.Message()

    msg['Subject'] = subject

    msg['From'] = 'redofs01@gmail.com'

    recipients=['Nicolas.Ravetti@personal.com.py', 'ravetti66@gmail.com']

    msg['To'] = ','.join(recipients)

    password = "sqvqkdvsmoqdkjmv"

    msg.add_header('Content-Type', 'text/html')
    email_content = email_content.encode('ascii', 'ignore').decode('ascii')

    msg.set_payload(email_content)
   

    s = smtplib.SMTP('smtp.gmail.com', port='587')

    s.starttls()

    # Login Credentials for sending the mail

    s.login(msg['From'], password)

    s.sendmail(msg['From'], recipients, msg.as_string())

    s.quit()