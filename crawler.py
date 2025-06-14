import re
import requests
import time
import os
import subprocess
from datetime import datetime

def date():
    now = datetime.now()
    now = now.strftime("%Y:%m:%d:%H:%M")
    return now

def checklic(data, allowed_licenses):
    if isinstance(allowed_licenses[0], list):
        allowed_licenses = [item for sublist in allowed_licenses for item in sublist]
    cleaned_allowed_licenses = [re.sub(r'[\s\-.]', '', lic).lower() for lic in allowed_licenses]
    filtered_repositories = []
    for item in data:
        if item.get("license") is not None:
            cleaned_license_name = re.sub(r'[\s\-.]', '', item["license"]["name"]).lower()
            if cleaned_license_name in cleaned_allowed_licenses:
                filtered_repositories.append(item)
    return filtered_repositories

def addline(keyword, lang, number):
    with open('crawlog.list', 'a') as log:
        log.write(f"getrepos://keyword:{keyword} lang:{lang} nbr: {number} \n")

def clear(data):
    fields = [
        "id",
        "name",
        "private",
        "license",
        "archived",
        "disabled",
        "language",
        "clone_url",
        "default_branch"
    ]
    filtered = []
    for item in data:
        if (not item.get("private") and
            not item.get("archived") and
            not item.get("disabled") and
            item.get("license") is not None and
            item.get("language") is not None):
            filtered_item = {key: item[key] for key in fields if key in item}
            filtered.append(filtered_item)
    return filtered

def download(json):
    print("Downloading repositories.")
    print(json)
    print("Feature not implemented.")
    #execmd([])

def fetchrepos(langage, keyword, token=None):
    repositories_data = []
    url = "https://api.github.com/search/repositories"
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    params = {
        "q": f"{keyword}+language:{langage}",
        "sort": "stars",
        "order": "desc"
    }
    try:
        print(f"[+] Sending request to {url} with sort=stars&order=desc and language {langage}")
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"[-] Received response for language {langage}: {response.status_code}")
        if response.status_code == 403:
            input("[Err] Rate limit exceeded. Waiting before making more requests. Press enter to restart.")
        repositories_data.extend(response.json().get('items', []))
    except requests.exceptions.RequestException as e:
        print(f"[Err] Error searching repositories for {langage}: {e}")
    time.sleep(1)
    return repositories_data

def main(languages, keywords, allowed_licenses, token=None):

    if os.getenv("TRAINER_CRWL") == "False":
        print("[Warn] Crawl disabled. If you want to enable it, try python3 main.py config --crawl true")
        return None

    output, return_code = execmd(['ls', 'crawlog.list'])
    if return_code == 2:
        print("[Warn] crawlog.list does not exists. Create file.")
        execmd(['touch', 'crawlog.list'])
        with open('crawlog.list', 'a') as log:
            log.writelines(['Crawl log file.\n', f'Create date: {date()}\n', '----------------------------------- \n'])
    else:
        with open('crawlog.list', 'a') as log:
            log.writelines(['\n', '\n', f'Crawl session at {date()}\n', '----------------------------------- \n'])

    output=None
    return_code=None

    index = 1

    for keyword in keywords:
        for langage in languages:
            repositories_data = fetchrepos(langage, keyword, token)
            repositories_data = clear(repositories_data)
            filtered_repositories = checklic(repositories_data, allowed_licenses)
            print(filtered_repositories)
            addline(keyword, langage, index)
            index = index + 1

    print("Crawled successfuly !")

    if os.getenv('TRAINER_DOWN') == 'false':
        return filtered_repositories
    else:
        download(filtered_repositories)

def execmd(command):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout, 0
    except subprocess.CalledProcessError as e:
        print("Error :", e.stderr)
        return e.stderr, e.returncode
        