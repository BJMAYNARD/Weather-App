import re
import lxml.etree as et
from lxml import etree
import os
import random
import urllib.request
import pip


def install_and_import(lxml):
    import importlib
    try:
        importlib.import_module(lxml)
    except ImportError:
        import pip
        pip.main(['install', lxml])
    finally:
        globals()[lxml] = importlib.import_module(lxml)


install_and_import('lxml')

# Source is National Weather Service: https://w1.weather.gov/xml/current_obs/
# Station ID codes can be found at the source URL, as well as other info about the data

import requests
def getWeather(stationID):
    current_weather = dict()

    # Get current weather data, and exit if there was a problem with the request
    try:
        r = requests.get(
            f"https://w1.weather.gov/xml/current_obs/{stationID}.xml")
    except:
        print("There was a problem with your connection. Are you online?")
        return current_weather

    # Parse out the info. This XML only has a depth of one, so just lift the text contents of each tag into a dictionary
    # If the request wasn't ok, return the status code along with a fail message
    if r.ok:
        page = et.fromstring(r.content)

        for element in page:
            current_weather[element.tag] = element.text
    else:
        print(f"Failed to fetch weather info from site ({r.status_code})")

    # Return weather data
    return current_weather


# Get Station ID from user, validating that the input is in the right format of 4 upper case letters
# Most people do not know the 4 letter code

sid = ''
while not sid:
    sid_input = input(
        "Weather.gov current conditions retriever\nPlease enter a station ID: ").strip().upper()
    if re.match(r'^[A-Z]{4}$', sid_input):
        sid = sid_input
    else:
        print("-"*40)
        print("Station IDs are in the format of 4 letters. Please try again")
        print("Codes can be found at https://w1.weather.gov/xml/current_obs/")
        print("-"*40)

# Calls on the SID and display the results if they were returned

data = getWeather(sid)
if data:
    print("-"*40)
    print(f"Conditions at {data['location']}:")
    print(f"Current temperature is {data['temperature_string']}")
    print(
        f"Humidity is at {data['relative_humidity']}% relative humidity")
    print(
        f"Wind is at {data['wind_string']}")
    print(f"Visability is at {data['visibility_mi']} miles.")
    print(f"Last Updated at {data['observation_time']}.")
