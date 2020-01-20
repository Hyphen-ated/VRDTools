# Usage: put draft data in input/drafts.tsv, 
#        then run this. it will calculate a bunch of stuff and give you two files in output/, containing data for
#        card stats and seat stats, in the format expected for being pasted into my spreadsheet

import math, json, datetime, util.cardparse as cardparse
f = open("input/drafts.tsv", "r", encoding="utf-8")
      
playeridx = 0
draftidx = 0

cardwins = {}
cardlosses = {}
cardpicks = {}
winpows = {}
losspows = {}
seatwins = [0] * 8
seatlosses =[0] * 8
card_release_dates = {}
date_format = "%Y-%m-%d"

carddict = {}
with open("input/scryfall-default-cards.json", encoding="utf-8") as json_file:
    data = json.load(json_file)
    for card in data:
        if cardparse.legal_in_vintage(card):
            name = cardparse.cardname(card)
            carddict[name] = card
            
            #find the earliest date each card was released
            carddatestr = card['released_at']
            carddate = datetime.datetime.strptime(carddatestr, date_format)
            if name not in card_release_dates.keys() or card_release_dates[name] > carddate:
                card_release_dates[name] = carddate

current_draft_id = None
current_draft_date = None
current_line = 0
draft_dates = []
for line in f:    
    current_line += 1
    elems = line.rstrip().split("\t")
    draftinfo = elems[0] #  the draft id or date, on the first and second rows
    if playeridx == 0:
        if not draftinfo:
            raise Exception("Missing draft id and date on line " + str(current_line))
        infos = draftinfo.split(", ")
        if len(infos) != 2:
            raise Exception("Line " + str(current_line) + ": doesn't have draftid,date at the front")
        current_draft_id = infos[0]
        current_draft_date_str = infos[1]
        if not current_draft_id or not current_draft_date_str:
            raise Exception("Line " + str(current_line) + ": doesn't have draftid,date at the front")
        current_draft_date = datetime.datetime.strptime(current_draft_date_str, date_format)
        draft_dates.append(current_draft_date)        
        
    # elems[1] is player name        
    winstr = elems[2]
    lossstr = elems[3]
    wins = int(winstr) if len(winstr) > 0 else 0
    losses = int(lossstr) if len(lossstr) > 0 else 0
    
    seatwins[playeridx] += wins
    seatlosses[playeridx] += losses

    oddpick = True
    cardcount = 0
    for card in elems[4:]:
        card = card.strip()
        card = card.lower()
        if not card:
            continue
                
        if card_release_dates[card] > current_draft_date:
            raise Exception(card + " was released on " + card_release_dates[card] + " but " + current_draft_id + " happened on " + current_draft_date + " (the draft has the wrong legality date)")
                    
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

outf = open("output/card stats.tsv", "w", encoding="utf-8")
print("Writing output/card stats.tsv")
for (card, picks) in cardpicks.items():
    
    regularSum = 0
    sqInvSum = 0
    prioritySum = 0
    possiblePicks = 0

    release_date = card_release_dates[card]
    for draft_date in draft_dates:
        if release_date <= draft_date:
            possiblePicks += 1
    
    for num in picks:
        regularSum += num
        sqInvSum += (361 - num) * (361 - num)
        prioritySum += 1.0/num
    
    # each time it could have been picked and wasn't, it counts as being picked in spot 361
    for i in range(possiblePicks - len(picks)):
        regularSum += 361
        sqInvSum += 0
        prioritySum += 1.0/361
        
    avg = str((1.0 * regularSum) / possiblePicks)    
    avgSqInv =  str(361 - math.sqrt((1.0 * sqInvSum) / possiblePicks))
    
    carddata = carddict[card]
    cost = "-"
    if "mana_cost" in carddata:
        cost = carddata["mana_cost"]
                
    outp = card + "\t" +\
           str(len(picks)) + "\t" +\
           str(possiblePicks) + "\t" +\
           avg + "\t" +\
           avgSqInv + "\t" +\
           str(cardwins[card]) + "\t" +\
           str(cardlosses[card]) + "\t" +\
           str(winpows[card]) + "\t" +\
           str(losspows[card]) + "\t" +\
           cost + "\n"
           

    
    outf.write(outp)

outf.close()

seatoutf = open("output/seat stats.tsv", 'w', encoding="utf-8")
print("Writing output/seat stats.tsv")
for seatidx in range(8):
    seatoutf.write("seat " + str(seatidx+1) + "\t" + str(seatwins[seatidx]) + "\t" + str(seatlosses[seatidx]) + "\n")
seatoutf.close()

    
        
    
