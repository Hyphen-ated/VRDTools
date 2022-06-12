# usage: this makes a list of all cards currently legal in modern, for use in a draft spreadsheet to highlight illegal picks.
import json,util.cardparse as cardparse

def list_modern_cards():
    with open("input/scryfall-default-cards.json", encoding="utf-8") as json_file:

        outf = open("output/modern_cards.txt", 'w', encoding="utf-8")
        jsoutf = open("output/modern_cards.js", 'w', encoding="utf-8")
        jsoutf.write("modern_cards = [\n")
        data = json.load(json_file)
        i = 0
        cardseen = {}
        cardnames = []
        print("processing " + str(len(data)) + " cards")
        for card in data:
            if cardparse.legal_in_modern(card):
                name = cardparse.cardname(card)
                if name not in cardseen:
                    cardseen[name] = True
                    cardnames.append(name)
        
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
        print("Writing output/modern_cards.txt")
        print("Writing output/modern_cards.js")

if __name__ == '__main__':
    list_modern_cards()