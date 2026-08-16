import sqlite3
import json
import random

# Connect to database
conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()

# Load trades
with open("data/trades.json", "r") as f:
    trades = json.load(f)

# Get all existing cards from database
cursor.execute("SELECT CardID FROM Card")
card_ids = [row[0] for row in cursor.fetchall()]

print("Trades found:", len(trades))
print("Cards found:", len(card_ids))

if len(card_ids) == 0:
    print("No cards found. Check your database.")
    exit()

tradecards = []

for trade in trades:

    # Each trade has 2-5 different cards
    number_of_cards = random.randint(2, min(5, len(card_ids)))

    chosen_cards = random.sample(card_ids, number_of_cards)

    for card in chosen_cards:

        # Randomly decide who owns/gives the card
        owner = random.choice([
            trade["SenderID"],
            trade["ReceiverID"]
        ])

        tradecards.append({
            "TradeID": trade["TradeID"],
            "CardID": card,
            "Owner": owner,
            "Quantity": random.randint(1, 4)
        })


# Save JSON
with open("tradecard.json", "w") as f:
    json.dump(tradecards, f, indent=4)

print("Generated", len(tradecards), "TradeCard rows")

conn.close()