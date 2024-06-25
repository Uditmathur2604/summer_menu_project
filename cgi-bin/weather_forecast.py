#!/usr/bin/env python3

import cgi
import cgitb
import json
import requests

# Enable CGI traceback for debugging
cgitb.enable()

# Print necessary headers
print("Content-Type: application/json\n")

# Parse the query parameters
form = cgi.FieldStorage()
city_name = form.getvalue("city")

# OpenWeatherMap API details
API_KEY = '6302c2c8d32da7d084341a3ade731119'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Function to get weather data
def get_weather(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "City not found"}

# Get weather for the provided city
weather_data = get_weather(city_name)

# Output the result as JSON
print(json.dumps(weather_data))
