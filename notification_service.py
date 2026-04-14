#this deals with sending the email alert to the operator

#smtplib = anything email related
#ssl = privacy layer
#os= mac os system layer
#.env=secrets file

import smtplib
import ssl
import os
from dotenv import load_dotenv

#tells python to go into the file in the macos op sys
load_dotenv()


def send_notification(current_humidity):
#this is the block to start an email. Here I am using the same TO: and FROM: but usually these would be different
    sender_email = os.getenv("MY_GMAIL")
    receiver_email = os.getenv("MY_GMAIL")
    password = os.getenv("GMAIL_PASS")


#laying out the structure of the email 
    subject = "North Silo Alert [!] HIGH HUMIDITY DETECTED"
    body = f"Warning: North Grain Silo humidity is {current_humidity}% \n Turn on Bin Dryer NOW"
    message = f"Subject: {subject}\n\n{body}"

#test
