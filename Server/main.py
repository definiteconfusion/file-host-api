from auth import privateAuth, requestAuth
from analytics import serverUtils
from flask import Flask, request
import functions
import analytics
import structs
import config

app = Flask(__name__)

app.debug = True


@app.route("/")
def home():
    return "Hello World"


@app.route("/commit/<METHOD>", methods=["GET", "POST"])
def apiCommit(METHOD):
    timeCache = serverUtils.startTime() # TIME START -- -- -- -- -->
    # Route Protection 
    if METHOD != "cdn" and METHOD != "api":
        return structs.HTTP(404)
    # Validates Auth Creds: If they don't exist or are otherwise incorrect the connection is severed without a response
    try:
        # Gathers Header Object
        headerContent = request.headers
        privateAuth(headerContent["token"])
    except:
        return structs.HTTP(500)
    # Gathers File Object
    try:
        file = request.files['file']
    except:
        return structs.HTTP(500)

    # Gathers User Ipv4 Address for Storage
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ipv4 = request.environ['REMOTE_ADDR']
    else:
        ipv4 = request.environ['HTTP_X_FORWARDED_FOR']  # if behind a proxy

    # Data Condensation
    fileDetails = {
        "filename": headerContent["fileName"],
        "fileextension": headerContent["fileExtension"],
        "fileid": functions.idGen(),
        "fileip": ipv4,
        "userid": headerContent["token"],
        "filecontent":headerContent["headerContent"],
        "requesttype": f"{METHOD}commit"
    }
    # Validates File Request: Checks for sqlinjection attack vectors by screening for special chars (ie. "\", "%", "SELECT", etc)
    if not requestAuth(fileDetails):
        return structs.HTTP(400)
    # Saves File to Disk & Saves File Details to DB
    processTime = serverUtils.endTime(timeCache) # TIME END -- -- -- -- -->
    fileSize = len(str(file).encode('utf-8')) # FILE SIZE MARKER -- -- -- -- -->
    try:
        spdTest = serverUtils.startTime() # SPEED START
        functions.contentWrite(fileDetails, METHOD)
        uploadTime = serverUtils.endTime(spdTest) # SPEED END -- -- -- -- -->
        fileSpeed = (fileSize / uploadTime.total_seconds()) # SPEED CALC -- -- -- -- -->
        analytics.databaseEntry(headerContent["token"], processTime, fileSpeed, ipv4) # ANALYTICS ENTRY -- -- -- -- -->
        return structs.HTTP(200)
    except Exception as e:
        # return structs.HTTP(500)
        return str(e)


@app.route("/pull/<METHOD>", methods=["GET"])
def apiPull(METHOD):
    timeCache = serverUtils.startTime()  # TIME START -- -- -- -- -->
    # Route Protection 
    if METHOD != "cdn" and METHOD != "api":
        return structs.HTTP(404)
    # Validates Auth Creds: If they don't exist or are otherwise incorrect the connection is severed without a response
    try:
        # Gathers User Ipv4 Address for Storage
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ipv4 = request.environ['REMOTE_ADDR']
        else:
            ipv4 = request.environ['HTTP_X_FORWARDED_FOR']  # if behind a proxy
        # Gathers Header Object
        headerContent = request.headers
        privateAuth(headerContent["token"])
    except:
        return structs.HTTP(500)
    processTime = serverUtils.endTime(timeCache)  # TIME END -- -- -- -- -->
    # File Return
    fileContent = functions.contentRead(headerContent, METHOD)
    if METHOD == "cdn":
        retContent = {"fileContent": fileContent, "fileConfig": functions.sql.cmd(
            f"SELECT filename, filextension FROM publicUserData WHERE userId = '{headerContent['token']}' AND filename = '{headerContent['fileName']}'")[
            0]}
    else:
        retContent = {"fileContent": fileContent, "fileConfig": functions.sql.cmd(
            f"SELECT filename, filextension FROM privateUserData WHERE userId = '{headerContent['token']}' AND filename = '{headerContent['fileName']}'")[
            0]}
    analytics.databaseEntry(headerContent["token"], processTime, None, ipv4)  # ANALYTICS ENTRY -- -- -- -- -->
    return retContent


