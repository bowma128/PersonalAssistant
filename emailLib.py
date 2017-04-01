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

def read_email(user,pwd,server):
    M = imaplib.IMAP4_SSL(server)
    try:
        rv, data = M.login(user,pwd)
    except imaplib.IMAP4.error:
        logger.log("IMAP login failed.")
        return False
    rv, mailboxes = M.list()
    if rv!="OK":
        logger.log("Could not read mailboxes.")
        return False
    rv, data = M.select("INBOX")
    if rv!="OK":
        logger.log("Could not read mailboxes.")
        return False

    rv, data = M.search(None, "UnSeen")
    output= []
    if len(data[0].split()) == 0:
        return ()
    for num in data[0].split():
        rv, data = M.fetch(num, "(RFC822)")
        msg = email.message_from_string(data[0][1].decode("utf-8"))
        t = time.mktime(email.utils.parsedate_tz(msg.get('date'))[:9])
        if msg.is_multipart():
            for payload in msg.get_payload():
                output.append(payload.get_payload())
        else:
            print(0)
            output.append(msg.get_payload())
    return output




def send_email(user,pwd,to,subject,body):
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
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
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


    server = smtplib.SMTP("smtpserver")
    server.ehlo()
    server.starttls()
    server.login(user, pwd)

    server.sendmail(msg['From'], emaillist , msg.as_string())
