from config import details
import sqlite3
import random


class sql:
    def cmd(command:str) -> str:
        database = details()["database"]
        init = sqlite3.connect(f'{database}')
        cursor = init.cursor()
        cursor.execute(f"{command}")
        if "SELECT" in command:
            type_result = cursor.fetchall()
        elif "PRAGMA" in command:
            type_result = cursor.fetchall()
        else:
            type_result = "ENDED IN ELSE"
            init.commit()
        return type_result

def idGen():
    neoid = ""
    chars = ["a", "b", "c", "d", "e", "f", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for idchars in range(10):
        neoid = neoid + chars[random.randint(0, 14)]
    return neoid
