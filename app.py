import logging
import sys
import os
# tells the application to bring in the flask component, jsonify, and the NEW render_template
from flask import Flask, jsonify, render_template

# tells the program to go get the send alert called out in the if statements 
from notification_service import send_notification

# tells the script where in the project to look for the variable needed
from weather_service import take_humidity

# tells flask where to look for the website files.
app = Flask(__name__)

# tells the application to disregard the default way of sorting.
app.json.sort_keys = False

# starts all the logging information, gives a timestamp I can read what the level is and message as well as creates a log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

logger.info("========================================================")
logger.info(" Silo Watch Program Initialized ")
logger.info("=======================================================")

# ==========================================================================
# ROUTE 1: Serves the HTML Dashboard on the main URL
# ==========================================================================
@app.route('/')
def home():
    # This looks for index.html inside your new 'templates' folder
    return render_template('index.html')

# ==========================================================================
# ROUTE 2: Provides the JSON data for the dashboard's JavaScript
# ==========================================================================
@app.route('/silo-humidity')
def city_wrapper():
    city = "Charleston,IL,US"
    # current_humidity is just a placeholder name so that we can call take_humidity from the weather service mod and pass the "city" to it
    current_humidity = take_humidity(city)
    
    # when the API is called up and no data is returned for what ever reason an error message is sent
    if current_humidity is None:
        error_msg = "CRITICAL: Sensor Offline. Manual Data Reading Required!"
        logger.error(f"Weather API failure: {error_msg}")
        send_notification(error_msg)
        return jsonify({"status": "Error", "message": error_msg}), 500

    # if the humidity is 51% or greater a directive is sent
    if current_humidity >= 51:
        alert_msg = f"WARNING: Humidity is {current_humidity}%. Please start bin dryer IMMEDIATELY"
        logger.warning(f"Threshold Broken: Humidity at {current_humidity}%. Firing Alert Email")
        send_notification(current_humidity)
    # this allows for an all clear baseline message to be broadcast
    else:
        logger.info(f"Status Check: \n Humidity is {current_humidity}%. \n No action required.")

    # this actually returns the JSON data that your dashboard's JavaScript will use
    return jsonify({
        "humidity" : current_humidity,
        "location" : "Grain Silo North",
        "humidistat_sensor_status" : "Active"
    })

# ==========================================================================
# This is the correct startup logic for Cloud Run
# ==========================================================================
if __name__ == '__main__':
    # Get the port number from the environment variable PORT
    # Default to 5001 if the environment variable is not set (for local testing)
    port = int(os.environ.get('PORT', 5001))
    
    # Run the app, listening on all interfaces and on the correct port
    app.run(debug=True, host='0.0.0.0', port=port)

#test gpush