from flask import Flask, request
from auth import privateAuth, requestAuth
import functions
import structs
import config 


app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

@app.route("/api/commit", methods=["GET", "POST"])
def apiCommit():
    # Gathers Header Object
    headerContent = request.headers
    
    # Gathers File Object
    file = request.files['file']
    
    # Validates Auth Creds: If they dont exist or are otherwise incorrect the connection is severed without a response
    privateAuth(headerContent["token"])
    
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
        "fileIp":ipv4
    }
    # Validates File Request: Checks for sqlinjection attack vectors by screening for special chars (ie. "\", "%", "SELECT", etc)
    if requestAuth(fileDetails) != True:
        return structs.httpResponses.fourhundred()
    # Saves File to Disk & Saves File Details to DB
    try:
        functions.contentWrite(file, fileDetails, False)
        return structs.httpResponses.twohundred()
    except:
        return structs.httpResponses.fivehundred()
    
app.run(host=config.details()["network"]["host"], port=config.details()["network"]["port"])