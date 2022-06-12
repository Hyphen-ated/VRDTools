import unidecode

def legal_in_vintage(card):
    legal = card['legalities']['vintage']
    return legal == 'legal' or legal == 'restricted'
    
def legal_in_modern(card):
    legal = card['legalities']['modern']
    return legal == 'legal'

layouts_to_ignore_back = ["transform", "flip", "adventure", "modal_dfc"]    
def cardname(card):
    name = card['name'].lower()
    name = simplify_name_characters(name)
    if card['layout'] in layouts_to_ignore_back:
        name = extract_first_card_name_only(name)
    return name

def carddisplayname(card):
    name = card['name']
    name = simplify_name_characters(name)
    if card['layout'] == 'transform' or card['layout'] == 'flip' or card['layout'] == 'adventure':
        name = extract_first_card_name_only(name)
    return name

def simplify_name_characters(name):
    return unidecode.unidecode(name)    

def extract_first_card_name_only(name):
    idx = name.find(" // ")
    if idx > -1:
        name = name[:idx]
    return name