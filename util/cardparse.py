def legal_in_vintage(card):
    legal = card['legalities']['vintage']
    return legal == 'legal' or legal == 'restricted'

def cardname(card):
    name = card['name'].replace(u"û", "u").replace(u"ö", "o").replace(u"á", "a").replace(u"é", "e").replace(u"à", "a").replace(u"â", "a").replace(u"ú", "u").replace(u"í", "i")
    if card['layout'] == 'transform' or card['layout'] == 'flip' or card['layout'] == 'adventure':
        idx = name.find(" // ")
        if idx > -1:
            name = name[:idx]
    return name.lower()