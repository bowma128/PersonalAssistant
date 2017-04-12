# PersonalAssistant
A Raspberry Pi-based personal assistant accessed by email/text message.


Targets Python version 3.4.1 and up.

Python dependencies: icalendar, pytz, requests

To download dependencies: python -m pip install icalendar pytz requests



You will need:
    
* A Gmail account solely for the personal assistant.
    
* An email account to send commands to.
    
* A New York Times Top Stories API Key.
    
* A URL of an ICAL file to read from (If using Google Calendar, this would be your "private address" for your calendar.

---

## Setup
                                          
1. Set up python 3.x and install all requred dependencies.
                                          
2. Use "config_blank.ini" as a template and create your configuration file, renaming it "config.ini".
                                          
  *If wanting to use text messages for control, see "SMS Gateways" below.
                                          
3. Once the configuration file is set up, run main.py to run the script.

---                                      

## SMS Gateways:
                                          
1. Look up which cellular carrier you are on.
                                          
2. [Using this website,](https://mfitzp.io/list-of-email-to-sms-gateways/) look up what your SMS or MMS gateway is by your cellular carrier. SMS will work, but MMS works better.

3. Use your phone number in the SMS/MMS Gateway.

  *For example: if 714-555-1234 was on Verizon Wireless, the email would be 7145551234@vxwpix.com.
