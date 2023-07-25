# import datetime as dt
# import time
# import smtplib



# def send_email_at(send_time):
#     print(send_time)   
#     time.sleep(send_time.timestamp() - time.time())
#     print('email sent')

# first_email_time = dt.datetime(2023,7,14,15,59,0) # set your sending time in UTC
# interval = dt.timedelta(minutes=2*60) # set the interval for sending the email



# while True:
#     send_email_at(first_email_time+interval)
#     send_time = first_email_time + interval
#     print(send_time)