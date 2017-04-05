import requests, json
import traceback

def getTopHeadline(category,config):
    #Get the API Key from the config file and create the URL with the category and key.
    apikey = config["NYTimes"]["api_key"]
    url = "https://api.nytimes.com/svc/topstories/v2/"+category+".json?api-key="+apikey
    #use requests to get and parse the JSON data.
    r = requests.get(url)
    json_raw = r.text
    try:
        json_data = json.loads(json_raw)
    except:
        print("Something went wrong. \n\n\n"+json_raw)
        return False
    ##Return the top headline.
    try:
        return str(json_data["results"][0]["title"].encode("ascii","ignore").decode("ascii","ignore"))
    except:
        print("Something went wrong. \n\n\n"+json_raw)
        traceback.print_exc()
    return False

def readInput(message,config):
    messageSplit = message.lower().split()
    if messageSplit[1] == "headline":
        if len(messageSplit)<3:
            return "Usage: news headline <category>. Reply 'news categories' for a list of categories."
        text = getTopHeadline(messageSplit[2],config)
        return text
    elif messageSplit[1]=="categories":
        return "Categories: home, opinion, world, national, politics, upshot, nyregion, business, technology, science, health, sports, arts, books, movies, theater, sundayreview, fashion, tmagazine, food, travel, magazine, realestate, automobiles, obituaries, insider"
    
