from random import choice
def generateToken():
    tokenLength=20
    toChoice="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    token="".join(choice(toChoice) for i in range(tokenLength)) 
    return token

def getUserFromToken(tokens, token):
    for key, value in zip(tokens.keys(),tokens.values()):
        if value == token:
            return key