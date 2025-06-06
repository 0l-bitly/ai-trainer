import requests
import argparse
import os
import json
from crawler import main as crawl_main

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
    os.environ['OUTPUT_NAME'] = config.get('output_name', "model-01")
    os.environ['CRWL'] = str(config.get('crawl', False)).lower()
    os.environ['GIT_PATH'] = config.get('gitpath', '')
    os.environ['COMPILE'] = str(config.get('compile', False)).lower()
    os.environ['TRAIN'] = str(config.get('train', False)).lower()
    os.environ['OUTDIR'] = config.get('outdir', '')
    os.environ['SUM'] = str(config.get('sum', False)).lower()

def printcfg():
    print("Configuration chargée avec succès.")
    print(f"OUTPUT_NAME: {os.environ['OUTPUT_NAME']}")
    print(f"CRWL: {os.environ['CRWL']}")
    print(f"GIT_PATH: {os.environ['GIT_PATH']}")
    print(f"COMPILE: {os.environ['COMPILE']}")
    print(f"TRAIN: {os.environ['TRAIN']}")
    print(f"OUTDIR: {os.environ['OUTDIR']}")
    print(f"SUM: {os.environ['SUM']}")

def main():
    print("Démarrage de ai-trainer version 1.0.")
    config = loading()
    setenvvars(config)
    printcfg()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Trainer Configuration")
    subparsers = parser.add_subparsers(dest='command')
    config_parser = subparsers.add_parser('config', help='Modifier la configuration')
    config_parser.add_argument('--output_name', type=str, help='Nom du modèle')
    config_parser.add_argument('--crawl', type=bool, help='Activer le crawl')
    config_parser.add_argument('--git_path', type=str, help='Chemin vers Git')
    config_parser.add_argument('--compile', type=bool, help='Activer la compilation')
    config_parser.add_argument('--train', type=bool, help='Activer l\'entraînement')
    config_parser.add_argument('--outdir', type=str, help='Répertoire de sortie')
    config_parser.add_argument('--sum', type=bool, help='Activer le résumé')
    crawl_parser = subparsers.add_parser('crawl', help='Lancer le crawl')
    crawl_parser.add_argument('--test', type=int, help='Lancer en mode test')
    args = parser.parse_args()

    if args.command == 'config':
        main()
        if args.output_name:
            os.environ['OUTPUT_NAME'] = args.output_name
        if args.crawl is not None:
            os.environ['CRWL'] = str(args.crawl).lower()
        if args.git_path:
            os.environ['GIT_PATH'] = args.git_path
        if args.compile is not None:
            os.environ['COMPILE'] = str(args.compile).lower()
        if args.train is not None:
            os.environ['TRAIN'] = str(args.train).lower()
        if args.outdir:
            os.environ['OUTDIR'] = args.outdir
        if args.sum is not None:
            os.environ['SUM'] = str(args.sum).lower()

    compilable_languages = loadlangs()
    print("Langages compilables :", compilable_languages)

    if args.command == 'crawl':
        main()
        print("Starting crawl.")
        #crawl_main()