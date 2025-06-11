import requests
import argparse
import os
import json
import shutil
from crawler import main as crawl_main
from funcs import genrandstr
from funcs import printjson
from funcs import readkeywords

def parselic(file_path='./cfg/licenses.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)
    free_licenses = []
    non_free_licenses = []
    for license_name, is_free in data['licenses'].items():
        if is_free:
            free_licenses.append(license_name)
        else:
            non_free_licenses.append(license_name)
    return free_licenses, non_free_licenses

def loading(config_path='./cfg/config.json'):
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Le fichier de configuration {config_path} est introuvable.")
        exit(1)
    except json.JSONDecodeError:
        print("Erreur lors de la lecture du fichier de configuration.")
        exit(1)

def loadlangs(file_path='./cfg/compilables.json'):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return [(lang['language'], lang['extension']) for lang in data['compilables']]
    except FileNotFoundError:
        print(f"Le fichier {file_path} est introuvable.")
        return []
    except json.JSONDecodeError:
        print("Erreur lors de la lecture du fichier de langages compilables.")
        return []

def setenvvars(config):
    os.environ['TRAINER_TRAINER_OUTPUT_NAME'] = config.get('output_name', "model-01")
    os.environ['TRAINER_CRWL'] = str(config.get('crawl', False)).lower()
    os.environ['TRAINER_GIT_PATH'] = config.get('gitpath', '')
    os.environ['TRAINER_COMPILE'] = str(config.get('compile', False)).lower()
    os.environ['TRAINER_TRAIN'] = str(config.get('train', False)).lower()
    os.environ['TRAINER_OUTDIR'] = config.get('outdir', '')
    os.environ['TRAINER_SUM'] = str(config.get('sum', False)).lower()
    os.environ['TRAINER_DOWN'] = str(config.get('download', False)).lower()

def printcfg():
    if os.environ.get('TRAINER_DBG') == 'True':
        print("Configuration chargée avec succès.")
        print(f"OUTPUT_NAME: {os.environ.get('TRAINER_OUTPUT_NAME')}")
        print(f"TRAINER_CRWL: {os.environ.get('TRAINER_CRWL')}")
        print(f"TRAINER_GIT_PATH: {os.environ.get('TRAINER_GIT_PATH')}")
        print(f"TRAINER_COMPILE: {os.environ.get('TRAINER_COMPILE')}")
        print(f"TRAINER_TRAIN: {os.environ.get('TRAINER_TRAIN')}")
        print(f"TRAINER_OUTDIR: {os.environ.get('TRAINER_OUTDIR')}")
        print(f"TRAINER_SUM: {os.environ.get('TRAINER_SUM')}")
        print(f"TRAINER_DOWNLOAD: {os.environ.get('TRAINER_DOWN')}")

def main():
    print("Démarrage de ai-trainer version 1.0.")
    config = loading()
    setenvvars(config)
    printcfg()

def init():
    if shutil.which("git") is None:
        print("Warning: Git not found. The repositories could not be downloaded.")
        print("Setting download to false.")
        os.environ['DOWN'] = str(False).lower()
        print("Setted download to false.")
    else:
        print("Git verification O.K.")

if __name__ == "__main__":
    init()
    parser = argparse.ArgumentParser(description="AI Trainer Configuration")
    parser.add_argument('--debug', '-d', action='store_true', help='Run in debug mode.')
    subparsers = parser.add_subparsers(dest='command')
    config_parser = subparsers.add_parser('config', help='Modifier la configuration')
    config_parser.add_argument('--output_name', type=str, help='Nom du modèle')
    config_parser.add_argument('--crawl', type=bool, help='Activer le crawl')
    config_parser.add_argument('--git_path', type=str, help='Chemin vers Git')
    config_parser.add_argument('--compile', type=bool, help='Activer la compilation')
    config_parser.add_argument('--train', type=bool, help='Activer l\'entraînement')
    config_parser.add_argument('--outdir', type=str, help='Répertoire de sortie')
    config_parser.add_argument('--sum', type=bool, help='Activer le résumé')
    config_parser.add_argument('--download', type=bool, help='Activer le téléchargement')
    crawl_parser = subparsers.add_parser('crawl', help='Lancer le crawl')
    crawl_parser.add_argument('--test', action='store_true', help='Lancer en mode test')
    crawl_parser.add_argument('--token', '-t', type=str, help='Github API Token pour une meilleure rate limit')
    crawl_parser.add_argument('--keywords', '-k', type=str, help='Mots-clés de recherche (chemin de fichiers de mots-clés)')
    args = parser.parse_args()

    if args.debug:
        os.environ['TRAINER-DBG'] = True

    if args.command == 'config':
        main()
        if args.output_name:
            os.environ['TRAINER_OUTPUT_NAME'] = args.output_name
        if args.crawl is not None:
            os.environ['TRAINER_CRWL'] = str(args.crawl).lower()
        if args.git_path:
            os.environ['TRAINER_GIT_PATH'] = args.git_path
        if args.compile is not None:
            os.environ['TRAINER_COMPILE'] = str(args.compile).lower()
        if args.train is not None:
            os.environ['TRAINER_TRAIN'] = str(args.train).lower()
        if args.outdir:
            os.environ['TRAINER_OUTDIR'] = args.outdir
        if args.sum is not None:
            os.environ['TRAINER_SUM'] = str(args.sum).lower()
    licensesdt = parselic()
    compilable_languages = loadlangs()
    if args.command == 'crawl':
        main()
        print("Starting crawl.")
        if args.test:
            print("Mode: Test")
            if args.token:
                sol = crawl_main("github", ["python"], licensesdt, args.token)
            else:
                sol = crawl_parser("github", ["python"], licensesdt)
            if sol is None:
                os.exit(0)
            printjson(sol)
        else:
            if args.keywords or args.k:
                keywords = readkeywords(args.keywords or args.k)
                print(keywords)                
            print(f"Crawling main. File: {keywords} API calls to: https://api.github.com/search/repositories ")
            #crawl_main()