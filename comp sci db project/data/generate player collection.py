import sqlite3
import json
import random

conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()

cursor.execute("SELECT PlayerID FROM Player")
players = [x[0] for x in cursor.fetchall()]

cursor.execute("SELECT CardID FROM Card")
cards = [x[0] for x in cursor.fetchall()]


collection = []

for player in players:

    chance = random.random()

    if chance < 0.2:
        amount = random.randint(0, 15)       # brand new
    elif chance < 0.65:
        amount = random.randint(20, 80)      # casual
    elif chance < 0.9:
        amount = random.randint(80, 160)     # active
    else:
        amount = random.randint(160, 250)    # collectors

    owned = random.sample(cards, min(amount, len(cards)))

    for card in owned:

        roll = random.random()

        if roll < 0.75:
            qty = 1
        elif roll < 0.95:
            qty = 2
        elif roll < 0.99:
            qty = 3
        else:
            qty = 4

        collection.append({
            "PlayerID": player,
            "CardID": card,
            "Quantity": qty
        })


with open("player_collection.json", "w") as f:
    json.dump(collection, f, indent=4)


print("Generated", len(collection), "rows")