# usage: just run it. it will get the latest card data from scryfall
#        and save it to input/scryfall-default-cards.json
#        Then it uploads it to the gsheet

import requests, urllib.request
import update_gsheets, list_vintage_cards
import os.path
from os import path

def get_data_url():
    
    r = requests.get("https://api.scryfall.com/bulk-data")

    for desc in r.json()["data"]:
        if desc["type"] == "default_cards":
            return desc["download_uri"]
    print(r.json())
    raise RuntimeError("Couldn't find default_cards in scryfall response")

if __name__ == '__main__':
    print("Getting bulk data URL...")
    data_url = get_data_url()
    print("Downloading new Scryfall data...")
    urllib.request.urlretrieve(data_url, "input/scryfall-default-cards.json")
    print("Processing new data locally...")
    list_vintage_cards.list_vintage_cards(include_later_banned_cards=True)
    if path.exists("input/gsheet_credentials.json"):
        print("Updating spreadsheet with card list...")
        update_gsheets.upload_vintage_cards()
    print("Done")
    
