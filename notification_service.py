#this deals with sending the email alert to the operator

#smtplib = anything email related
#ssl = privacy layer
#os= os system layer now very important since this is on the mac and my work laptop
#.env=secrets file
#W_S lets me pull the actual humidity fetch function from the other module 

import smtplib
import ssl
import os
import weather_service
from dotenv import load_dotenv

#tells python to go into the file in the macos op sys
load_dotenv()


#this is the container that holds the entire emailing function
def send_notification(humidity_value):
#this is the block to start an email. Here I am using the same TO: and FROM: but usually these would be different
    sender_email = os.getenv("MY_GMAIL")
    receiver_email = os.getenv("MY_GMAIL")
    password = os.getenv("GMAIL_PASS")


#laying out the structure of the email 
    subject = "North Silo Alert [!] HIGH HUMIDITY DETECTED"
    body = f"Warning: North Grain Silo humidity is {humidity_value}% \n Turn on Bin Dryer NOW"
    message = f"Subject: {subject}\n\n{body}"


#this is the encryption layer basically a secure tunnel end to end 
    context = ssl.create_default_context()

#this block grabs the ssl protocol and uses port 465 sends over the user and pass allowing the email to actually be sent off. Then gives a response if it worked 
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully")
        
        #this along with the above helps keep the whole program from straight up crashing. Gives it a soft off ramp of sorts
    except Exception as e:
      print(f"Something went wrong: {e}")