@app.route("/user/<METHOD>")
def user(METHOD):
    email = request.args.get("email")
    verifToken = request.args.get("token")
    try:
        if METHOD == "register" and email:
            initIdMethod = functions.userIdGen(email)
            functions.sql.cmd(
                f"INSERT INTO users (userId, userToken, recEmail) VALUES ('{initIdMethod}', '{initIdMethod}', '{email}')")
            return {
                "token": initIdMethod,
                "response": structs.HTTP(200)
            }
        elif METHOD == "recovery":
            try:
                userToken = str(functions.sql.cmd(f"SELECT userToken FROM users WHERE recEmail = '{email}'")[0][0])
                recToken = functions.idGen(20)
                if not functions.email(email, recToken):
                    return structs.HTTP(408)
                functions.sql.cmd(
                    f"INSERT INTO activeVerifTokens (verifToken, userToken) VALUES ('{recToken}', '{userToken}')")
                return structs.HTTP(200)
            except Exception as e:
                return str(e)
        elif METHOD == "verify":
            try:
                userToken = functions.sql.cmd(f"SELECT userToken FROM activeVerifTokens WHERE verifToken = '{verifToken}'")[0][0]
                return userToken
            except:
                return structs.HTTP(404)
        else:
            return structs.HTTP(404)
    except:
        return structs.HTTP(500)


@app.route("/git/commit/<METHOD>", methods=["GET", "POST"])
def gitCommit(METHOD):
    timeCache = serverUtils.startTime()  # TIME START -- -- -- -- -->
    if METHOD != "gitcdn" and METHOD != "gitapi":
        return structs.HTTP(404)
    # Validates Auth Creds: If they don't exist or are otherwise incorrect the connection is severed without a response
    try:
        # Gathers Header Object
        headerContent = request.headers
        privateAuth(headerContent["token"])
    except:
        structs.HTTP(500)
    try:
        file = request.files['file']
    except:
        return structs.HTTP(500)

    # Gathers User Ipv4 Address for Storage
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ipv4 = request.environ['REMOTE_ADDR']
    else:
        ipv4 = request.environ['HTTP_X_FORWARDED_FOR']  # if behind a proxy

    # Data Condensation
    fileDetails = {
        "fileName": headerContent["fileName"],
        "fileExtension": headerContent["fileExtension"],
        "fileId": functions.idGen(),
        "fileIp": ipv4,
        "userId": headerContent["token"]
    }
    # Validates File Request: Checks for sqlinjection attack vectors by screening for special chars (ie. "\", "%", "SELECT", etc)
    if not requestAuth(fileDetails):
        return structs.HTTP(400)
    # Saves File to Disk & Saves File Details to DB
    processTime = serverUtils.endTime(timeCache)  # TIME END -- -- -- -- -->
    fileSize = len(str(file).encode('utf-8'))  # FILE SIZE MARKER -- -- -- -- -->
    try:
        spdTest = serverUtils.startTime()  # SPEED START
        functions.contentWrite(file, fileDetails, METHOD)
        uploadTime = serverUtils.endTime(spdTest)  # SPEED END -- -- -- -- -->
        fileSpeed = (fileSize / uploadTime.total_seconds())  # SPEED CALC -- -- -- -- -->
        analytics.databaseEntry(headerContent["token"], processTime, fileSpeed, ipv4)  # ANALYTICS ENTRY -- -- -- -- -->
        return structs.HTTP(200)
    except:
        return structs.HTTP(500)


@app.route("/git/pull/<METHOD>", methods=["GET"])
def gitPull(METHOD):
    timeCache = serverUtils.startTime()  # TIME START -- -- -- -- -->
    # Route Protection
    if METHOD != "gitcdn" and METHOD != "gitapi":
        return structs.HTTP(404)
    # Validates Auth Creds: If they don't exist or are otherwise incorrect the connection is severed without a response
    try:
        # Gathers User Ipv4 Address for Storage
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ipv4 = request.environ['REMOTE_ADDR']
        else:
            ipv4 = request.environ['HTTP_X_FORWARDED_FOR']  # if behind a proxy
        # Gathers Header Object
        headerContent = request.headers
        privateAuth(headerContent["token"])
    except:
        structs.HTTP(500)
    processTime = serverUtils.endTime(timeCache)  # TIME END -- -- -- -- -->
    # File Return
    fileContent = functions.contentRead(headerContent, METHOD)
    if METHOD == "gitcdn":
        retContent = {"fileContent": fileContent, "fileConfig": functions.sql.cmd(
            f"SELECT filename, filextension FROM gitPublicUserData WHERE userId = '{headerContent['token']}' AND filename = '{headerContent['fileName']}'")[
            0]}
    else:
        retContent = {"fileContent": fileContent, "fileConfig": functions.sql.cmd(
            f"SELECT filename, filextension FROM gitPrivateUserData WHERE userId = '{headerContent['token']}' AND filename = '{headerContent['fileName']}'")[
            0]}
    analytics.databaseEntry(headerContent["token"], processTime, None, ipv4)  # ANALYTICS ENTRY -- -- -- -- -->
    return retContent


app.run(host=config.details()["network"]["host"], port=config.details()["network"]["port"])
