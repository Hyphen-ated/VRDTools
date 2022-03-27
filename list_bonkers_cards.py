# usage: this makes lists of conspiracies, heroes, and vanguard avatars

import json,util.cardparse as cardparse

def list_bonkers_cards():
    with open("input/scryfall-default-cards.json", encoding="utf-8") as json_file:

        later_banned_file = open("cards-later-banned-in-vintage.txt", encoding="utf-8")
        conspiracy_f = open("output/conspiracy_cards.txt", 'w', encoding="utf-8")
        hero_f = open("output/hero_cards.txt", 'w', encoding="utf-8")
        avatar_f = open("output/avatar_cards.txt", 'w', encoding="utf-8")

        data = json.load(json_file)
        i = 0
        cardseen = {}
        cardnames = []
        print("processing " + str(len(data)) + " cards")
        for card in data:
            name = cardparse.cardname(card)
            if name not in cardseen:                
                cardseen[name] = True                
                if "type_line" in card:
                    if card["type_line"].startswith("Hero"):
                        hero_f.write(name+'\n')
                    elif card["type_line"].startswith("Conspiracy"):
                        conspiracy_f.write(name+'\n')
                    elif card["type_line"].startswith("Vanguard"):
                        avatar_f.write(name+'\n')
                                           
        conspiracy_f.close()
        hero_f.close()
        avatar_f.close()

        print("Writing output/conspiracy_cards.txt")
        print("Writing output/hero_cards.js")
        print("Writing output/avatar_cards.js")

if __name__ == '__main__':
    list_bonkers_cards()