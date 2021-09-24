# usage: this lists cards with accents/weirdness in the names, and shows how they get mapped to ascii.
#        all the character mappings are done manually in cardparse. this thing also lists any names
#        that we don't know how to map. (which means adding handling in cardparse)
import json,util.cardparse as cardparse

include_later_banned_cards = False

with open("input/scryfall-default-cards.json", encoding="utf-8") as json_file:

    data = json.load(json_file)
    outf = open("output/funky_names.txt", 'w', encoding="utf-8")
    funky = set()
    unhandled = set()
    print("processing " + str(len(data)) + " cards")
    for card in data:
        name = card['name']
        simple = cardparse.simplify_name_characters(name.lower())
        if name.lower() != simple:
            funky.add(name + " -> " + simple)
        if not simple.isascii():
            unhandled.add(name)
            
    outf.write("Funky:\n")
    outf.write("\n".join(sorted(funky)))
    outf.write("\nUnhandled:\n")
    outf.write("\n".join(sorted(unhandled)))
    outf.write("\n")
    outf.close()
    print("Output to funky_names.txt, with " + str(len(funky)) + " funky and " + str(len(unhandled)) + " unhandled.")