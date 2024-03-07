from auth import privateAuth, requestAuth
from flask import Flask, request
import functions
import structs
import config 

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"

@app.route("/commit/<METHOD>", methods=["GET", "POST"])
def apiCommit(METHOD):
    # Route Protection 
    if METHOD != "cdn" and METHOD != "api":
        return structs.httpResponses.fourhundredfour()
    # Validates Auth Creds: If they dont exist or are otherwise incorrect the connection is severed without a response
    try:
        # Gathers Header Object
        headerContent = request.headers
        privateAuth(headerContent["token"])
    except:
        structs.httpResponses.fivehundred()
        
    # Assignes Write Method 
    if METHOD == "api":
        iscdn = False
    elif METHOD == "cdn":
        iscdn = True
        
    # Gathers File Object
    try:
        file = request.files['file']
    except:
        return structs.httpResponses.fivehundred()
    
    # Gathers User Ipv4 Adress for Storage
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ipv4 = request.environ['REMOTE_ADDR']
    else:
        ipv4 = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy
    
    # Data Condensation
    fileDetails = {
        "fileName":headerContent["fileName"],
        "fileExtension":headerContent["fileExtension"],
        "fileId": functions.idGen(),
        "fileIp":ipv4,
        "userId": headerContent["token"]
    }
    # Validates File Request: Checks for sqlinjection attack vectors by screening for special chars (ie. "\", "%", "SELECT", etc)
    if requestAuth(fileDetails) != True:
        return structs.httpResponses.fourhundred()
    # Saves File to Disk & Saves File Details to DB
    try:
        functions.contentWrite(file, fileDetails, iscdn)
        return structs.httpResponses.twohundred()
    except:
        return structs.httpResponses.fivehundred()
    

@app.route("/pull/<METHOD>", methods=["GET"])
def apiPull(METHOD):
    # Route Protection 
    if METHOD != "cdn" and METHOD != "api":
        return structs.httpResponses.fourhundredfour()
    # Validates Auth Creds: If they dont exist or are otherwise incorrect the connection is severed without a response
    try:
        # Gathers Header Object
        headerContent = request.headers
        privateAuth(headerContent["token"])
    except:
        structs.httpResponses.fivehundred()
    # Assignes Write Method 
    if METHOD == "api":
        iscdn = False
    elif METHOD == "cdn":
        iscdn = True
    # File Return
    fileContent = functions.contentRead(headerContent, iscdn)
    if iscdn  == True:
        return {"fileContent":fileContent, "fileConfig":functions.sql.cmd(f"SELECT filename, filextension FROM publicUserData WHERE userId = '{headerContent['token']}' AND filename = '{headerContent['fileName']}'")[0]}
    else:
        return {"fileContent":fileContent, "fileConfig":functions.sql.cmd(f"SELECT filename, filextension FROM privateUserData WHERE userId = '{headerContent['token']}' AND filename = '{headerContent['fileName']}'")[0]}
app.run(host=config.details()["network"]["host"], port=config.details()["network"]["port"])