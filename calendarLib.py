##Calendar parser
##Takes the URL of a Google Calendar private URL and returns a set
##    of "Event" objects saying the time, location, and name of events.


import time
import requests
import icalendar
import datetime
import pytz



class Event():
    def __init__(self, name, date, place="", allDay = False):
        self.name = name
        self.date = date
        self.place = place
        self.allDay = allDay
    def prettyPrint(self, showDate=True):
        month = str(int(self.date[1]))
        day = str(int(self.date[2]))
        h = self.date[3]
        if h == 12 or h == 0:
            hour = "12"
        else:
            hour = str(h%12)
        if showDate:
            t = time.strftime(month+"/"+day+"/%Y at "+hour+":%M%p",self.date)
            if self.allDay:
                t = time.strftime(month+"/"+day+"/%Y",self.date)
        else:
            t = time.strftime(hour+":%M%p",self.date)
        p = ""
        if self.place != "":
            p = " @ "+self.place
        return t+p+": "+self.name


def getCalendarFile(url):
    r = requests.get(url)
    return r.text

def getCalendarEvents(url,tz = "America/Los_Angeles"):
    raw = getCalendarFile(url)
    ical = icalendar.Calendar.from_ical(raw)
    outputList = []
    for component in ical.walk():
        if component.name == "VEVENT":
            s = component.get("summary")
            d = component.get("dtstart").dt
            try:
                d = d.astimezone(pytz.timezone(tz))
            except:
                pass
            
            d = d.timetuple()
            p = component.get("location")
            outputList.append(Event(s,d,p))
    return sorted(outputList, key=lambda x: x.date) #Return a sorted list.

def getUpcomingEvents(url,tz="America/Los_Angeles"):
    events = getCalendarEvents(url)
    t = time.localtime()
    outList =  []
    for event in events:
        if event.date>t:
            ## If the event is upcoming, add it to the list.
            outList.append(event)
    return sorted(outList,key=lambda x: x.date) # Return a sorted list.

def readInput(message,config):
    messageSplit = message.lower().split()
    if messageSplit[1] == "next":
        upcoming = getUpcomingEvents(config["calendar"]["url"],config["calendar"]["timezone"])
        return upcoming[0].prettyPrint()
    if messageSplit[1] == "upcoming":
        upcoming = getUpcomingEvents(config["calendar"]["url"],config["calendar"]["timezone"])
        number = 5
        if len(messageSplit)>=3:
            try:
                number = int(messageSplit[2])
            except:
                return "I couldn't understand the number you sent."
        if len(upcoming) <= number:
            ## If the user asked for more events than there are on the calendar, send the whole calendar.
            return "\n".join([event.prettyPrint() for event in upcoming])
        else:
            return "\n".join([event.prettyPrint() for event in upcoming[:number]])

if __name__ == "__main__":
    testTime = time.strptime("4/16/2017 12:00AM", "%m/%d/%Y %I:%M%p") 
    myEvent = Event("Radio Show",testTime,"Chapman",True)
    myEvent2 = Event("Class",testTime)
    print("Pretty printing events...")
    print(myEvent.prettyPrint())
    print(myEvent2.prettyPrint(False))
