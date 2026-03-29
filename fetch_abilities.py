import csv
import urllib.request
import json
import time
import os

NAME_OVERRIDES = {
    "Farfetch_d": "farfetchd",
    "Sirfetch_d": "sirfetchd",
    "Ho Oh": "ho-oh",
    "Chi Yu": "chi-yu",
    "Chien Pao": "chien-pao",
    "Ting Lu": "ting-lu",
    "Wo Chien": "wo-chien",
    "Hakamo O": "hakamo-o",
    "Jangmo O": "jangmo-o",
    "Kommo O": "kommo-o",
    "Porygon 2": "porygon2",
    "Porygon Z": "porygon-z",
    "Mr Mime": "mr-mime",
    "Mr Rime": "mr-rime",
    "Mime Jr": "mime-jr",
    "Type Null": "type-null",
    "Tapu Koko": "tapu-koko",
    "Tapu Lele": "tapu-lele",
    "Tapu Bulu": "tapu-bulu",
    "Tapu Fini": "tapu-fini",
    "Great Tusk": "great-tusk",
    "Brute Bonnet": "brute-bonnet",
    "Flutter Mane": "flutter-mane",
    "Slither Wing": "slither-wing",
    "Sandy Shocks": "sandy-shocks",
    "Iron Treads": "iron-treads",
    "Iron Bundle": "iron-bundle",
    "Iron Hands": "iron-hands",
    "Iron Jugulis": "iron-jugulis",
    "Iron Moth": "iron-moth",
    "Iron Thorns": "iron-thorns",
    "Iron Valiant": "iron-valiant",
    "Iron Leaves": "iron-leaves",
    "Iron Crown": "iron-crown",
    "Roaring Moon": "roaring-moon",
    "Walking Wake": "walking-wake",
    "Raging Bolt": "raging-bolt",
    "Scream Tail": "scream-tail",
    "Gouging Fire": "gouging-fire",
    "Paldean Wooper": "wooper-paldea",
    "Koraidon": "koraidon",
    "Miraidon": "miraidon",
    "Terapagos": "terapagos",
    "Pecharunt": "pecharunt",
    "Munkidori": "munkidori",
    "Fezandipiti": "fezandipiti",
    "Okidogi": "okidogi",
    "Ogerpon": "ogerpon-teal-mask",
    "Basculegion": "basculegion-male",
    "Basculin": "basculin-red-striped",
    "Aegislash": "aegislash-shield",
    "Gourgeist": "gourgeist-average",
    "Giratina": "giratina-altered",
    "Frillish": "frillish-male",
    "Enamorus": "enamorus-incarnate",
    "Eiscue": "eiscue-ice",
    "Deoxys": "deoxys-normal",
    "Darmanitan": "darmanitan-standard",
    "Maushold": "maushold-family-of-three",
    "Lycanroc Midday": "lycanroc-midday",
    "Landorus": "landorus-incarnate",
    "Keldeo": "keldeo-ordinary",
    "Jellicent": "jellicent-male",
    "Indeedee": "indeedee-male",
    "Morpeko": "morpeko-full-belly",
    "Minior": "minior-red-meteor",
    "Mimikyu": "mimikyu-disguised",
    "Meowstic": "meowstic-male",
    "Palafin": "palafin-zero",
    "Oricorio Baile": "oricorio-baile",
    "Oinkologne": "oinkologne-male",
    "Nidoran": "nidoran-f",
    "Pyroar": "pyroar-male",
    "Pumpkaboo": "pumpkaboo-average",
    "Shaymin": "shaymin-land",
    "Squawkabilly": "squawkabilly-green-plumage",
    "Zygarde": "zygarde-50",
    "Wormadam": "wormadam-plant",
    "Wishiwashi": "wishiwashi-solo",
    "Urshifu": "urshifu-single-strike",
    "Toxtricity": "toxtricity-amped",
    "Tornadus": "tornadus-incarnate",
    "Thundurus": "thundurus-incarnate",
    "Hoopa Hoopa": "hoopa",
    "Calyrex": "calyrex",
}

