import requests
import os
from dotenv import load_dotenv
from datetime import datetime

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
        "desc": weather_code_description(values.get('weatherCode'))  # You can map this later
    }
    
def get_forecast(location, days=3):
    url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&units=imperial&apikey={API_KEY}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print("Forecast weather error:", res.text)
        return None

    # Grab the first day’s forecast (today or tomorrow)
    json_data = res.json()
    daily_data=json_data.get("timelines",{}).get("daily", [])
    forecast = []
    
    for day in daily_data[:days]:
        values = day.get("values", {})
        date = datetime.strptime(day["time"], "%Y-%m-%dT%H:%M:%SZ").strftime("%a %b %d")
        
        entry = {
            "date": date,
            "temp_min": values.get("temperatureMin"),
            "temp_max": values.get("temperatureMax"),
            "precip": values.get("precipitationProbabilityAvg"),
            "code": values.get("weatherCodeMax"),
            "desc": weather_code_description(values.get("weatherCodeMax"))
        }
        forecast.append(entry)

        
    return forecast
    
def weather_code_description(code):
    code_map = {
      0: "Unknown",
      1000: "Clear, Sunny",
      1100: "Mostly Clear",
      1101: "Partly Cloudy",
      1102: "Mostly Cloudy",
      1001: "Cloudy",
      2000: "Fog",
      2100: "Light Fog",
      4000: "Drizzle",
      4001: "Rain",
      4200: "Light Rain",
      4201: "Heavy Rain",
      5000: "Snow",
      5001: "Flurries",
      5100: "Light Snow",
      5101: "Heavy Snow",
      6000: "Freezing Drizzle",
      6001: "Freezing Rain",
      6200: "Light Freezing Rain",
      6201: "Heavy Freezing Rain",
      7000: "Ice Pellets",
      7101: "Heavy Ice Pellets",
      7102: "Light Ice Pellets",
      8000: "Thunderstorm"
    }
    return code_map.get(code, f"Unknown ({code})")   