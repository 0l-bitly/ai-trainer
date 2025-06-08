import requests
import time

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
        if not item.get("private") and not item.get("archived") and not item.get("disabled") and item.get("license") is not None and item.get("language") is not None:
            filtered_item = {key: item[key] for key in fields if key in item}
            filtered.append(filtered_item)
    return filtered

def main(languages, keyword, token=None):
    repositories_data = []
    url = "https://api.github.com/search/repositories"
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    for language in languages:
        params = {
            "q": f"{keyword}+language:{language}",
            "sort": "stars",
            "order": "desc"
        }
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            repositories_data.extend(response.json().get('items', []))
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la recherche de dépôts pour {language}: {e}")
        time.sleep(1)
    repositories_data = clear(repositories_data)
    return repositories_data