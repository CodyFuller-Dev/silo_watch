import logging
import sys
import os
# tells the application to bring in the flask component, jsonify, and render_template
from flask import Flask, jsonify, render_template

# tells the program to go get the send alert called out in the if statements
from notification_service import send_notification

# tells the script where in the project to look for the variable needed
from weather_service import take_humidity

# tells flask where to look for the website files. Use __name__ only to keep
# from confusing things.
# It automatically stores the name of the current file aka app.py
app = Flask(__name__)

# tells the application to disregard the default way of sorting. This allows
# for my json to be displayed on the webpage as I see fit.
# note this is called out as potentially problematic in some of the documents.
# If I encounter some bugs here would be a good place to start.
app.json.sort_keys = False

# starts all the logging information, gives a timestamp I can read what the
# level is and message as well as creates a log file
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


# this shoots the user right to the correct URL with no guess work
@app.route('/')
def home():
    # this looks for index.html inside the templates folder
    return render_template('index.html')


# this defines what goes at the end of self hosted url to return what we are looking for
@app.route('/silo-humidity')
def city_wrapper():
    city = "Charleston,IL,US"
    # current_humidity is just a placeholder name so that we can call
    # take_humidity from the weather service mod and pass the "city" to it
    current_humidity = take_humidity(city)

    # when the API is called up and no data is returned for what ever reason an
    # error message is sent
    if current_humidity is None:
        error_msg = "CRITICAL: Sensor Offline. Manual Data Reading Required!"
        logger.error(f"Weather API failure: {error_msg}")
        send_notification(error_msg)
        return jsonify({"status": "Error", "message": error_msg}), 500

    # if the humidity is 51% or greater a directive is sent
    if current_humidity >= 51:
        logger.warning(
            f"Threshold Broken: Humidity at {current_humidity}%. Firing Alert Email"
        )
        send_notification(current_humidity)
    # this allows for an all clear baseline message to be broadcast
    else:
        logger.info(f"Status Check: \n Humidity is {current_humidity}%. \n No action required.")

    # this actually displays all the data in listed format for the dashboard to use
    return jsonify({
        "humidity": current_humidity,
        "location": "Grain Silo North",
        "humidistat_sensor_status": "Active"
    })


# this makes it so you need to start app.py directly and not if it is imported
# somewhere else in a different project module.
if __name__ == '__main__':
    # this is the website starting portion. Using PORT keeps cloud and local runs aligned.
    port = int(os.environ.get('PORT', 5001))

    # run the app, listening on all interfaces and on the correct port
    app.run(debug=True, host='0.0.0.0', port=port)
