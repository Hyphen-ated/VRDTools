import math, json, datetime
f = open("drafts.tsv", "r", encoding="utf-8")
      
playeridx = 0
draftidx = 0

date_format = "%Y-%m-%d"
carddict = {}
card_release_dates = {}
with open("../scryfall-default-cards.json", encoding="utf-8") as json_file:
    data = json.load(json_file)
    for card in data:
        legal = card['legalities']['vintage']
        if legal == 'legal' or legal == 'restricted':
            name = card['name'].replace(u"û", "u").replace(u"ö", "o").replace(u"á", "a").replace(u"é", "e").replace(u"à", "a").replace(u"â", "a").replace(u"ú", "u").replace(u"í", "i")
            if card['layout'] == 'transform' or card['layout'] == 'flip' or card['layout'] == 'adventure':
                idx = name.find(" // ")
                if idx > -1:
                    name = name[:idx]
            name = name.lower()
            
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

outf = open("draft dates output.tsv", "w")
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
    wins = int(elems[2])
    losses = int(elems[3])

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

    
        
    
