import functions
import sys

def privateAuth(authToken:str):
    try:
        if functions.sql.cmd(f"SELECT userId FROM users WHERE userToken = '{authToken}'"):
            return True
        else:
            return sys.exit()
    
    except:
        return sys.exit()

def requestAuth(fileDetails:dict):
    screenedChars = [
        "'",
        '"',
        ";",
        "-",
        "\\",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "%",
        "_",
        "SELECT",
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "CREATE"
    ]
    for key in fileDetails:
        for chars in range(len(screenedChars)):
            if screenedChars[chars] in fileDetails[key]:
                return False
    return True