# usage: just run it. it will get the latest card data from scryfall
#        and save it to input/scryfall-default-cards.json
#        Then it uploads it to the gsheet

import requests, urllib.request
import update_gsheets, list_vintage_cards

def get_data_url():
    r = requests.get("https://api.scryfall.com/bulk-data")

    for desc in r.json()["data"]:
        if desc["type"] == "default_cards":
            return desc["download_uri"]
    print(r.json())
    raise RuntimeError("Couldn't find default_cards in scryfall response")

if __name__ == '__main__':
    urllib.request.urlretrieve(get_data_url(), "input/scryfall-default-cards.json")
    list_vintage_cards.list_vintage_cards(include_later_banned_cards=True)
    update_gsheets.upload_vintage_cards()
