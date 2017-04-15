##Reminders
##Version: 0.1
##Author: Dylan Bowman
import time

class Reminders():
    def __init__(self):
        self.reminders = []

    def parseCSV(self,filename):
        ##Takes in a filename of a CSV and returns a list of lines in the form of maps
        ##   That map the header of that column to the value
        ##Read the file into a list of lines.
        try:
            fileHandle = open(filename,"r")
        except:
            fileHandle = open(filename,"w")
            fileHandle.write("type,text,location,t-date,r-type,r-day,r-time")
            fileHandle.close()
            self.reminders = []
            return
        lines = fileHandle.readlines()
        fileHandle.close()
        output = []
        count = 0
        headers = []
        for line in lines:
            count += 1
            s = line.replace("\n","").split(",")
            #If it's the first line, assume it's the header.
            if count == 1:
                headers = s
            else:
                #If it's not the first line, loop through it and map it's header to it's values.
                outDict = {}
                for i in range(len(s)):
                    if s[i] != "":
                        outDict[headers[i]] = s[i]
                #Add that to the output list.
                output.append(outDict)
        self.reminders = output

    def writeCSV(self,filename):
        ##Assume all possible headers.
        outStrs = []
        headers = ["type","text","location","t-date","t-time","r-type","r-day","r-time"]
        outStrs.append(",".join(headers))
        for reminder in self.reminders:
            outList = []
            for header in headers:
                if header in reminder:
                    outList.append(reminder[header])
                else:
                    outList.append("")
            outStrs.append(",".join(outList))
        outStr ="\n".join(outStrs)
        fileHandle = open(filename,"w")
        fileHandle.write(outStr)
        fileHandle.close()

    def addReminder(self,data):
        if data[0] == "l":
            #Location based reminder, add as such.
            outputDict = {"type":"l", "text":data[1], "location":data[2]}
            self.reminders.append(outputDict)
        elif data[0] == "t":
            #Example list: "t","Take out the trash","4/17/17","08:00 PM"
            # type: t, text: take out the trash, date: 4/17/17, time: 8PM
            outputDict = {"type":"t","text":data[1],"t-date":data[2],"t-time":data[3]}
            self.reminders.append(outputDict)
        elif data[0] == "r":
            #Example list: "r","Take meds","w","5","08:00 PM"
            # type: r, text: take meds, r-type: weekly, r-day: 5, r-time: 8PM
            outputDict ={}
            if data[2]=="d":
                #Daily reminder, doesn't need a day value.
                outputDict = {"type":"r","text":data[1],"r-type":"d","r-time":data[3]}
            else:
                outputDict = {"type":"r","text":data[1],"r-type":data[2],"r-day":data[3],"r-time":data[4]}
            self.reminders.append(outputDict)
            
    def removeReminder(self,text):
        ##Search for all reminders with text and remove it.
        self.reminders = [r for r in self.reminders if r["text"].lower() != text.lower()]

    def getLocationReminders(self,location):
        reminders = [r for r in self.reminders if "location" in r and r["location"].lower() == location.lower()]
        self.reminders = [r for r in self.reminders if r not in reminders] ## Delete the reminders sent.
        return "\n".join([r["text"] for r in reminders])

    def getTimeReminders(self):
        lt = time.localtime()
        output = []
        for reminder in self.reminders:
            if reminder["type"] == "t":
                d=[]
                t=[]
                try:
                    d = time.strptime(reminder["t-date"], "%m/%d/%Y")
                except:
                    print(reminder["t-date"] +" is not a valid date. MM/DD/YYYY")
                    continue
                try:
                    t = time.strptime(reminder["t-time"], "%I:%M %p")
                except:
                    print(reminder["t-time"] + " is not a valid time. HH:MM PM")
                    continue
                if lt[0]==d[0] and lt[1]==d[1] and lt[2]==d[2] and lt[3]==t[3] and lt[4]==t[4]:
                    #If the time and date match, give to user and remove from the list.
                   output.append(reminder["text"])
                   self.reminders = [r for r in self.reminders if r != reminder]
            if reminder["type"] == "r":
                #Parse the time, see if it's right. If it is, then see what type it is and decide.
                lt = time.localtime()
                t = time.strptime(reminder["r-time"], "%I:%M %p")
                if t[3]!=lt[3] or t[4]!=lt[4]:
                    ##If the hour or minute don't match up, it's not time to send that reminder.
                    ##Move along.
                    continue
                if reminder["r-type"]=="d":
                    #If it's a daily reminder and the time matches, send it.
                    output.append(reminder["text"])
                elif reminder["r-type"] == "w":
                    #If it's a weekly reminder, check if the day matches.
                    d = 0
                    try:
                        day = int(reminder["r-day"])
                    except:
                        print(reminder["r-day"] + " is not a valid weekday. 0 - 6, 0 being Monday.")
                    if lt[6]==day:
                        output.append(reminder["text"])
                elif reminder["r-type"] == "m":
                    #If it's a monthly reminder, check if the day matches.
                    d = 0
                    try:
                        day = int(reminder["r-day"])
                    except:
                        print(reminder["r-day"] + " is not a valid number.")
                    if lt[2]==day:
                        output.append(reminder["text"])
        return "\n".join(output)

    def readInput(self,message):
        messageSplit = message.lower().split()
        messageSplitUpper = message.split()
        if messageSplit[1] == "remove":
            l = len(self.reminders)
            self.removeReminder(" ".join(messageSplit[2:]))
            diff = l - len(self.reminders)
            if diff == 0:
                return "No reminders removed."
            else:
                return "Removed "+str(diff)+" reminders."
        if messageSplit[1] == "get":
            #Getting location based reminders.
            rem = self.getLocationReminders(" ".join(messageSplit[2:]))
            #if there aren't reminders, return true so the system doesn't text back.
            if rem == "":
                return True
            else:
                return "Reminder: "+rem
        if messageSplit[1] == "add":
            if messageSplit[2] == "location":
                self.addReminder(["l"," ".join(messageSplitUpper[4:]),messageSplit[3]])
                return "Reminder added."
            if messageSplit[2] == "once":
                ##Try to parse the date and time. If one fails, alert the user.
                try:
                    d = time.strptime(messageSplit[3],"%m/%d/%Y")
                except:
                    print (messageSplit[3])
                    return "I can't understand that date. Format: MM/DD/YYYY"
                try:
                    t = time.strptime(messageSplit[4]+" "+messageSplit[5],"%I:%M %p")
                except:
                    return "I can't understand that time. Format: HH:MM am/pm"
                ## If the function has gotten this far, the time and date are valid. Add the reminder.
                self.addReminder([ "t"," ".join(messageSplitUpper[6:]),messageSplit[3],messageSplit[4]+" "+messageSplit[5]])
                return "Reminder added."
            if messageSplit[2] == "daily":
                ## Try to parse the time. If it fails, alert the user.
                try:
                    t = time.strptime(messageSplit[3]+" "+messageSplit[4],"%I:%M %p")
                except:
                    return "I can't understand that time. Format: HH:MM am/pm"
                ## If the function has gotten this far, the time is valid, add the reminder.
                self.addReminder(["r"," ".join(messageSplitUpper[5:]),"d",messageSplit[3]+" "+messageSplit[4]])
                return "Reminder added."
            if messageSplit[2] == "monthly":
                ##Try to parse the day of the month and the time. If it fails, alert the user.
                try:
                    d = int(messageSplit[3])
                except:
                    return "I don't understand that day number."
                try:
                    t = time.strptime(messageSplit[4]+" "+messageSplit[5],"%I:%M %p")
                except:
                    return "I can't understand that time. Format: HH:MM am/pm"
                #If we're here, add the reminder.
                self.addReminder(["r"," ".join(messageSplitUpper[6:]),"m",messageSplit[3],messageSplit[4]+" "+messageSplit[5]])
                return "Reminder added."
            if messageSplit[2] == "weekly":
                d = parseWeekday(messageSplit[3])
                if d==False:
                    return "I can't understand that weekday."
                try:
                    t = time.strptime(messageSplit[4]+" "+messageSplit[5],"%I:%M %p")
                except:
                    return "I can't understand that time. Format: HH:MM am/pm"
                #If we're here, add the reminder.
                self.addReminder(["r"," ".join(messageSplitUpper[6:]),"w",d,messageSplit[4]+" "+messageSplit[5]])
                return "Reminder added."
