from scripts.get_wiki_pics import get_wiki_pics
from wikidata_codes import codes
from scripts.cache import cache_get, cache_set

def preload_all_images():
    for entry in codes:
        family = entry["family"]
        key = f"wiki_pics:{family}"

        if cache_get(key):
            print(f"[SKIP] {family} already cached.")
            continue

        try:
            print(f"[FETCH] Cacheing images for {family}")
            data = get_wiki_pics(family)
            cache_set(key, data, ttl=604800)
        except Exception as e:
            print(f"[ERROR] Failed for {family}: {e}")
