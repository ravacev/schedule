import smtplib
import email.message

from smtplib import SMTPException


def sendEmail(email_content):
    
    msg = email.message.Message()

    msg['Subject'] = 'Agenda OFS'

    msg['From'] = 'agenda@personal.com.py'

    recipients=["AgendayConfirmacion@personal.com.py","InternetCorporativo@personal.com.py",
                "MesadeayudaDEC@personal.com.py","OPERADORES_DE_HOJA_DE_RUTA@personal.com.py",
                "OPERADORES_DE_SOPORTE@personal.com.py","CC_INTERNET@personal.com.py",
                "Soluciones_Tecnologicas@personal.com.py","OFS_Red@personal.com.py"]

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