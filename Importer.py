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
    
def import_cards():
    for filename in os.listdir("card data"):
        if filename.endswith(".json") and filename != "sets.json":
            print("importing", filename)
            
            with open ("card data/" + filename, encoding="utf-8") as file:
                cards = json.load(file)

            for card in cards:
                insert_set(card)
                insert_card(card)
    conn.commit()
    print("Card and CardSet import complete!")
    
def main():
    import_cards()
    conn.close()
    
    
main()        