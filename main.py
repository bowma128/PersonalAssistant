#Personal Assistant - a text based personal assistant.
# Dylan Bowman 2017
# Version 0.1

#Local imports
import emailLib, weather, news
#Python imports
import configparser, time

def main():
    config=configparser.ConfigParser()
    config.read("config.ini")
    authorized = config["email"]["authorized"].replace(" ","").split(",")
    send_text(config,"7757700521@vzwpix.com","System is up and running.")
    print("System is up and running.")
    run_app = True # Change this to false to quit the application.
    while(run_app):
        try:
            messages = read_emails(config)
        except:
            print("Could not read emails.")
            time.sleep(1)
            continue
        for message in messages:
            if message[0] in authorized:
                run_app = process_message(message,config)            
            else:
                print("Unauthorized user sending mail: "+message[0])
        time.sleep(1)

def process_message(message,config):
    message_body = message[1].lower()
    split_msg = message_body.split(" ")
    if message_body == "quit":
        print("Recieved quit command. Exiting.")
        send_text(config,message[0],"Goodbye.")
        return False
    elif message_body == "time" or message_body=="date":
        print("Sent date to user.")
        send_text(config,message[0],time_date())
        return True
    elif split_msg[0]=="weather":
        ## If the user input a weather command, send it to the weather module.
        print("User: "+message_body)
        out = weather.readInput(message_body,config)
        print("Me: "+out)
        send_text(config,message[0],out)
        return True
    elif split_msg[0] == "news":
        ## If the user input a news command, send it to the news module.
        print("User: "+message_body)
        out = news.readInput(message_body,config)
        print("Me: "+out)
        send_text(config,message[0],out)
        return True
    else:
        print("Couldn't understand message: "+message_body)
        return True

def time_date():
    # Returns a nice-looking time/date.
    lt = time.localtime()
    suffix = "th"
    if lt[2]%10==1:
        suffix = "st"
    elif lt[2]%10==2:
        suffix = "nd"
    elif lt[2]%10==3:
        suffix = "rd"
    number = str(lt[2])
    return time.strftime("%A, %B "+number+suffix+", %Y %I:%M:%S %p", time.localtime())

def read_emails(config):
    user = config["email"]["user"]
    password = config["email"]["password"]
    imap_addr = config["email"]["imap_server"]
    return emailLib.read_email(user,password,imap_addr)
    
def send_text(config,to,body):
    user = config["email"]["user"]
    password = config["email"]["password"]
    smtp_addr = config["email"]["smtp_server"]
    emailLib.send_email(user,password,to,"",body,smtp_addr)


if __name__ == "__main__":
    main()
