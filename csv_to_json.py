import csv, json, os

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'MartinDex.csv')
out_path = os.path.join(base_dir, 'martindex.json')

pokemon = []
with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pokemon.append({
            'num':          row['Num'],
            'name':         row['Name'],
            'type1':        row['Type1'],
            'type2':        row['Type2'],
            'hp':           row['HP'],
            'attack':       row['Attack'],
            'defense':      row['Defense'],
            'spAtk':        row['SpAtk'],
            'spDef':        row['SpDef'],
            'speed':        row['Speed'],
            'generation':   row['Generation'],
            'legendary':    row['Legendary'],
            'ability1':     row.get('Ability1', ''),
            'ability2':     row.get('Ability2', ''),
            'hiddenAbility':row.get('HiddenAbility', ''),
        })

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(pokemon, f, separators=(',', ':'))

print(f"Done! Wrote {len(pokemon)} Pokémon to martindex.json")
