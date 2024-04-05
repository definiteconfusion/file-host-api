from auth import privateAuth, requestAuth
from flask import Flask, request
import functions
import structs
import config

app = Flask(__name__)

app.debug = True

@app.route("/")
def home():
    return "Hello World"

@app.route("/commit/<METHOD>", methods=["GET", "POST"])
def apiCommit(METHOD):
    # Route Protection 
    if METHOD != "cdn" and METHOD != "api":
        return structs.httpResponses.fourhundredfour()
    # Validates Auth Creds: If they don't exist or are otherwise incorrect the connection is severed without a response
    try:
        # Gathers Header Object
        headerContent = request.headers
        privateAuth(headerContent["token"])
    except:
        return structs.httpResponses.fivehundred()
    # Gathers File Object
    try:
        file = request.files['file']
    except:
        return structs.httpResponses.fivehundred()

    # Gathers User Ipv4 Address for Storage
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
        functions.contentWrite(file, fileDetails, METHOD)
        return structs.httpResponses.twohundred()
    except:
        return structs.httpResponses.fivehundred()


@app.route("/pull/<METHOD>", methods=["GET"])
def apiPull(METHOD):
    # Route Protection 
    if METHOD != "cdn" and METHOD != "api":
        return structs.httpResponses.fourhundredfour()
    # Validates Auth Creds: If they don't exist or are otherwise incorrect the connection is severed without a response
    try:
        # Gathers Header Object
        headerContent = request.headers
        privateAuth(headerContent["token"])
    except:
        structs.httpResponses.fivehundred()
    # File Return
    fileContent = functions.contentRead(headerContent, METHOD)
    if METHOD == "cdn":
        retContent = {"fileContent":fileContent, "fileConfig":functions.sql.cmd(f"SELECT filename, filextension FROM publicUserData WHERE userId = '{headerContent['token']}' AND filename = '{headerContent['fileName']}'")[0]}
    else:
        retContent = {"fileContent":fileContent, "fileConfig":functions.sql.cmd(f"SELECT filename, filextension FROM privateUserData WHERE userId = '{headerContent['token']}' AND filename = '{headerContent['fileName']}'")[0]}
    return retContent

@app.route("/user/<METHOD>")
def user(METHOD):
    email = request.args.get("email")
    verifToken = request.args.get("token")
    try:
        if METHOD == "register" and email:
            initIdMethod = functions.idGen()
            functions.sql.cmd(f"INSERT INTO users (userId, userToken, recEmail) VALUES ('{initIdMethod}', '{initIdMethod}', '{email}')")
            return {
                "token":initIdMethod,
                "response":structs.httpResponses.twohundred()
            }
        elif METHOD == "recovery":
            try:
                userToken = str(functions.sql.cmd(f"SELECT userToken FROM users WHERE recEmail = '{email}'")[0][0])
                recToken = functions.idGen(20)
                if functions.email(email, recToken) == False:
                    return structs.httpResponses.fourhundredeight()
                functions.sql.cmd(f"INSERT INTO activeVerifTokens (verifToken, userToken) VALUES ('{recToken}', '{userToken}')")
                return structs.httpResponses.twohundred()
            except Exception as e:
                return str(e)
        elif METHOD == "verify":
            retToken = functions.sql.cmd(f"SELECT userToken FROM activeVerifTokens WHERE verifToken = '{verifToken}'")[0][0]
            return retToken
        else:
            return "Ended in Else"
    except:
        return structs.httpResponses.fivehundred()

@app.route("/git/commit/<METHOD>", methods=["GET", "POST"])
def gitCommit(METHOD):
    if METHOD != "gitcdn" and METHOD != "gitapi":
        return structs.httpResponses.fourhundredfour()
    # Validates Auth Creds: If they don't exist or are otherwise incorrect the connection is severed without a response
    try:
        # Gathers Header Object
        headerContent = request.headers
        privateAuth(headerContent["token"])
    except:
        structs.httpResponses.fivehundred()
    try:
        file = request.files['file']
    except:
        return structs.httpResponses.fivehundred()

    # Gathers User Ipv4 Address for Storage
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
        functions.contentWrite(file, fileDetails, METHOD)
        return structs.httpResponses.twohundred()
    except:
        return structs.httpResponses.fivehundred()

@app.route("/git/pull/<METHOD>", methods=["GET"])
def gitPull(METHOD):
    # Route Protection
    if METHOD != "gitcdn" and METHOD != "gitapi":
        return structs.httpResponses.fourhundredfour()
    # Validates Auth Creds: If they don't exist or are otherwise incorrect the connection is severed without a response
    try:
        # Gathers Header Object
        headerContent = request.headers
        privateAuth(headerContent["token"])
    except:
        structs.httpResponses.fivehundred()
    # File Return
    fileContent = functions.contentRead(headerContent, METHOD)
    if METHOD == "gitcdn":
        retContent = {"fileContent":fileContent, "fileConfig":functions.sql.cmd(f"SELECT filename, filextension FROM gitPublicUserData WHERE userId = '{headerContent['token']}' AND filename = '{headerContent['fileName']}'")[0]}
    else:
        retContent = {"fileContent":fileContent, "fileConfig":functions.sql.cmd(f"SELECT filename, filextension FROM gitPrivateUserData WHERE userId = '{headerContent['token']}' AND filename = '{headerContent['fileName']}'")[0]}
    return retContent

app.run(host=config.details()["network"]["host"], port=config.details()["network"]["port"])