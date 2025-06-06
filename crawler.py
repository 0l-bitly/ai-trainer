import requests

def main(languages, keyword):
    repositories_data = []
    url = "https://api.github.com/search/repositories"
    for language in languages:
        params = {
            "q": f"{keyword}+language:{language}",
            "sort": "stars",
            "order": "desc"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            repositories_data.extend(response.json().get('items', []))
        else:
            print(f"Erreur lors de la recherche de dépôts pour {language}: {response.status_code}")
    return repositories_data