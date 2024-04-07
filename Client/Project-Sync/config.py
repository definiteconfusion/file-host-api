import sys
import os

class basic:
    @staticmethod
    def details():
        detail = {
            ".ignore":[
                ".js"
            ]
        }
        return detail

class synthDetails:
    @staticmethod
    def op_sys():
        return sys.platform

    @staticmethod
    def os_spec_details():
        details = {
            "win":{
                "fileSeperator":"\\",
            },
            "darwin":{
                "fileSeperator": "/",
            }
        }
        return details
    @staticmethod
    def pack_name():
        full_dirLST = os.getcwd().split(synthDetails.os_spec_details()[synthDetails.op_sys()]["fileSeperator"])
        pack_dirSTR = full_dirLST[len(full_dirLST) - 1]
        return pack_dirSTR

    @staticmethod
    def header_dir():
        currDir = os.getcwd()
        header_dir = currDir.replace(f"/{synthDetails.pack_name()}", "") + '/'
        return header_dir
print(synthDetails.header_dir())