import smtplib
import ssl
import os
import logging

# this deals with sending the email alert to the operator
# smtplib = anything email related
# ssl = privacy layer
# os = system variables and environment hooks
# logging = tracks what happened when running in docker/cloud
# set up the logger
logger = logging.getLogger(__name__)


def send_notification(humidity_value):
    # this is the block to start an email. Here I am using the same TO and
    # FROM but usually these would be different
    # fetch secrets right when they are needed
    sender_email = os.getenv("MY_GMAIL")
    receiver_email = os.getenv("MY_GMAIL")
    password = os.getenv("GMAIL_PASS")

    # check if any of the required secrets are missing
    if not all([sender_email, receiver_email, password]):
        logger.error(
            "SMTP FAILED: One or more email environment variables "
            "(MY_GMAIL, GMAIL_PASS) are not set in the container."
        )
        return

    # laying out the structure of the email
    subject = "North Silo Alert [!] HIGH HUMIDITY DETECTED"
    body = f"Warning: North Grain Silo humidity is {humidity_value}% \n Turn on Bin Dryer NOW"
    message = f"Subject: {subject}\n\n{body}"

    # this is the secure tunnel layer and send sequence using STARTTLS over
    # port 587
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        logger.info("Email sent successfully to operator.")

    except smtplib.SMTPAuthenticationError as e:
        # soft off-ramp so auth failures do not crash the whole app
        logger.error(f"SMTP Auth failed - password may be expired or revoked: {e}")
    except Exception as e:
        # catch-all for provider rejection, network issues, or unexpected SMTP
        # failures
        logger.error(f"SMTP FAILED - Gmail rejected the connection: {e}")
