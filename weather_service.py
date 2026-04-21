#deals with all information tied to the weather API

#gets current os tools
import os
#allows python to use urls aka web browser of sorts
import requests
#lets python look for the .env file to pull secret information from
from dotenv import load_dotenv

#tells python to go into the file in the macos op sys. This also assigns the real key to api_key
load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")


#this defines a function instead of a variable. as it goes though the function it morphs. 
#first you call out what city-->
#then it adds the secret sauce from url API key-->
#phone call goes out to openweather-->
#openweather picks up and sends you the kitchen sink-->
#digs though the file cabinet looking for the "main" folder, finds it then pulls out the humidity number-->
#so proud gives you the number
def take_humidity(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"

    response = requests.get(url)

    data = response.json()

    humidity = data['main']['humidity']

    return humidity
