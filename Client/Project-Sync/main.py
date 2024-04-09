import functions
import config
import time

functions.setup()
lastFileContent = {}
currFileContent = {}
while True:
    files = functions.file_system.indexer(config.synthDetails.header_dir())
    for fileRead in range(len(files)):
        fileContent = functions.file_system.fileRead(f"{config.synthDetails.header_dir()}{files[fileRead]}")
        currFileContent[files[fileRead]] = fileContent
    # print("_-_" * 25)
    # print(currFileContent)
    # print(lastFileContent)
    # print(functions.fileDictCompare(currFileContent, lastFileContent))
    # print("_-_" * 25)
    isChanged = functions.fileDictCompare(currFileContent, lastFileContent)
    if isChanged:
        print(isChanged)
        functions.serverSync(files)
    lastFileContent = currFileContent
    currFileContent = {}
    time.sleep(5)