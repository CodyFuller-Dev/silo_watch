import os
import requests

def take_humidity(city):
    # Fetch the API key right when it is needed
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        # This will show a clear error in your logs if the secret is missing
        raise ValueError("OPENWEATHER_API_KEY environment variable not set.")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    response = requests.get(url)
    data = response.json()
    humidity = data['main']['humidity']
    return humidity
