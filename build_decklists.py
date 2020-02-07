import json,util.cardparse as cardparse, os, glob, re


row_width = 26
json_file = open("input/scryfall-default-cards.json", "r", encoding="utf-8")

deck_lists_outf = open("output/decklists.txt", "w", encoding="utf-8")
out = ""
data = json.load(json_file)
cards_by_name = {}
for card in data:
    name = cardparse.cardname(card)
    cards_by_name[name] = card
    

inputdir = "input/decklists/"
cardlinepattern = re.compile("(\d+ )?(.*)")
for deckfilename in glob.glob(inputdir + "*.txt"):
    playername = deckfilename[len(inputdir):-len(".txt")]
    
    deckfile = open(deckfilename, "r")
    cardtypes = ["Lands", "Creatures", "Planeswalkers", "Artifacts", "Enchantments", "Instants", "Sorceries", "Other", "Sideboard"]
    cardlists = {}
    for type_ in cardtypes:
        cardlists[type_] = []

    in_Sideboard = False
    for line in deckfile:
        line = line.strip()
        if line:
            if line == "Sideboard:":
                in_Sideboard = True
                continue
            result = cardlinepattern.match(line)
            if not result:
                print("line in " + playername + ".txt doesn't have the right pattern: '" + line + "'")
                exit()
            
            count = result.group(1)
            if count:
                count = int(count)
            else:
                count = 1
              
            cardname = result.group(2)
            cardname = cardparse.simplify_name_characters(cardname).lower()
            if not cardname or cardname not in cards_by_name:
                print("unknown card in " + playername + ".txt: '" + cardname + "'")
                exit()
            card = cards_by_name[cardname]
            if "card_faces" in card and len(card["card_faces"]) > 1:
                card["mana_cost"] = card["card_faces"][0]["mana_cost"]
                #card["cmc"] = card["card_faces"][0]["cmc"]
            card["mycount"] = count
            type_line = card["type_line"]
            
            
            if in_Sideboard:
                cardlists["Sideboard"].append(card)
            elif "Land" in type_line:
                cardlists["Lands"].append(card)
            elif "Creature" in type_line:
                cardlists["Creatures"].append(card)
            elif "Planeswalker" in type_line:
                cardlists["Planeswalkers"].append(card)
            elif "Artifact" in type_line:
                cardlists["Artifacts"].append(card)
            elif "Enchantment" in type_line:
                cardlists["Enchantments"].append(card)
            elif "Instant" in type_line:
                cardlists["Instants"].append(card)
            elif "Sorcery" in type_line:
                cardlists["Sorceries"].append(card)
            else:
                cardlists["Other"].append(card)
    
    out += "\n" + playername
    for cardtype in cardtypes:
        clist = cardlists[cardtype]
        if len(clist) > 0:
            count_in_type = 0
            clist.sort(key=lambda c: c["name"])
            clist.sort(key=lambda c: c["mycount"])
            clist.sort(key=lambda c: c["cmc"])
            for card in clist:
                count = card["mycount"]
                count_in_type += count
                
            out += "\n" + cardtype + " (" + str(count_in_type) + ")\n"   
            
            for card in clist:
                displayname = cardparse.carddisplayname(card)
    
                cost = card["mana_cost"]
                cmc = card["cmc"]
                count = card["mycount"]
                cost = cost.replace("{", "")
                cost = cost.replace("}", "")
                cardline = displayname
                if len(cardline) + len(cost) >= row_width:
                    cutoff = row_width - len(cost) - 4
                    cardline = cardline[:cutoff] + "... "
                    
                padding = row_width - len(cardline) - len(cost)
                cardline += " " * padding
                cardline += cost
                if count > 1:
                    cardline = str(count) + " " + cardline
                out += cardline + "\n"

            

deck_lists_outf.write(out)
deck_lists_outf.close()

            
            
            
            
            
    
    