# usage: this makes a list of all cards currently legal in vintage, for use in a draft spreadsheet to highlight illegal picks.
#        some cards were banned in vintage after being picked in past drafts. if you're analyzing old data rather than running
#        a current draft, edit this file to set include_later_banned_cards = True, to include those cards
import json,util.cardparse as cardparse

include_later_banned_cards = False

with open("input/scryfall-default-cards.json", encoding="utf-8") as json_file:

    later_banned_file = open("cards-later-banned-in-vintage.txt", encoding="utf-8")
    outf = open("output/vintage_cards.txt", 'w', encoding="utf-8")
    jsoutf = open("output/vintage_cards.js", 'w', encoding="utf-8")
    jsoutf.write("vintage_cards = [\n")
    data = json.load(json_file)
    i = 0
    cardseen = {}
    cardnames = []
    print("processing " + str(len(data)) + " cards")
    for card in data:
        if cardparse.legal_in_vintage(card):
            name = cardparse.cardname(card)
            if name not in cardseen:
                cardseen[name] = True
                cardnames.append(name)                
    if include_later_banned_cards:
        for card in later_banned_file:
            try:
                name = card.rstrip()
                outf.write(name+'\n')
                unquotename = name.replace('"', '\\"')
                jsoutf.write('"' + unquotename + '",\n')
            except:
                print(name + " had a problem (from cards-later-banned-in-vintage.txt)")
        
    cardnames.sort()
    for name in cardnames:
        try:
            outf.write(name+'\n')
            unquotename = name.replace('"', '\\"')
            jsoutf.write('"' + unquotename + '",\n')
        except:
            print(name + " had a problem")
    
    jsoutf.write("];")
    outf.close()
    jsoutf.close()
    print("Writing output/vintage_cards.txt")
    print("Writing output/vintage_cards.js")          
          
