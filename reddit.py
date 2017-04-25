import requests,json
import requests.auth
import emailLib

class post():
    def __init__(self,data):
        self.selfPost = data["is_self"]
        self.url = data["url"]
        self.author=data["author"]
        self.title=data["title"]
        #Determine if the link is a photo.
        urlSplit = self.url.split(".")
        if len(urlSplit)==1:
            self.photo = False
        else:
            if urlSplit[len(urlSplit)-1] in ["jpg","jpeg","png","gif"]:
                self.photo = True
                self.ext = urlSplit[len(urlSplit)-1]
            else:
                self.photo = False
    def __str__(self):
        return "\""+self.title+"\" by "+self.author+": "+self.url
        
def get_access_token(config):
    client_auth = requests.auth.HTTPBasicAuth(config["reddit"]["id"],config["reddit"]["secret"])
    client_headers = {"User-Agent": "Personal Assistant/0.1 by dbowman_pa"}
    client_data = {"grant_type":"password",
                   "username":config["reddit"]["user"],
                   "password":config["reddit"]["pass"]}
    r = requests.post("https://www.reddit.com/api/v1/access_token",
                      data = client_data,
                      headers = client_headers,
                      auth = client_auth
                      )
    json_data = r.json()
    return json_data["access_token"]

def get_top_post(config, subreddit):
    #Get an access token from reddit.
    access_token = get_access_token(config)
    #Set up the headers and access the server.
    headers = {"Authorization":"bearer "+access_token, "User-Agent":"Personal Assistant/0.1 by dbowman_pa"}
    r = requests.get("https://oauth.reddit.com/r/"+subreddit+"/hot",headers=headers)
    #Parse the JSON data.
    json_data = json.loads(r.text)
    children = json_data["data"]["children"]
    #Loop through the children.
    for child in children:
        data = child["data"]
        p = post(data)
        #Return the first child that is not a sticky post.
        if not data["stickied"]:
            return p

def digestable(config):
    p = get_top_post(config,config["reddit"]["sub"])
    if p.photo:
        r = requests.get(p.url)
        fileHandle = open("picture."+p.ext,"wb")
        fileHandle.write(r.content)
        fileHandle.close()
        return {"is_photo":True, "location":"picture."+p.ext, "title":p.title}
    else:
        return {"is_photo":False, "url":p.url, "title":p.title}

def readInput(config,message):
    messageSplit = message.lower().split()
    if messageSplit[1] == "top":
        if len(messageSplit)<3:
            return "Usage: reddit top <subreddit>"
        p = get_top_post(config,messageSplit[2])
        if p.photo:
            r = requests.get(p.url)
            fileHandle = open("picture."+p.ext,"wb")
            fileHandle.write(r.content)
            fileHandle.close()
            return {"sub":messageSplit[2],"is_photo":True, "location":"picture."+p.ext, "title":p.title}
        else:
            return {"sub":messageSplit[2],"is_photo":False, "url":p.url, "title":p.title}


if __name__ == "__main__":
    import configparser
    config = configparser.ConfigParser()
    config.read("config.ini")
    p = get_top_post(config,"wholesomememes")
    print(p)
