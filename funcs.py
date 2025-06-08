import random
import string
import json

def genrandstr(length):
    if length <= 0:
        return ""
    characters = string.ascii_lowercase + string.digits
    randstr = ''.join(random.choice(characters) for _ in range(length))
    return randstr

def printjson(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))