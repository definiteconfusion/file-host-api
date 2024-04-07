class httpResponses:
    @staticmethod
    def twohundred():
        return {"code":200,"response":"OK"}

    @staticmethod
    def fourhundred():
        return {"code":400,"response":"Bad Request"}

    @staticmethod
    def fourhundredthree():
        return {"code":403,"response":"Unauthorized"}

    @staticmethod
    def fourhundredfour():
        return {"code":404,"response":"Not Found"}

    @staticmethod
    def fivehundred():
        return {"code":500,"response":"Internal Server Error"}

    @staticmethod
    def fourhundredeight():
        return {"code": 408, "response": "Request Timeout"}