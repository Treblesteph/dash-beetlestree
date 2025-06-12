import requests
import json
from wikidata_codes import codes
from scripts.cache import cache_get, cache_set

def get_wikidata_code(family_name):
    for entry in codes:
        if entry["family"].lower() == family_name.lower():
            return entry["wikidatacode"]
    return None


def get_wiki_pics_cached(family):
    key = f"wiki_pics:{family}"
    cached = cache_get(key)
    if cached: return cached

    result = get_wiki_pics(family)
    cache_set(key, result)
    return result


def get_wiki_pics(fam):

    fam_description = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{fam}").json()["extract"]

    code = get_wikidata_code(fam)
    endpoint = "https://query.wikidata.org/sparql"
    query = f"""
    SELECT ?taxon ?taxonLabel ?image WHERE {{
        ?taxon wdt:P171* wd:{code} .
        ?taxon wdt:P18 ?image .
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    """

    headers = {"Accept": "application/sparql-results+json"}
    response = requests.get(endpoint, params={"query": query}, headers=headers)
    data = response.json()

    pics = [
        {
            "species": item["taxonLabel"]["value"],
            "image_url": item["image"]["value"]
        }
        for item in data["results"]["bindings"]
    ]

    return fam_description, pics