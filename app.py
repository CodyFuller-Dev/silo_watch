import logging
import sys
import os

#tells the application to bring in the flask component as well as the jsonify component
from flask import Flask, jsonify, redirect, url_for

#tells the program to go get the send alert called out in the if statements 
from notification_service import send_notification

#tells the script where in the project to look for the variable needed
from weather_service import take_humidity

#tells flask where to look for the website files. Use __name__ only to keep from confusing things. It automatically stores the name of the current file aka app.py
app = Flask(__name__)

#tells the application to disregard the default way of sorting. This allows for my json to be displayed on the webpage as I see fit. 
#note this is called out as potentially problematic in some of the documents. If I encounter some bugs here would be a good place to start.
app.json.sort_keys = False

#starts all the logging information, gives a timestamp I can read what the level is and message as well as creates a log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

logger.info("========================================================")
logger.info(" Silo Watch Program Initialized ")
logger.info(" Navigate to http://127.0.0.1:5001/silo to view status " )
logger.info("=======================================================")

#this shoots the user right to the correct URL with no guess work
@app.route('/')
def index():
    return redirect(url_for('city_wrapper'))

#this defines what goes at the end of self hosted url to return what we are looking for
@app.route('/silo')

#struggled with this, def XX I am just wrapping the variable "city" in a define so I can call it up later. 
def city_wrapper():
    city = "Charleston,IL,US"

#current_humidity is just a placeholder name so that we can call take_humidity from the weather service mod and pass the "city" to it
    current_humidity = take_humidity(city)
    #when the API is called up and no data is returned for what ever reason an error message is sent
    if current_humidity is None:
        error_msg = "CRITICAL: Sensor Offline. Manual Data Reading Required!"
        logger.error(f"Weather API failure: {error_msg}")
        send_notification(error_msg)
        return jsonify({"status": "Error", "message": error_msg}), 500

#if the humidity is 51% or greater a directive is sent
    if current_humidity >=10:
        alert_msg = f"WARNING: Humidity is {current_humidity}%. Please start bin dryer IMMEDIATELY"
        logger.warning(f"Threshold Broken: Humidity at {current_humidity}%. Firing Alert Email")
        send_notification(current_humidity)

#this allows for an all clear baseline message to be broadcast
    else:
        logger.info(f"Status Check: \n Humidity is {current_humidity}%. \n No action required.")

#this actually displays all the data on the webpage in my specific listed format as allowed from the sort_keys line above
    return jsonify({
        "humidity" : current_humidity,
        "location" : "Grain Silo North",
        "humidistat_sensor_status" : "Active"
    })

#this makes it so you need to start app.py directly and not if it is imported somewhere else in a different project module. 
if __name__ == '__main__' :
    
    #this is the website starting portion, debug lets the browser show the issues as well as restarts the server when new code it saved, port 5000 is the default network port for flask.
    #Updated to include 0.0.0.0 for docker integration 
    # use docker run -p 5001:5000 for the Work Laptop
    app.run(debug=True, host='0.0.0.0', port=5001)
