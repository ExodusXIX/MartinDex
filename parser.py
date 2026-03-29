import csv
import os
 
pokedex = {}
pokedex_list = []
 
REGIONS = [
    (1,   151,  'Kanto'),
    (152, 251,  'Johto'),
    (252, 386,  'Hoenn'),
    (387, 493,  'Sinnoh'),
    (494, 649,  'Unova'),
    (650, 721,  'Kalos'),
    (722, 809,  'Alola'),
    (810, 905,  'Galar'),
    (906, 1025, 'Paldea'),
]
 
def get_region(num):
    try:
        n = int(num)
        for start, end, region in REGIONS:
            if start <= n <= end:
                return region
    except:
        pass
    return 'Special'
 
def load():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'MartinDex.csv')
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            has_abilities = 'Ability1' in row
            entry = {
                'num':           row['Num'],
                'name':          row['Name'],
                'type1':         row['Type1'],
                'type2':         row['Type2'],
                'hp':            row['HP'],
                'attack':        row['Attack'],
                'defense':       row['Defense'],
                'spAtk':         row['SpAtk'],
                'spDef':         row['SpDef'],
                'speed':         row['Speed'],
                'generation':    row['Generation'],
                'legendary':     row['Legendary'],
                'ability1':      row.get('Ability1', ''),
                'ability2':      row.get('Ability2', ''),
                'hiddenAbility': row.get('HiddenAbility', ''),
                'region':        get_region(row['Num']),
            }
            pokedex[row['Name'].lower()] = entry
            pokedex[row['Num']] = entry
            pokedex_list.append({
                'num':    row['Num'],
                'name':   row['Name'],
                'region': get_region(row['Num']),
            })
 
    # Sort: Kanto first then by num, Megas (high nums) go to their base region
    region_order = {r: i for i, (_, _, r) in enumerate(REGIONS)}
    region_order['Special'] = 99
    pokedex_list.sort(key=lambda x: (region_order.get(x['region'], 99), int(x['num'])))
 
def search(query):
    return pokedex.get(query.strip().lower()) or pokedex.get(query.strip())
 
def get_all():
    return pokedex_list
 
load()