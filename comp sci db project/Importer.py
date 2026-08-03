import sqlite3
import json
import os

conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")


with open("card data/sets.json", encoding="utf-8") as file:
    all_sets = json.load(file)
    
sets = {}
for s in all_sets:
    sets[s["id"]] = s


def insert_set(card):
    
    set_id = card["id"].split("-")[0]

    set_info = sets[set_id]
    

    cursor.execute("""
    INSERT OR IGNORE INTO CardSet VALUES (?,?,?,?)""",
    (set_info["id"], set_info["name"], set_info["series"], set_info["releaseDate"])
    )
    
def insert_card(card):
    if "supertype" not in card:
        print("no supertype")
    if card["supertype"] == "Pokémon":
        card_type = "Creature Card"
    elif card["supertype"] == "Trainer":
        card_type = "Trainer Card"
    elif card["supertype"] == "Energy":
        card_type = "Energy Card"
    else:
        return
    
    cursor.execute("""
    INSERT OR IGNORE INTO Card VALUES (?,?,?,?,?,?)""",
    (card["id"], card["id"].split("-")[0], card["name"], card_type, card["number"], card.get("rarity", "Unknown"))
    )

def insert_creature(card):

    stage = card.get("subtypes", ["Basic"])[0]
    if stage == "Basic":
        stage = "Basic pokemon"

    hp = int(card.get("hp", 0))

    element = card.get("types", ["Colorless"])[0]

    retreat = len(card.get("retreatCost", []))

    weakness = None
    if card.get("weaknesses"):
        weakness = card["weaknesses"][0]["type"]

    resistance = None
    if card.get("resistances"):
        resistance = card["resistances"][0]["type"]

    cursor.execute("""
    INSERT OR IGNORE INTO CreatureCard
    VALUES (?,?,?,?,?,?,?)
    """, (
        card["id"],
        stage,
        hp,
        element,
        retreat,
        weakness,
        resistance
    ))

def insert_trainer(card):

    subtype = card.get("subtypes", ["Item"])[0]

    if subtype == "Pokémon Tool":
        subtype = "Tool"

    rules = "\n".join(card.get("rules", []))

    cursor.execute("""
    INSERT OR IGNORE INTO TrainerCard
    VALUES (?,?,?)
    """,
    (
        card["id"],
        subtype,
        rules
    ))

def insert_energy(card):

    energy_type = card.get("subtypes", ["Basic"])[0]

    element = card.get("types", ["Colorless"])[0]

    special_effects = "\n".join(card.get("rules", []))

    cursor.execute("""
    INSERT OR IGNORE INTO EnergyCard
    VALUES (?,?,?,?)
    """, (
        card["id"],
        element,
        energy_type,
        special_effects
    ))

def insert_ability(card):

    if "abilities" not in card:
        return

    for i, ability in enumerate(card["abilities"], start=1):

        ability_id = f'{card["id"]}-AB{i}'

        cursor.execute("""
        INSERT OR IGNORE INTO CardAbility
        VALUES (?,?,?,?,?)
        """, (
            ability_id,
            card["id"],
            ability["name"],
            ability["type"],
            ability["text"]
        ))

def insert_attack(card):

    if "attacks" not in card:
        return

    for i, attack in enumerate(card["attacks"], start=1):

        attack_id = f'{card["id"]}-AT{i}'

        cursor.execute("""
        INSERT OR IGNORE INTO AttackDetails
        VALUES (?,?,?,?,?,?)
        """, (
            attack_id,
            card["id"],
            attack["name"],
            attack.get("damage", ""),
            len(attack.get("cost", [])),
            attack.get("text")
        ))

def insert_player(player):
    cursor.execute("""
    INSERT OR IGNORE INTO Player VALUES (?,?,?,?,?,?)
    """,
    (
        player["PlayerID"],
        player["Username"],
        player["DateJoined"],
        player["DateOfBirth"],
        player["PhoneNumber"],
        player["Email"]
    ))

def import_players():
    with open("player data/players.json", encoding="utf-8") as file:
        players = json.load(file)

    for player in players:
        insert_player(player)

    conn.commit()
    print("Player import complete!")

def import_cards():
    for filename in os.listdir("card data"):
        if filename.endswith(".json") and filename != "sets.json":
            print("importing", filename)

            with open("card data/" + filename, encoding="utf-8") as file:
                cards = json.load(file)

            for card in cards:
                insert_set(card)
                insert_card(card)

                supertype = card.get("supertype")

                if supertype == "Pokémon":
                    insert_creature(card)
                    insert_ability(card)
                    insert_attack(card)

                elif supertype == "Trainer":
                    insert_trainer(card)

                elif supertype == "Energy":
                    insert_energy(card)

    conn.commit()
    print("Card import complete!")
    
def main():
    import_cards()
    import_players()
    conn.close()
    
    
main()        