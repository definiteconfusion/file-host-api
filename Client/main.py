import requests

def fileRead(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    "token":"gu",
    "fileName": "deffcoltst",
    "fileExtension":"html"
}

file_content = fileRead("/Users/jakerase/Downloads/deffcoltst.html")

rutLst = ["cdn", "api"]
for i in range(len(rutLst)):
    if file_content is not None:
        files = {"file": file_content}
        prin = requests.post(f"http://127.0.0.1:3000/commit/{rutLst[i]}", headers=HEADER, files=files).text
        print(prin)
