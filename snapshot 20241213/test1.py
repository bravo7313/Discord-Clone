import smtplib

s = smtplib.SMTP('smtp.gmail.com',587)
s.starttls()

s.login("testservermail7@gmail.com","poft zgfg cilj bzud")

otp=548565

message=MIMEMultipart()
        message['From']="testservermail7@gmail.com"
        message['To']=atharva332004@gmail.com
        message['Subject']="NO REPLY, OTP FOR DISCORD CLONE"

        message_body=f"Your OTP for Discord Clone is {otp}"

        message.attach(MIMEText(message_body,'plain'))

        msg=message.as_string()

s.sendmail("testservermail7@gmail.com","atharva332004@gmail.com",message)
print("sending OTP")

s.quit()
