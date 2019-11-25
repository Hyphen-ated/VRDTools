import math, json
f = open("drafts.tsv", "r", encoding="utf-8")
      
playeridx = 0
draftidx = 0

cardwins = {}
cardlosses = {}
cardpicks = {}
winpows = {}
losspows = {}
seatwins = [0] * 8
seatlosses =[0] * 8

carddict = {}
with open("../scryfall-oracle-cards.json", encoding="utf-8") as json_file:
    data = json.load(json_file)
    for card in data:
        legal = card['legalities']['vintage']
        if ( legal == 'legal' or legal == 'restricted'):
            name = card['name'].replace(u"û", "u").replace(u"ö", "o").replace(u"á", "a").replace(u"é", "e").replace(u"à", "a").replace(u"â", "a").replace(u"ú", "u").replace(u"í", "i")
            if card['layout'] == 'transform' or card['layout'] == 'flip' or card['layout'] == 'adventure':
                idx = name.find(" // ")
                if idx > -1:
                    name = name[:idx]
            name = name.lower()
            carddict[name] = card        

for line in f:    
    elems = line.rstrip().split("\t")
    draftinfo = elems[1] #  the draft id or date, on the first and second rows
    wins = int(elems[2])
    losses = int(elems[3])
    seatwins[playeridx] += wins
    seatlosses[playeridx] += losses

    oddpick = True
    cardcount = 0
    for card in elems[4:]:
        card = card.strip()
        card = card.lower()
        if not card:
            continue
                    
        if card not in cardwins:
            cardwins[card] = wins
        else:
            cardwins[card] += wins

        if card not in cardlosses:
            cardlosses[card] = losses
        else:
            cardlosses[card] += losses

        if oddpick:
            pick = playeridx + 1 + cardcount * 8
        else:
            pick = (8 - playeridx) + cardcount * 8

        if card not in cardpicks:
            cardpicks[card] = [pick]
        else:
            cardpicks[card].append(pick)

        winpow = 1.0/(pick + 10) * wins
        losspow = 1.0/(pick + 10) * losses
        if card not in winpows:
            winpows[card] = winpow
        else:
            winpows[card] += winpow

        if card not in losspows:
            losspows[card] = losspow
        else:
            losspows[card] += losspow

        oddpick = not oddpick
        cardcount += 1
           
    playeridx += 1
    if playeridx >= 8:
        playeridx = 0

outf = open("card stats output.tsv", "w")
for (card, picks) in cardpicks.items():
    avg = str((1.0 * sum(picks)) / len(picks))

    sqInvSum = 0
    prioritySum = 0
    
    for num in picks:
        sqInvSum += (361 - num) * (361 - num)
        prioritySum += 1.0/num
        
    avgSqInv =  str(361 - math.sqrt((1.0 * sqInvSum) / len(picks)))
    
    carddata = carddict[card]
    cost = "-"
    if "mana_cost" in carddata:
        cost = carddata["mana_cost"]
    outp = card + "\t" +\
           str(len(picks)) + "\t" +\
           avg + "\t" +\
           avgSqInv + "\t" +\
           str(cardwins[card]) + "\t" +\
           str(cardlosses[card]) + "\t" +\
           str(winpows[card]) + "\t" +\
           str(losspows[card]) + "\t" +\
           cost + "\n"
           

    
    outf.write(outp)

outf.close()

seatoutf = open("seat stats output.tsv", 'w+')
for seatidx in range(8):
    seatoutf.write("seat " + str(seatidx) + "\t" + str(seatwins[seatidx]) + "\t" + str(seatlosses[seatidx]) + "\n")
seatoutf.close()

    
        
    
