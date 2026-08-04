import os
import requests


def take_humidity(city):
    # deals with all information tied to the weather API
    # fetch the API key right when it is needed
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        # this gives a clear failure message if the secret is missing
        raise ValueError("OPENWEATHER_API_KEY environment variable not set.")

    # build API call -> fetch payload -> pull humidity from main block
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    response = requests.get(url)
    data = response.json()
    humidity = data['main']['humidity']
    return humidity