MEGA_BASE = {
    "Mega Abomasnow": "abomasnow", "Mega Absol": "absol", "Mega Aerodactyl": "aerodactyl",
    "Mega Aggron": "aggron", "Mega Alakazam": "alakazam", "Mega Altaria": "altaria",
    "Mega Ampharos": "ampharos", "Mega Audino": "audino", "Mega Banette": "banette",
    "Mega Beedrill": "beedrill", "Mega Blastoise": "blastoise", "Mega Blaziken": "blaziken",
    "Mega Camerupt": "camerupt", "Mega Charizard X": "charizard", "Mega Charizard Y": "charizard",
    "Mega Diancie": "diancie", "Mega Gallade": "gallade", "Mega Garchomp": "garchomp",
    "Mega Gardevoir": "gardevoir", "Mega Gengar": "gengar", "Mega Glalie": "glalie",
    "Mega Gyarados": "gyarados", "Mega Heracross": "heracross", "Mega Houndoom": "houndoom",
    "Mega Kangaskhan": "kangaskhan", "Mega Latias": "latias", "Mega Latios": "latios",
    "Mega Lopunny": "lopunny", "Mega Lucario": "lucario", "Mega Manectric": "manectric",
    "Mega Mawile": "mawile", "Mega Medicham": "medicham", "Mega Metagross": "metagross",
    "Mega Mewtwo X": "mewtwo", "Mega Mewtwo Y": "mewtwo", "Mega Pidgeot": "pidgeot",
    "Mega Pinsir": "pinsir", "Mega Rayquaza": "rayquaza", "Mega Sableye": "sableye",
    "Mega Salamence": "salamence", "Mega Sceptile": "sceptile", "Mega Scizor": "scizor",
    "Mega Sharpedo": "sharpedo", "Mega Slowbro": "slowbro", "Mega Steelix": "steelix",
    "Mega Swampert": "swampert", "Mega Tyranitar": "tyranitar", "Mega Venusaur": "venusaur",
}

def to_slug(name):
    """Simple, reliable slug — exact match first, then fallback."""
    if name in MEGA_BASE:
        return MEGA_BASE[name]
    if name in NAME_OVERRIDES:
        return NAME_OVERRIDES[name]
    # Generic fallback: lowercase, spaces to hyphens
    return name.lower().replace(' ', '-').replace('_', '')

def fetch_abilities(slug):
    url = f"https://pokeapi.co/api/v2/pokemon/{slug}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'MartinDex/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        abilities = {'ability1': '', 'ability2': '', 'hidden_ability': ''}
        for a in data['abilities']:
            raw = a['ability']['name'].replace('-', ' ').title()
            if a['is_hidden']:
                abilities['hidden_ability'] = raw
            elif a['slot'] == 1:
                abilities['ability1'] = raw
            elif a['slot'] == 2:
                abilities['ability2'] = raw
        return abilities
    except Exception as e:
        print(f"  ERROR fetching {slug}: {e}")
        return None

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    in_path = os.path.join(base_dir, 'MartinDex.csv')

    with open(in_path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    has_abilities = 'Ability1' in rows[0]
    fieldnames = list(rows[0].keys())
    if not has_abilities:
        fieldnames += ['Ability1', 'Ability2', 'HiddenAbility']

    updated = []
    errors = []
    total = len(rows)

    for i, row in enumerate(rows):
        name = row['Name']
        # Skip if already populated
        if has_abilities and row.get('Ability1', '').strip():
            updated.append(row)
            print(f"[{i+1}/{total}] {name} — skipped")
            continue

        slug = to_slug(name)
        print(f"[{i+1}/{total}] {name} -> {slug}")
        abilities = fetch_abilities(slug)
        if abilities:
            row['Ability1'] = abilities['ability1']
            row['Ability2'] = abilities['ability2']
            row['HiddenAbility'] = abilities['hidden_ability']
        else:
            row.setdefault('Ability1', '')
            row.setdefault('Ability2', '')
            row.setdefault('HiddenAbility', '')
            errors.append(name)
        updated.append(row)
        time.sleep(0.25)

    with open(in_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated)

    print(f"\nDone! Saved to {in_path}")
    if errors:
        print(f"\nStill failed ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")

if __name__ == '__main__':
    main()