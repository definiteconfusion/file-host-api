from flask import Flask, request
import functions
import datetime
import structs
import config 
import os

app = Flask(__name__)

@app.route("/api/post", methods=["POST"])
def api():
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
    file.save(os.path.join(config.details()["content"], f"{fileId}.{fileExtension}"))
    functions.sql.cmd(f"INSERT INTO userData (filename, fileid, filextension, lastmodified) VALUES ('{(file.filename).split('.')[0]}', '{fileId}', '{(file.filename).split('.')[1]}', '{datetime.datetime.now()}')")
    if cfg == True:
        try:
            print(eval(urlconfig))
            return structs.httpResponses.twohundred()
        except Exception as err:
            print(err)  
            return str(err)
    else:
        return fileExtension

app.run(host=config.details()["network"]["host"], port=config.details()["network"]["port"])