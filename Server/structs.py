def HTTP(code:int) -> dict:
    codes = {
        "200":{"code": 200, "response": "OK"},
        "400":{"code":400,"response":"Bad Request"},
        "403":{"code":403,"response":"Unauthorized"},
        "404":{"code":404,"response":"Not Found"},
        "408":{"code": 408, "response": "Request Timeout"}
    }
    return codes[str(code)]