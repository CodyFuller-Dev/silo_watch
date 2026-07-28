import smtplib
import ssl
import os
import logging

# Set up the logger
logger = logging.getLogger(__name__)

def send_notification(humidity_value):
    # Fetch secrets right when they are needed
    sender_email = os.getenv("MY_GMAIL")
    receiver_email = os.getenv("MY_GMAIL")
    password = os.getenv("GMAIL_PASS")

    # Check if any of the required secrets are missing
    if not all([sender_email, receiver_email, password]):
        logger.error("SMTP FAILED: One or more email environment variables (MY_GMAIL, GMAIL_PASS) are not set in the container.")
        return

    # Laying out the structure of the email 
    subject = "North Silo Alert [!] HIGH HUMIDITY DETECTED"
    body = f"Warning: North Grain Silo humidity is {humidity_value}% \n Turn on Bin Dryer NOW"
    message = f"Subject: {subject}\n\n{body}"

    # Use STARTTLS over port 587
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        logger.info("Email sent successfully to operator.")
        
    except Exception as e:
        logger.error(f"SMTP FAILED - Gmail rejected the connection: {e}")