def parseWeekday(weekday):
    w = weekday.lower()
    if w == "monday" or w == "mon" or w == "m" or w == "0":
        return "0"
    if w == "tuesday" or w == "tue" or w == "t" or w == "1":
        return "1"
    if w == "wednesday" or w == "wed" or w == "w" or w == "2":
        return "2"
    if w == "thursday" or w == "thu" or w == "r" or w == "3":
        return "3"
    if w == "friday" or w == "fri" or w == "f" or w == "4":
        return "4"
    if w == "saturday" or w == "sat" or w == "5":
        return "5"
    if w == "sunday" or w == "sun" or w == "6":
        return "6"
    return False
            
if __name__ == "__main__":
    r = Reminders()
    r.parseCSV("test_data.csv")
    print("Adding location reminder.")
    print(r.readInput("reminders add location here hello friend! How are you?"))
    print("Reading location reminders.")
    print(r.readInput("reminders get here"))
    print("Adding solo reminder.")
    print(r.readInput("reminders add once 4/15/2017 3:30 pm Solo reminder works!"))
    print("Adding daily reminder.")
    print(r.readInput("reminders add daily 3:30 pm Daily reminder works!"))
    print("Adding monthly reminder.")
    print(r.readInput("reminders add monthly 15 5:00 pm Monthly reminder works!"))
    print("Adding weekly reminder.")
    print(r.readInput("reminders add weekly Saturday 5:00 pm Weekly reminder works!"))
    r.writeCSV("out_data.csv")
    print("Here's what's left over.")
    for reminder in r.reminders:
        print(reminder)
