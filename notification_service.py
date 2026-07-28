import smtplib
import ssl
import os
import logging

# Set up the logger
logger = logging.getLogger(__name__)

def send_notification(humidity_value):
    sender_email = os.getenv("MY_GMAIL")
    receiver_email = os.getenv("MY_GMAIL")
    password = os.getenv("GMAIL_PASS")

    # Laying out the structure of the email 
    subject = "North Silo Alert [!] HIGH HUMIDITY DETECTED"
    body = f"Warning: North Grain Silo humidity is {humidity_value}% \n Turn on Bin Dryer NOW"
    message = f"Subject: {subject}\n\n{body}"

    # Use STARTTLS over port 587 (The standard allowed port for Google Cloud Run)
    try:
        # 1. Connect over standard SMTP port 587
        server = smtplib.SMTP("smtp.gmail.com", 587)
        # 2. Start the secure TLS tunnel (STARTTLS)
        context = ssl.create_default_context()
        server.starttls(context=context)
        # 3. Login and send!
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        
        # Log success so you know it worked!
        logger.info("Email sent successfully to operator.")
        
    except Exception as e:
        # Log the exact error as an ERROR so it shows up in your filtered logs
        logger.error(f"SMTP FAILED - Gmail rejected the connection: {e}")
