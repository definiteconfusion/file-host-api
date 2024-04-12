# API Endpoint Reference

## Private vs Public File Storage
### Private
Private files are stored on the server under the context of `API`. This context separates the files from the public files, however this difference is also reflected in the server call 
```Python
# Imports
import requests
# File Reader Function
def fileRead(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        pass
# Defines Information to be Sent with the File
HEADERS = {
"fileName": "example_filename",
"fileExtension": "example_file_extension",
"userId": "example_user_token"
}
# Opens File from Working Directory
FILE = fileRead("./examplefile.json")
# Submits a POST request to the server and prints the text response
print(requests.post("<SERVER HOST IPV4 ADDRESS>/commit/api", files=FILE).text)
```
<seealso>
    <category ref="lnks">
        <a href="https://github.com/definiteconfusion">My Github</a>
        <a href="https://www.linkedin.com/in/jake-rase-9a28a926a/">My LinkedIn</a>
        <a href="https://www.python.org/downloads/">Python Download</a>
    </category>
</seealso>