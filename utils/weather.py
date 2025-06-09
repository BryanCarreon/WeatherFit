import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY= os.getenv("TOMORROW_API_KEY")

HEADERS = {
    "accept": "application/json",
    "accept-encoding": "deflate, gzip, br"
}

def get_weather_now(location):
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&units=imperial&apikey={API_KEY}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print("Realtime weather error:", res.text)
        return None

    values = res.json()["data"]["values"]
    return {
        "temp": f"{values['temperature']}°F",
        "desc": f"Code {values['weatherCode']}"  # You can map this later
    }
    
def get_forecast(location):
    url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&units=imperial&apikey={API_KEY}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print("Forecast weather error:", res.text)
        return None

    # Grab the first day’s forecast (today or tomorrow)
    daily = res.json()["timelines"]["daily"][0]
    values = daily["values"]
    return {
        "temp_min": f"{values.get('temperatureMin', 'N/A')}°F",
        "temp_max": f"{values.get('temperatureMax', 'N/A')}°F",
        "desc": f"Code {values.get('weatherCode', 'Unavailable')}"
    }