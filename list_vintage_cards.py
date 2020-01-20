# usage: this makes a list of all cards currently legal in vintage, for use in a draft spreadsheet to highlight illegal picks
import json,util.cardparse as cardparse


with open("input/scryfall-default-cards.json", encoding="utf-8") as json_file:

    outf = open("output/vintage_cards.txt", 'w', encoding="utf-8")
    jsoutf = open("output/vintage_cards.js", 'w', encoding="utf-8")
    jsoutf.write("vintage_cards = [\n")
    data = json.load(json_file)
    i = 0
    cardseen = {}
    print("processing " + str(len(data)) + " cards")
    for card in data:
        if cardparse.legal_in_vintage(card):
            name = cardparse.cardname(card)
            if name not in cardseen:
                cardseen[name] = True
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
          
