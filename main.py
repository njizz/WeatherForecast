import requests
from datetime import datetime
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv("config.env")

OWM_ENDPOINT = os.getenv("OWM_ENDPOINT")
API_KEY = os.getenv("API_KEY")
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
MY_LAT = 51.49  # Your latitude
MY_LONG = -2.61  # Your longitude

time_now = datetime.now()

parameters = {
        "lat": MY_LAT,
        "lon": MY_LONG,
        "exclude": "current,daily,minutely",
        "appid": API_KEY,
    }

response = requests.get(OWM_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()
weather_slice = data['hourly'][:12]

will_rain = False
for hour_data in weather_slice:
    condition_code = hour_data['weather'][0]['id']
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
            body="It's going to rain today. Remember to bring an ☔",
            from_=os.getenv("SENDER"),
            to=os.getenv("RECEIVER")
        )

    print(message.status)


next_12_hrs_weather = {f"{time_now.hour + i}:00": "".join([weather for weather in data['hourly'][i]['weather'][0]['main']]) for i in range(12)}
if 'Rain' in next_12_hrs_weather.values():
    print("Bring an umbrella")

