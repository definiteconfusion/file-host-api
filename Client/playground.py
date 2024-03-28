import requests
import os

def fileRead(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    
def contentWrite(filec, fileDetails):
    savePath = str(os.getcwd()) + "/Desktop/file-host-api/Client/" + f"{fileDetails[0]}.{fileDetails[1]}"
    with open(savePath, 'w') as file:
        file.write(filec)

HEADER = {
    "token":"gu",
    "fileName": "deffcoltst",
    "fileExtension":"html"
}
#
# file_content = fileRead("/Users/jakerase/Downloads/deffcoltst.html")
# #
# rutLst = ["gitcdn"]
# for i in range(len(rutLst)):
#     if file_content is not None:
#         files = {"file": file_content}
#         prin = requests.post(f"http://127.0.0.1:3000/git/commit/{rutLst[i]}", headers=HEADER, files=files).text
#         print(prin)

rutLst = ["gitcdn"]
for i in range(len(rutLst)):
    prin = eval(requests.get(f"http://127.0.0.1:3000/git/pull/{rutLst[i]}", headers=HEADER).text)
    print(prin)
    fileContent = prin["fileContent"]
    fileConfig = prin["fileConfig"]
    contentWrite(fileContent, fileConfig)

# print(requests.get("http://127.0.0.1:3000/user/register?email=recTest@gmail.com").text)
# print(requests.get("http://127.0.0.1:3000/user/recovery?email=recTest@gmail.com").text)
# print(requests.get('http://127.0.0.1:3000/user/verify?token=6bbe33312e9f77342c11').text)
