import functions

def privateAuth(authToken:str, passkey:str):
    storedPsw = functions.sql.cmd(f"SELECT passkey FROM users WHERE token = '{authToken}'")
    if storedPsw == passkey:
        return True
    else:
        return False