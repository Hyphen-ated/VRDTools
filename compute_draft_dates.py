# Usage: put draft data in input/drafts.tsv (or run update_gsheets)
#        then run this. it will figure out the earliest each draft could have been, based on the release dates of the
#        cards, and output this to output/draft dates.tsv

import math, json, datetime,util.cardparse as cardparse
f = open("input/drafts.tsv", "r", encoding="utf-8")
          
      
playeridx = 0
draftidx = 0

date_format = "%Y-%m-%d"
carddict = {}
card_release_dates = {}
with open("input/scryfall-default-cards.json", encoding="utf-8") as json_file:
    data = json.load(json_file)
    for card in data:
        if cardparse.legal_in_vintage(card):
            name = cardparse.cardname(card)

        
            #find the earliest date each card was released
            carddatestr = card['released_at']            
            carddate = datetime.datetime.strptime(carddatestr, date_format)
            if name not in card_release_dates.keys() or card_release_dates[name] > carddate:
                card_release_dates[name] = carddate
            carddict[name] = card        

current_draft_id = None
current_draft_date = None
current_draft_cards = set()
current_line = 0

outf = open("output/draft dates.tsv", "w", encoding="utf-8")
print("Writing output/draft dates.tsv")
for line in f:
    current_line += 1
    elems = line.rstrip().split("\t")
    draftinfo = elems[0] #  the draft id or date, on the first and second rows
    if playeridx == 0:
        if not draftinfo:
            raise Exception("Missing draft id on line " + str(current_line))
                        
        current_draft_id = draftinfo
        outf.write(current_draft_id + "\t")
        
    elif playeridx == 1:
        current_draft_date = draftinfo
    # elems[1] is player name which I don't care about right now
    wins = int(elems[2]) if elems[2] else 0
    losses = int(elems[3]) if elems[3] else 0

    cardcount = 0
    for card in elems[4:]:
        card = card.strip()
        card = card.lower()
        if not card:
            continue
                    
        current_draft_cards.add(card)       

        cardcount += 1
           
    playeridx += 1
    if playeridx >= 8:
        playeridx = 0
        latest_date = datetime.datetime(1990, 1, 1)
        for card in current_draft_cards:
            if card_release_dates[card] > latest_date:
                latest_date = card_release_dates[card]
        outf.write(latest_date.strftime(date_format) + "\n")
        current_draft_cards.clear()
            



outf.close()

    
        
    
