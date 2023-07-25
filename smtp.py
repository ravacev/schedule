import smtplib 
from email.message import EmailMessage 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(email_message):

    email_subject = "Email test from Python" 
    sender_email_address = "redofs01@gmail.com" 
    receiver_email_address = "ravetti66@gmail.com" 
    email_smtp = "smtp.gmail.com" 
    email_password = "sqvqkdvsmoqdkjmv" 

    # Create an email message object 
    message = EmailMessage() 

    # Configure email headers 
    message['Subject'] = email_subject 
    message['From'] = sender_email_address 
    message['To'] = receiver_email_address 

    # Set email body text 
    message.set_content(email_message)
    message.attach()

    # Set smtp server and port 
    server = smtplib.SMTP(email_smtp, '587') 

    # Identify this client to the SMTP server 
    server.ehlo() 

    # Secure the SMTP connection 
    server.starttls() 

    # Login to email account 
    server.login(sender_email_address, email_password) 

    # Send email 
    server.send_message(message)

    # Close connection to server 
    server.quit()