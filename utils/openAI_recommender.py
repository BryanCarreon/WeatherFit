from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def outfit_recommendation(weather_data: dict):
    weather_str = "\n".join(f"{key}: {value}" for key, value in weather_data.items())
    
    prompt = f"""Based on the following weather data, recommend an outfit to wear. Be brief and consider temperature, humidity, UV index, and rain chance.

Weather data:
{weather_str}

Your response:"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages = [
                {"role": "system", "content": "You help users decide what to wear based on weather."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        ) 
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI Error:", e)
        return "No suggestion available."