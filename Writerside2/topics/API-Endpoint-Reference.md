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
### Public
Public files fall under the `CDN` header, just as with the `API` files, it requires a different specification in the server call
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
print(requests.post("<SERVER HOST IPV4 ADDRESS>/commit/cdn", files=FILE).text)
```

## Git Repositories
#### NOT WORKING!!!!!

## PySync
PySync is the automatic project cloud saving client for the api. It can be installed and setup globally or on a project-by-project basis via a convenient CLI. When run, at a default stretch of time (The default is 5 seconds), the client will look for changes in files, or file content, if there are any, it packs the files and makes a post request to the server while saving the given project token for later. 
<seealso>
    <category ref="lnks">
        <a href="https://github.com/definiteconfusion">My Github</a>
        <a href="https://www.linkedin.com/in/jake-rase-9a28a926a/">My LinkedIn</a>
        <a href="https://www.python.org/downloads/">Python Download</a>
    </category>
</seealso>