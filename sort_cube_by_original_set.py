# Usage: put cube in input/cube.txt, 
#        then run this. it will sort the cards by set, put the sets in release order,
#        and put the result in "output/cube sorted by original set.txt"

import math, json, datetime,util.cardparse as cardparse
f = open("input/cube.txt", "r", encoding="utf-8")
          
      
playeridx = 0
draftidx = 0

date_format = "%Y-%m-%d"
carddict = {}
card_release_dates = {}
card_release_sets = {}
sets = {}

def new_set(name, date, fullname):
    set = {}
    set['name'] = name
    set['fullname'] = fullname
    set['date'] = date
    set['cards'] = []
    return set

with open("input/scryfall-default-cards.json", encoding="utf-8") as json_file:
    data = json.load(json_file)
    for card in data:
        if card['reprint'] is True:
            continue
        cardset = card['set']        
        name = cardparse.cardname(card)  
        
        
        carddatestr = card['released_at']        
        carddate = datetime.datetime.strptime(carddatestr, date_format)
        
        if name not in card_release_dates.keys() or card_release_dates[name] > carddatestr:
            card_release_dates[name] = carddatestr
            card_release_sets[name] = cardset
                                     
            if cardset not in sets:
                sets[cardset] = new_set(cardset, carddatestr, card['set_name'])
                
            if sets[cardset]['date'] != carddatestr:
                # if we already have a date for a set, and we find a different date for that set,
                # it means that set is goofy. 
                sets[cardset]['goofy'] = True  
                if sets[cardset]['date'] > carddatestr:
                    sets[cardset]['date'] = carddatestr
              
        carddict[name] = card        

for line in f:
    cardname = line.strip()
    set = card_release_sets[cardname.lower()]
    sets[set]['cards'].append(cardname)
f.close()    


outf = open("output/cube sorted by original set.txt", "w", encoding="utf-8")
print("Writing output/cube sorted by original set.txt")
for set in sorted(sets.items(), key=lambda s: s[1]['date']):
    set = set[1]
    if len(set['cards']) == 0:
        continue
    outf.write( set['name'].upper() + " -- " + set['fullname'] + " (" + str(len(set['cards'])) + "):\n")
    for card in sorted(set['cards']):
        outf.write(card + "\n")
    outf.write("\n")
            

outf.close()
print("Done")
    
        
    
