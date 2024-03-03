from config import details
import datetime
import sqlite3
import structs
import random
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

def idGen():
    neoid = ""
    chars = ["a", "b", "c", "d", "e", "f", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for idchars in range(10):
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
    if iscdn != True:
        savePath = os.path.join(details()['content'], "API/", f"{fileDetails['fileId']}.{fileDetails['fileExtension']}")
    else:
        savePath = os.path.join(details()['content'], "CDN/", f"{fileDetails['fileId']}.{fileDetails['fileExtension']}")
    try:    
        currTime = datetime.datetime.now()
        file.save(savePath)
        sql.cmd(f"INSERT INTO privateUserData (filename, fileid, filextension, lastmodified, fileIp) VALUES ('{(fileDetails['fileName'])}', '{fileDetails['fileId']}', '{fileDetails['fileExtension']}', '{currTime}', '{fileDetails['fileIp']}')")
    except Exception as e:
        print(e)