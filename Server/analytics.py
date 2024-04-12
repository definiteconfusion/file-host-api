import functions
import datetime


class serverUtils:
    @staticmethod
    def startTime():
        return datetime.datetime.now()

    @staticmethod
    def endTime(startTime: datetime):
        return datetime.datetime.now() - startTime


def databaseEntry(token, processTime, readSpeed, ipAddr):
    try:
        functions.sql.cmd(
            f"INSERT INTO analyticData (email, processingTime, readSpeed, ipAddr) VALUES ('{token}', '{processTime}', '{readSpeed}', '{ipAddr}')")
        return True
    except Exception as e:
        print(e)
        return False
