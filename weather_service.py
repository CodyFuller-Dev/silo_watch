#deals with all information tied to the weather API

#gets macos tools
import os
#allows python to use urls aka web browser of sorts
import requests
#lets python look for the .env file to pull secret information from
from dotenv import load_dotenv

#tells python to go into the file in the macos op sys. This also assigns the real key to api_key
load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

########################################################################################################################

#this defines a function instead of a variable. as it goes though the function it morphs. 
#first you call out what city-->
#then it adds the secret sauce from url API key-->
#phone call goes out to openweather-->
#openweather picks up and sends you the kitchen sink-->
#digs though the file cabnint looking for the "main" folder, finds it then pulls out the humidity number-->
#so proud gives you the number
def take_humidity(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"

    response = requests.get(url)

    data = response.json()

    humidity = data['main']['humidity']

    return humidity

########################################################################################################################

#pretty output message with the noice \n for a line break
print("Humidity Check \n _________________")
#THIS is the ignition for all that code from the middle. it turns into one button that runs it all. Like putting a quarter in a pop machine 
report = take_humidity("Charleston,IL,US")
#gives the number provided by the report
print(report)