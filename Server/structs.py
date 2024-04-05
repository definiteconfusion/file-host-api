class httpResponses:
    def twohundred():
        return {"code":200,"response":"OK"}
    def fourhundred():
        return {"code":400,"response":"Bad Request"}
    def fourhundredthree():
        return {"code":403,"response":"Unauthorized"}
    def fourhundredfour():
        return {"code":404,"response":"Not Found"}
    def fivehundred():
        return {"code":500,"response":"Internal Server Error"}
    def fourhundredeight():
        return {"code": 408, "response": "Request Timeout"}