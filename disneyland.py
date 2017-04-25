import requests,json

def get_wait_times():
    r = requests.post('https://authorization.go.com/token',data={"grant_type":"assertion","assertion_type":"public","client_id":"WDPRO-MOBILE.MDX.WDW.ANDROID-PROD"})
    json_data = json.loads(r.text)
    access_token = json_data["access_token"]
    
    #Get data for Disneyland.
    r2_d2 = requests.get("https://api.wdpro.disney.go.com/facility-service/theme-parks/330339/wait-times",
                      headers={"Authorization":"BEARER "+access_token,
                               "Accept":"application/json;apiversion=1",
                               "X-Conversation-Id":"WDPRO-MOBILE.MDX.CLIENT-PROD",
                               "X-App-Id":"WDW-MDX-ANDROID-3.4.1"
                               }
                      )
    data = json.loads(r2_d2.text.replace("\xa0",""))
    outDict = {}
    for entry in data["entries"]:
        name = entry["name"]
        wt = entry["waitTime"]
        t = ""
        if wt["status"]=="Closed":
            t = "Closed"
        else:
            if "postedWaitMinutes" in wt:
                outDict[name] = wt["postedWaitMinutes"]
    #Get data for California Adventure.
    c3po = requests.get("https://api.wdpro.disney.go.com/facility-service/theme-parks/336894/wait-times",
                      headers={"Authorization":"BEARER "+access_token,
                               "Accept":"application/json;apiversion=1",
                               "X-Conversation-Id":"WDPRO-MOBILE.MDX.CLIENT-PROD",
                               "X-App-Id":"WDW-MDX-ANDROID-3.4.1"
                               }
                      )
    data = json.loads(c3po.text.replace("\xa0",""))
    for entry in data["entries"]:
        name = entry["name"]
        wt = entry["waitTime"]
        t = ""
        if wt["status"]=="Closed":
            t = "Closed"
        else:
            if "postedWaitMinutes" in wt:
                outDict[name] = wt["postedWaitMinutes"]
    
    return outDict

names = {
        "buzz":"Buzz Lightyear Astro Blasters",
        "thunder":"Big Thunder Mountain Railroad",
        "monorail":"Disneyland Monorail",
        "dumbo":"Dumbo the Flying Elephant",
        "tiki":"Enchanted Tiki Room",
        "nemo":"Finding Nemo Submarine Voyage",
        "gadget":"Gatget's Go Coaster",
        "haunted":"Haunted Mansion",
        "indy":"Indiana Jones Adventure",
        "tea":"Mad Tea Party",
        "toad":"Mr. Toad's Wild Ride",
        "peter":"Peter Pan's Flight",
        "pinocchio":"Pinocchio's Daring Journey",
        "pirates":"Pirates of the Caribbean",
        "space":"Hyperspace Mountain",
        "splash":"Splash Mountain",
        "star":"Star Tours- The Adventures Continue",
        "small":"\"it's a small world\"",
        "alice":"Alice in Wonderland",
        "screamin":"California Screamin'",
        "screaming":"California Screamin'",
        "grizzly":"Grizzly River Run",
        "soarin":"Soarin' Around The World",
        "soaring":"Soarin' Around The World",
        "mania":"Toy Story Midway Mania!",
        "midway":"Toy Story Midway Mania!",
        "racers":"Radiator Springs Racers",
        "sky school":"Goofy's Sky School"
        }

def read_input(message,config):
    messageSplit = message.lower().split()
    if messageSplit[1] == "summary":
        rides = config["Disney"]["rides"].split(",")
        times = get_wait_times()
        outList=[]
        for ride in rides:
            r = ""
            if ride in names:
                r = names[ride]
            else:
                r = ride
            if r in times:
                outList.append(r+": "+str(times[r]))
            else:
                outList.append("Couldn't understand "+r+".")
        return "\n".join(outList)
    if messageSplit[1] == "time":
        if len(messageSplit)<3:
            return "Usage: disneyland time <ride>"
        query = " ".join(messageSplit[2:])
        if query in names:
            ##If the user sends a short name, translate it.
            query = names[query]
        times = get_wait_times()
        if query in times:
            return query+": "+str(times[query])
        else:
            return "I couldn't understand "+query+"."
        


if __name__ == "__main__":
    wait_times = get_wait_times()
    for i in wait_times.keys():
        print (i+": "+str(wait_times[i]))
    print()
    print()
    print(read_input("disneyland summary","yes"))
    print()
    print(read_input("disneyland time sky school","yes"))
