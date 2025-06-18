import requests
import argparse
import os
import json
import shutil
from crawler import main as crawl_main
from funcs import genrandstr
from funcs import printjson
from funcs import readkeywords
from funcs import parselic
from funcs import loading
from funcs import setenvvars
from funcs import printcfg
from funcs import parsecompilation
from funcs import getlangs

def main(configjsonpath='./cfg/config.json'):
    print("Démarrage de ai-trainer version 1.0.")
    config = loading(configjsonpath)
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
    parser.add_argument('--config_file', '-cfg', type=str, help='Custom config file path.')
    parser.add_argument('--compilation_config_file', type=str, help='Custom compilation config file path.')
    subparsers = parser.add_subparsers(dest='command')
    config_parser = subparsers.add_parser('config', help='Modify configuration')
    config_parser.add_argument('--output_name', type=str, help='Model name')
    config_parser.add_argument('--crawl', type=bool, help='Activate crawl')
    config_parser.add_argument('--git_path', type=str, help='Path to Git')
    config_parser.add_argument('--compile', type=bool, help='Activate compilation')
    config_parser.add_argument('--train', type=bool, help='Activate training')
    config_parser.add_argument('--outdir', type=str, help='Output directory')
    config_parser.add_argument('--sum', type=bool, help='Activate sums')
    config_parser.add_argument('--download', type=bool, help='Activate download')
    crawl_parser = subparsers.add_parser('crawl', help='Start crawl')
    crawl_parser.add_argument('--test', action='store_true', help='Start in test mode')
    crawl_parser.add_argument('--token', '-t', type=str, help='Github API Token for a better rate limit')
    crawl_parser.add_argument('--keywords', '-k', type=str, help='Keywords (file path)')
    args = parser.parse_args()

    if args.debug:
        os.environ['TRAINER_DBG'] = 'true'

    if args.compilation_config_file:
        compilationinfo = parsecompilation(args.compilation_config_file)
    else:
        compilationinfo = parsecompilation()

    if args.config_file:
        main(args.config_file)
    else:
        main()

    licensesdt = parselic()

    if args.command == 'config':
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

    if args.command == 'crawl':
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
            print("Mode: Main")
            try:
                print("Loading authorized programming langages.")
                langages = getlangs(compilationinfo, "langage")
            except Exception as e:
                print("ERROR: ", e)
            if args.keywords:
                keywordsfile = args.keywords
                keywords = readkeywords(keywordsfile)
                print(keywords)
            else:
                keywordsfile = "./keywords.txt"
                print("Keywords not specified. Using default.")
                keywords = readkeywords()
                print(keywords)
            print(f"Crawling main. Keywords file: {keywordsfile} API calls to: https://api.github.com/search/repositories Langages file: ./cfg/compilation.json")
            if args.token:
                crawl_main(langages, keywords, licensesdt, args.token)
            else:
                crawl_main(langages, keywords, licensesdt)