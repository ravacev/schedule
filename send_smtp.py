import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Send mail for schedule
# Values that will not be changed
smtp_server = '10.11.11.50'  # Replace with your SMTP server address
smtp_port = 25  # Replace with the appropriate SMTP port (587 is commonly used for TLS)
sender_email = 'agenda@personal.com.py'  # Replace with your email address

def sendEmail(body, receiver_email, subject):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ','.join(receiver_email)
    msg['Subject'] = subject

    # Add the UTF-8 encoded body to the email
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    try:
        # Establish a connection to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:

            # Send the email
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")