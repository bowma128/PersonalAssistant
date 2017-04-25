import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import sys
import email
import imaplib
import time

def strip_address(address):
    index1 = address.find("<")+1
    index2 = address.find(">")
    if index1 == -1 or index2 == -1:
        return address
    else:
        return address[index1:index2]

def read_email(user,pwd,server):
    M = imaplib.IMAP4_SSL(server)
    try:
        rv, data = M.login(user,pwd)
    except imaplib.IMAP4.error:
        print("IMAP login failed.")
        return False
    rv, mailboxes = M.list()
    if rv!="OK":
        print("Could not read mailboxes.")
        return False
    rv, data = M.select("INBOX")
    if rv!="OK":
        print("Could not read mailboxes.")
        return False

    rv, data = M.search(None, "UnSeen")
    output_full= []
    if len(data[0].split()) == 0:
        return ()
    for num in data[0].split():
        output =[]
        rv, data = M.fetch(num, "(RFC822)")
        msg = email.message_from_string(data[0][1].decode("utf-8"))
        sender = strip_address(msg["From"])
        output.append(sender)
        t = time.mktime(email.utils.parsedate_tz(msg.get('date'))[:9])
        if msg.is_multipart():
            for payload in msg.get_payload():
                output.append(payload.get_payload())
        else:
            print(0)
            output.append(msg.get_payload())
        output_full.append(output)
    return output_full




def send_email(user,pwd,to,subject,body,smtp_addr):
    gmail_user = user
    gmail_password = pwd

    _from = gmail_user

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL(smtp_addr,465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(_from, to, email_text)
        server.close()

    except:
        print ('Something went wrong...')
        traceback.print_exc()

def send_attachment(user,pwd,to,subject,body,file,smtpserver):

    recipients = to
    emaillist = [elem.strip().split(',') for elem in recipients]
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = user
    msg['Reply-to'] = user

    msg.preamble = 'Multipart massage.\n'

    part = MIMEText(body)
    msg.attach(part)

    part = MIMEApplication(open(str(file),"rb").read())
    part.add_header('Content-Disposition', 'attachment', filename=file)
    msg.attach(part)


    server = smtplib.SMTP_SSL(smtpserver,465)
    server.ehlo()
    server.login(user, pwd)

    server.sendmail(msg['From'], to, msg.as_string())


if __name__ == "__main__":
    import configparser
    config = configparser.ConfigParser()
    config.read("config.ini")
    user = config["email"]["user"]
    password = config["email"]["password"]
    imap_addr = config["email"]["imap_server"]
    smtp_addr = config["email"]["smtp_server"]
    authorized = config["email"]["authorized"].replace(" ","").split(",")
    print("Sending email")
    #send_email(user,password,"7757700521@vzwpix.com","","Hello!",smtp_addr)
    print("Sending attachment")
    send_attachment(user,password,"7757700521@vzwpix.com","",
                    "Hello!","picture.jpg",smtp_addr)
#    print(read_email(user,password,imap_addr))
