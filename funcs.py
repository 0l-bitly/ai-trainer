import random
import string
import json
import os

def genrandstr(length):
    if length <= 0:
        return ""
    characters = string.ascii_lowercase + string.digits
    randstr = ''.join(random.choice(characters) for _ in range(length))
    return randstr

def printjson(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))

def readkeywords(filename='./keywords.txt'):
    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = [ligne.strip() for ligne in file.readlines()]
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"Error ocurred : {e}")
    
    return words

def parsecompilation(file_path="./cfg/compilation.json"):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"File {file_path} contains invalid JSON.")
        return None
    except PermissionError:
        print(f"Access denied to the file {file_path}")
        return None
    except Exception as e:
        print(f"Error : {e}")
        return None

def parselic(file_path='./cfg/licenses.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)
    free_licenses = []
    for license_name, is_free in data['licenses'].items():
        if is_free:
            free_licenses.append(license_name)
        else:
            pass
    return free_licenses

def loading(config_path):
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Le fichier de configuration {config_path} est introuvable.")
        exit(1)
    except json.JSONDecodeError:
        print("Erreur lors de la lecture du fichier de configuration.")
        exit(1)

def setenvvars(config):
    os.environ['TRAINER_OUTPUT_NAME'] = config.get('output_name', "model-01")
    os.environ['TRAINER_CRWL'] = str(config.get('crawl', False)).lower()
    os.environ['TRAINER_GIT_PATH'] = config.get('gitpath', '')
    os.environ['TRAINER_COMPILE'] = str(config.get('compile', False)).lower()
    os.environ['TRAINER_TRAIN'] = str(config.get('train', False)).lower()
    os.environ['TRAINER_OUTDIR'] = config.get('outdir', '')
    os.environ['TRAINER_SUM'] = str(config.get('sum', False)).lower()
    os.environ['TRAINER_DOWN'] = str(config.get('download', False)).lower()

def printcfg():
    if os.environ.get('TRAINER_DBG') == 'true':
        print("Configuration chargée avec succès.")
        print(f"OUTPUT_NAME: {os.environ.get('TRAINER_OUTPUT_NAME')}")
        print(f"TRAINER_CRWL: {os.environ.get('TRAINER_CRWL')}")
        print(f"TRAINER_GIT_PATH: {os.environ.get('TRAINER_GIT_PATH')}")
        print(f"TRAINER_COMPILE: {os.environ.get('TRAINER_COMPILE')}")
        print(f"TRAINER_TRAIN: {os.environ.get('TRAINER_TRAIN')}")
        print(f"TRAINER_OUTDIR: {os.environ.get('TRAINER_OUTDIR')}")
        print(f"TRAINER_SUM: {os.environ.get('TRAINER_SUM')}")
        print(f"TRAINER_DOWNLOAD: {os.environ.get('TRAINER_DOWN')}")

def getlangs(config_data, itemtoget):
    languages = []
    if config_data is not None and "compilables" in config_data:
        for item in config_data["compilables"]:
            language = item.get(itemtoget)
            if language:
                languages.append(language)
    return languages