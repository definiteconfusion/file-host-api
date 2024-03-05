import os
def details():
    detail = {
        "network":{
            "host":"127.0.0.1",
            "port":"3000"
        },
        "plugins":{
            "enabledPlugins":"",
            "allplugins":""
        },
        "database": "/Users/jakerase/Desktop/file-host-api/Data/files.db",
        "content":"/Users/jakerase/Desktop/file-host-api/Content",
        "plugins":"/Users/jakerase/Desktop/file-host-api/Plugins",
        "headerDirectory": os.getcwd()
    }
    return detail