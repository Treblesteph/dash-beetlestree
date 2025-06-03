import requests
from bs4 import BeautifulSoup


def get_naturespot_imgs(fam):
    species_imgs = []

    img_page_url = "https://www.naturespot.org/family/"
    fam_url = img_page_url + fam
    response = requests.get(fam_url)

    if response.status_code == 404: return species_imgs
    
    soup = BeautifulSoup(response.text, 'html.parser')
    item_list_div = soup.find("div", class_="item-list")
    
    if not item_list_div: return species_imgs

    li_blocks = item_list_div.find_all("li")

    for li in li_blocks:
        link = li.find("a", href=True)
        img = link.find("img", attrs={"data-src": True}) if link else None
        
        if link and img and "species" in link["href"]:
            species_url = link["href"]
            image_url = img["data-src"]

            if species_url.startswith("/species/"):
                species_name = species_url.split("/species/")[-1]
                species_imgs.append({
                    "species": species_name,
                    "image_url": image_url
                })

    return species_imgs