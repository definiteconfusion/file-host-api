from flask import Flask, request
import functions
import datetime
import structs
import config 
import os

app = Flask(__name__)

@app.route("/api/post", methods=["POST"])
def post():
    urlconfig = request.args.get("cfg")
    if urlconfig:
        cfg = True
    else:
        cfg = False
    if 'file' not in request.files:
        return structs.httpResponses.fourhundred()
    file = request.files['file']

    if file.filename == '':
        return structs.httpResponses.fourhundred()
    fileExtension = (file.filename).split(".")[1]
    fileId = functions.idGen()
    currTime = datetime.datetime.now()
    file.save(os.path.join(config.details()["content"], f"{fileId}.{fileExtension}"))
    functions.sql.cmd(f"INSERT INTO userData (filename, fileid, filextension, lastmodified) VALUES ('{(file.filename).split('.')[0]}', '{fileId}', '{(file.filename).split('.')[1]}', '{currTime}')")
    if cfg == True:
        try:
            print(eval(urlconfig))
            return structs.httpResponses.twohundred()
        except Exception as err:
            print(err)  
            return str(err)
    else:
        return {
            "fileId":fileId,
            "fileName":file.filename,
            "dateTime":currTime
        }
    
@app.route("/api/sync", methods=["GET"])
def sync():
    urlconfig = eval(request.args.get("cfg"))
    try:
        sqlRes = functions.sql.cmd(f"SELECT fileId, lastmodified FROM userData WHERE fileId = '{urlconfig['fileId']}'")
        return sqlRes
    except Exception as e:
        # return structs.httpResponses.fourhundred()
        return str(e)
app.run(host=config.details()["network"]["host"], port=config.details()["network"]["port"])