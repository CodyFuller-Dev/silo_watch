# this is a unit test for app.py
# importing as app_module because the flask app object could get confused if
# just using app
import app as app_module

# this defines the name of the test being preformed
# it tells pytest with the test_ desigation
# it tells a human with the _returns_dashboard


def test_home_route_returns_dashboard():

    # top down view this is creating a fake browser from the flask app and
    # storing it in a variable named client
    # app_module is the building blueprint
    # app_module.app is the legit building
    # test _client() is the vistior pass
    # client is the guy actually holding that pass
    client = app_module.app.test_client()

    # this line actually tests the rout to the dashboard
    # the fake browser (client) sends a http Get request though the fake
    # browser then returns a status code below and stores it in "responce"
    # the / is routing it directly to the homepage of the app
    response = client.get("/")

    # the asert means if the status code dose not return a 200 the test is a
    # failure
    # checks the physical page to confirm it really looks like what it is
    # expected to be by checking the title of the website
    assert response.status_code == 200
    assert b"<title>Silo Watch</title>" in response.data
    # ####### this ends the first test

# this starts out a new test that checks if the standard sensor reading of (ok)
# returns normal json
# monkeypatch swaps out the real function for a test only item that way actual
# api calls are not made
# this sets the attribute of take_humidity to the test only item of 52 if the
# test works the resuly will always be 52


def test_silo_humidity_returns_json_when_sensor_ok(monkeypatch):
    monkeypatch.setattr(app_module, "take_humidity", lambda city: 52)

    # the first line is a tempory storage box to put all the send_notification
    # data in durring the test
    # this changes from sending an email to storing a value
    # if the sensor is reading ok then it saves the value of 52 to the storage
    # box if not it not 52 it gets failed out below
    sent = {}
    monkeypatch.setattr(
        app_module,
        "send_notification",
        lambda value: sent.setdefault("value", value),
    )

    # this is like the above
    # this reaching out to silo-humidity and then saves the responce
    # this one is testing for if humidity is 52
    client = app_module.app.test_client()
    response = client.get("/silo-humidity")

    # this block is for checking the the json value returned from the page
    # matches exactally
    # also looking for the status code of 200
    # and if the value is 52
    assert response.status_code == 200
    assert response.get_json() == {
        "humidity": 52,
        "location": "Grain Silo North",
        "humidistat_sensor_status": "Active",
    }
    assert sent["value"] == 52
    # ####### this ends the second test

# this test focuses on the error side of the test
# swaps the known good 52 for a none value to simulate a breakage of the senson or api failure


def test_silo_humidity_returns_error_when_sensor_offline(monkeypatch):
    monkeypatch.setattr(app_module, "take_humidity", lambda city: None)

    # this is like above where it sets up temp box
    # this is testing if the error messages that need to happen if the sensor
    # is offline or if the value is out of spec
    # it takes those values and stores them in the temp box
    sent = {}
    monkeypatch.setattr(
        app_module,
        "send_notification",
        lambda value: sent.setdefault("value", value),
    )

    # this reaching out to silo-humidity and then saves the responce
    # this one is testing for if humidity value returned is none
    client = app_module.app.test_client()
    response = client.get("/silo-humidity")

    # this is checking for if the responce code is bad aka 500
    # confirms that the error message json from the silo-humidity is the actual
    # json message returned
    # confirms that the error message needing sent is the correct one
    assert response.status_code == 500
    assert response.get_json() == {
        "status": "Error",
        "message": "CRITICAL: Sensor Offline. Manual Data Reading Required!",
    }
    assert sent["value"] == "CRITICAL: Sensor Offline. Manual Data Reading Required!"
