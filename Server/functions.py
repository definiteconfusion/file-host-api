from config import details
from timeout_decorator import timeout
import datetime
import sqlite3
import smtplib
import random
import ssl
import os

class sql:
    def cmd(command:str) -> str:
        database = details()["database"]
        init = sqlite3.connect(f'{database}')
        cursor = init.cursor()
        cursor.execute(f"{command}")
        if "SELECT" in command:
            type_result = cursor.fetchall()
        elif "PRAGMA" in command:
            type_result = cursor.fetchall()
        else:
            type_result = "ENDED IN ELSE"
            init.commit()
        return type_result

def idGen(length:int=10):
    neoid = ""
    chars = ["a", "b", "c", "d", "e", "f", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for idchars in range(length):
        neoid = neoid + chars[random.randint(0, 14)]
    return neoid

def fileRead(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    
def contentWrite(file, fileDetails, iscdn):
    if iscdn == "api":
        savePath = os.path.join(details()['content'], "API/", f"{fileDetails['fileId']}.{fileDetails['fileExtension']}")
    elif iscdn == "cdn":
        savePath = os.path.join(details()['content'], "CDN/", f"{fileDetails['fileId']}.{fileDetails['fileExtension']}")
    elif iscdn == "gitapi":
        savePath = os.path.join(details()['content'], "GITAPI/", f"{fileDetails['fileId']}.{fileDetails['fileExtension']}")
    else:
        savePath = os.path.join(details()['content'], "GITCDN/", f"{fileDetails['fileId']}.{fileDetails['fileExtension']}")

    try:    
        currTime = datetime.datetime.now()
        file.save(savePath)
        if iscdn == "api":
            sql.cmd(f"INSERT INTO privateUserData (filename, fileid, filextension, lastmodified, fileIp, userId) VALUES ('{(fileDetails['fileName'])}', '{fileDetails['fileId']}', '{fileDetails['fileExtension']}', '{currTime}', '{fileDetails['fileIp']}', '{fileDetails['userId']}')")
        elif iscdn == "cdn":
            sql.cmd(f"INSERT INTO publicUserData (filename, fileid, filextension, lastmodified, fileIp, userId) VALUES ('{(fileDetails['fileName'])}', '{fileDetails['fileId']}', '{fileDetails['fileExtension']}', '{currTime}', '{fileDetails['fileIp']}', '{fileDetails['userId']}')")
        elif iscdn == "gitapi":
            sql.cmd(f"INSERT INTO gitPublicUserData (filename, fileid, filextension, lastmodified, fileIp, userId) VALUES ('{(fileDetails['fileName'])}', '{fileDetails['fileId']}', '{fileDetails['fileExtension']}', '{currTime}', '{fileDetails['fileIp']}', '{fileDetails['userId']}')")
        else:
            sql.cmd(f"INSERT INTO gitPublicUserData (filename, fileid, filextension, lastmodified, fileIp, userId) VALUES ('{(fileDetails['fileName'])}', '{fileDetails['fileId']}', '{fileDetails['fileExtension']}', '{currTime}', '{fileDetails['fileIp']}', '{fileDetails['userId']}')")
    except Exception as e:
        print(e)
        
def contentRead(fileDetails, iscdn):
    try:
        if iscdn != "cdn":
            neoFileDetails = sql.cmd(f"SELECT fileId, filextension FROM privateUserData WHERE userId = '{fileDetails['token']}' AND filename = '{fileDetails['fileName']}'")[0]
            content = fileRead(f"{details()['content']}/API/{neoFileDetails[0]}.{neoFileDetails[1]}")
        else:
            neoFileDetails = sql.cmd(f"SELECT fileId, filextension FROM publicUserData WHERE userId = '{fileDetails['token']}' AND filename = '{fileDetails['fileName']}'")[0]
            content = fileRead(f"{details()['content']}/CDN/{neoFileDetails[0]}.{neoFileDetails[1]}")
        return content
    except Exception as e:
        return e

def send_via_email(
    number: str,
    message: str,
    sender_credentials: tuple,
    subject: str = "",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
    sender_email, email_password = sender_credentials
    receiver_email = number

    email_message = f"Subject: {subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

@timeout(10)
def email(email:str, token:str):
    sender_credentials = (details()["smtp_creds"]["origin_addr"],details()["smtp_creds"]["2fa_passkey"])
    try:
        send_via_email(email,
                         f"""
                         \nYour Recovery API Call Looks Like This 
                         \n
                         \n -- Python -- 
                         \nimport requests
                         \nprint(requests.get('http://{details()["network"]["host"]}:{details()["network"]["port"]}/user/verify?token={token}').text)
                         \n
                         \n -- Node.Js -- 
                         \nfetch('http://{details()["network"]["host"]}:{details()["network"]["port"]}0/user/verify?token={token}')
                         \n.then(response => response.text())
                         \n.then(data => console.log(data))
                         \n.catch(error => console.error('Error:', error));
                         \n
                         \n -- PhP -- 
                        \n<?php
                        \n$url = 'http://{details()["network"]["host"]}:{details()["network"]["port"]}/user/verify?token={token}';
                        \n$response = file_get_contents($url);
                        \necho $response;
                        \n?>
    """, sender_credentials,"File Host Api Account Recovery")
    except TimeoutError:
        return False