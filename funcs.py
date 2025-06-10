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

def readkeywords(filename):
    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = [ligne.strip() for ligne in file.readlines()]
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"Error ocurred : {e}")
    
    return words