import json
import random
import sqlite3

conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()

# Existing decks
cursor.execute("SELECT DeckID FROM Deck")
decks = [row[0] for row in cursor.fetchall()]

# Existing cards
cursor.execute("SELECT CardID FROM Card")
cards = [row[0] for row in cursor.fetchall()]

print("Decks found:", len(decks))
print("Cards found:", len(cards))
print("Example decks:", decks[:5])
print("Example cards:", cards[:5])

cardindeck = []

for deck in decks:

    # number of unique cards in this deck
    unique_cards = random.randint(20, 30)

    chosen_cards = random.sample(
        cards,
        unique_cards
    )

    total = 0

    for card in chosen_cards:

        # stop around 60 cards
        if total >= 60:
            break

        quantity = random.randint(1,4)

        # don't exceed 60
        if total + quantity > 60:
            quantity = 60 - total

        cardindeck.append({
            "DeckID": deck,
            "CardID": card,
            "Quantity": quantity
        })

        total += quantity


with open("cardindeck.json", "w") as f:
    json.dump(cardindeck, f, indent=4)


print(
    f"Generated {len(cardindeck)} CardInDeck rows"
)