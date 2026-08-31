from ast import Try
import sqlite3
import sys
import os
import datetime
from datetime import date

sqlite3.register_adapter(datetime.date, lambda val: val.isoformat())
sqlite3.register_adapter(datetime.datetime, lambda val: val.isoformat())


conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

def print_as_table(cursor, data):
    # 1. Handle case where no data is found
    if data is None or data == []:
        print("\nNo data found.")
        return
    
    # 2. Automatically normalize single records into a list
    # If 'data' is a single tuple (one record), wrap it in a list
    if isinstance(data, tuple):
        records = [data]
    else:
        records = data

    # 3. Extract headers from the cursor
    headers = [col[0] for col in cursor.description]

    # 4. Calculate dynamic column widths across ALL records and headers
    col_widths = []
    for col_idx, header in enumerate(headers):
        max_len = len(header)
        for row in records:
            # Check the length of the string version of each cell
            max_len = max(max_len, len(str(row[col_idx])))
        col_widths.append(max_len + 4)  # Add padding

    # 5. Create the formatting template
    format_template = "".join([f"{{:<{w}}}" for w in col_widths])

    # 6. Print the table structure and data
    print("\n" + "=" * sum(col_widths))
    print(format_template.format(*headers))
    print("-" * sum(col_widths))
    
    for row in records:
        row_strings = [str(item) for item in row]
        print(format_template.format(*row_strings))
        
    print("=" * sum(col_widths))

cursor.execute("""
SELECT Deck.DeckID, Deck.DeckName, Player.Username, 
SUM(CardInDeck.Quantity) AS 'Total Cards',
COUNT(CardInDeck.CardID) AS 'Unique Cards', 
SUM(CASE WHEN Card.CardType = 'Creature Card' THEN CardInDeck.Quantity ELSE 0 END) AS 'Creature Cards',
SUM(CASE WHEN Card.CardType = 'Trainer Card' THEN CardInDeck.Quantity ELSE 0 END) AS 'Trainer Cards',
SUM(CASE WHEN Card.CardType = 'Energy Card' THEN CardInDeck.Quantity ELSE 0 END) AS 'Energy Cards'
FROM Deck
JOIN Player ON Player.PlayerID = Deck.PlayerID
JOIN CardInDeck ON CardInDeck.DeckID = Deck.DeckID
JOIN Card ON Card.CardID = CardInDeck.CardID
WHERE Deck.deckid = 'D001'""")

deck_stats = cursor.fetchone()
print_as_table(cursor, deck_stats)

