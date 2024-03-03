class httpResponses:
    def twohundred():
        return {"code":200,"response":"OK"}
    def fourhundred():
        return {"code":400,"response":"Bad Request"}
    def fourhundredthree():
        return {"code":403,"response":"Unauthorized"}