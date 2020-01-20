# usage: this is for figuring out which cards you need to print for a VRD, and which ones you need to pull from
#        your cube or your cube sideboard.
#        in input/, put "draft.txt", "cube.txt", "cube sideboard.txt" each containing one card per line.
#        (ignore cube sideboard if you don't have one)
#        then run this and you'll get three output files:
#        pull lists.txt has your cards sorted by cube/sideboard and by color, to help you pull all those cards out
#        toprint.txt has a list of all the cards you need to print
#        toprint.html has links to scryfall that'll show you all the printings of each card, to make it more convenient
#                     for you to decide which printing to use

import json,util.cardparse as cardparse, os

json_file = open("input/scryfall-default-cards.json", "r", encoding="utf-8")
pull_lists_outf = open("output/pull lists.txt", "w", encoding="utf-8")
out = ""
data = json.load(json_file)
cards_by_name = {}
for card in data:
    name = cardparse.cardname(card)
    cards_by_name[name] = card
    
    

cubecards = {}
if os.path.isfile("input/cube.txt"):
    cubef = open("input/cube.txt", "r", encoding="utf-8")
    for card in cubef:
        card = card.strip().lower()
        if card not in cards_by_name:
            print(card + " is in cube but not in scryfall cards")
        else:
            cubecards[card] = True


sideboardcards = {}
if os.path.isfile("input/cube sideboard.txt"):
    sideboardf = open("input/cube sideboard.txt", "r", encoding="utf-8")
    for card in sideboardf:
        card = card.strip().lower()
        if card not in cards_by_name:
            print(card + " is in cube sideboard but not in scryfall cards")
        else:
            sideboardcards[card] = True

toprintcards = {}        
        
draftf = open("input/draft.txt", "r", encoding="utf-8")
draft = {}
cats = ["White", "Blue", "Black", "Red", "Green", "Multi", "Colorless", "Lands"]   
pulls = {}
pulltypes = ["Cube", "Sideboard", "Print"]
for puller in pulltypes:
    pulls[puller] = {}
    
for cat in cats:
    for puller in pulltypes:
        pulls[puller][cat] = []

for line in draftf:    
    for card in line.split("\t"):
        card = card.strip().lower()
        if len(card) > 0:
            if card not in cards_by_name:
                print(card + " is in draft but not in scryfall cards")
            else:

                if card in cubecards:
                    puller = "Cube"
                elif card in sideboardcards:
                    puller = "Sideboard"
                else:
                    puller = "Print"
                    toprintcards[card] = True
                    
                c = cards_by_name[card]
                if c["layout"] == "transform":
                    colors = c["card_faces"][0]["colors"]
                else:
                    colors = c["colors"]                     
                if len(colors) == 0:
                    if "Land" in  c["type_line"]:
                        pulls[puller]["Lands"].append(card)
                    else:
                        pulls[puller]["Colorless"].append(card)
                elif len(colors) > 1:
                    pulls[puller]["Multi"].append(card)
                elif "W" in colors:
                    pulls[puller]["White"].append(card)
                elif "U" in colors:
                    pulls[puller]["Blue"].append(card)
                elif "B" in colors:
                    pulls[puller]["Black"].append(card)
                elif "R" in colors:
                    pulls[puller]["Red"].append(card)
                elif "G" in colors:
                    pulls[puller]["Green"].append(card)

for puller, pullval in pulls.items():
    pull_lists_outf.write("------" + puller + "------\n")
    for cat in cats:
        catval = pullval[cat]
        catval.sort()
        pull_lists_outf.write("---" + cat + "---\n")
        pull_lists_outf.writelines("%s\n" % card for card in catval)
        pull_lists_outf.write("\n\n")

pull_lists_outf.close()
print("Writing output/pull lists.txt")

htmloutf = open("output/toprint.html", "w", encoding="utf-8")
print("Writing output/toprint.html")
toprintoutf = open("output/toprint.txt", "w", encoding="utf-8")
print("Writing output/toprint.txt")

htmloutf.write("<html>")   


url_pattern = "https://scryfall.com/search?q=oracleid%3A$ORACLEID&order=released&dir=asc&as=grid&unique=prints"

for card in toprintcards:
    toprintoutf.write(card+"\n")

    oracleid = cards_by_name[card]["oracle_id"]
    url = url_pattern.replace("$ORACLEID", oracleid)
    htmloutf.write("<a href=\"" + url + "\">" + card + "</a><br>\n")

htmloutf.write("</html>")
htmloutf.close()
toprintoutf.close()
                

        
    
