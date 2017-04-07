##Handle getting the weather from yahoo!

import requests, json


import time

def get_weather(location):
    baseurl = baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+location+'")'
    url = baseurl+"q="+yql_query+"&format=json"
    r = requests.get(url)
    raw = r.text
    json_file = json.loads(raw)
    return json_file

def get_daily_forecasts(json_file):
    outputList = {}
    forecastData = json_file["query"]["results"]["channel"]["item"]["forecast"]
    for i in range(len(forecastData)):
        day = forecastData[i]
        outputList[i] = day["high"]+"/"+day["low"]+" | "+day["text"]
    return outputList

def digestable(json_file):
    # Takes the first day of the forecast and makes it look good for the digest.
    forecastData = json_file["query"]["results"]["channel"]["item"]["forecast"]
    day = forecastData[0]
    output = "The high is "+day["high"]+", the low is "+day["low"]+", and it will be "+day["text"].lower()+"."
    return output

def get_current_temperature(json_file):
    return json_file["query"]["results"]["channel"]["item"]["condition"]["temp"]

def get_sunrise_sunset(location):
    ##Get the weather, get the times.
    json_file = get_weather(location)
    astronomy = json_file["query"]["results"]["channel"]["astronomy"]
    strings = (astronomy["sunrise"],astronomy["sunset"])

    ##strptime has a habit of setting the date to the 1900s. Make a string to adjust.
    adjust = time.strftime("%d %m %Y")
    sunrise = time.strptime(adjust + " "+strings[0],"%d %m %Y %I:%M %p")
    sunset = time.strptime(adjust + " "+strings[1],"%d %m %Y %I:%M %p")
    
    return (sunrise, sunset)

def readInput(message,config):
    messageSplit = message.lower().split()
    location = config["Weather"]["default_location"]
    if messageSplit[1] == "temperature":
        if len(messageSplit)>2:
            location = messageSplit[2]
        w = get_weather(location)
        return get_current_temperature(w)
    if messageSplit[1] == "forecast":
        if len(messageSplit)>2:
            location = messageSplit[2]
        w = get_weather(location)
        forecasts = get_daily_forecasts(w)
        return forecasts[0]
    if messageSplit[1] == "forecasts":
        if len(messageSplit)<3:
            return "Usage: weather forecasts <amount> [location]"
        if len(messageSplit)>3:
            location = messageSplit[3]
        w = get_weather(location)
        amount = 0
        try:
            amount = int(messageSplit[2])
        except:
            return "Please specify an amount."
        if amount > 8 or amount < 2:
            return "Please specify an amount 2-7."
        forecasts = get_daily_forecasts(w)
        outStr = ""
        for i in range(amount):
            outStr += forecasts[i]
            if i!= amount-1:
                outStr += "\n"
        return outStr

