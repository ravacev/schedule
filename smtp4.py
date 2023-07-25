import smtplib
from smtplib import SMTPException

import email.message

def sendEmail(email_content, values, sender):
    
    msg = email.message.Message()

    msg['Subject'] = f'Caso transferido a {values["team"]}. OT: {values["id_ot"]}, Ticket: {values["num_ticket"]}'

    msg['From'] = 'agenda@personal.com.py'

    recipients=[sender['Email']]

    msg['To'] = ','.join(recipients)

    msg.add_header('Content-Type', 'text/html')

    email_content = email_content.encode('ascii', 'ignore').decode('ascii')

    msg.set_payload(email_content)
    
    try:
        smtpObj = smtplib.SMTP('10.11.11.50', 25)
        smtpObj.sendmail(msg['From'], recipients, msg.as_string())
        print ("Successfully sent email")
    except SMTPException:
        print ("Error: unable to send email")