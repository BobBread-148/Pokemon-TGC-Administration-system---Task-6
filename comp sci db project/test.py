import sqlite3
import sys
import os

conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("SELECT PlayerID, Username FROM Player;")
a = cursor.fetchone()
cursor.execute("""
SELECT SUM(Quantity) FROM PlayerCollection 
WHERE PlayerID = "P001"
""")
b = cursor.fetchone()
cursor.execute("""
SELECT Card.CardName, Card.Rarity FROM Card
JOIN PLayerCollection ON PLayerCollection.CardID = Card.CardID
JOIN PLayer ON PlayerCollection.PlayerID = Player.PlayerID
WHERE Player.PlayerID = 'P001'
    ORDER BY
        CASE Card.Rarity
            WHEN 'Special Illustration Rare' THEN 1
            WHEN 'Illustration Rare'         THEN 2
            WHEN 'Hyper Rare'                THEN 3
            WHEN 'Ultra Rare'                THEN 4
            WHEN 'Ace Spec'                  THEN 5
            WHEN 'Double Rare'               THEN 6
            WHEN 'Rare Holo'                 THEN 7
            WHEN 'Rare'                      THEN 8
            WHEN 'Uncommon'                  THEN 9
            WHEN 'Common'                    THEN 10
            ELSE 11
        END ASC
    LIMIT 1;
""")
c = cursor.fetchone()
cursor.execute("SELECT COUNT(DeckID) FROM Deck WHERE PlayerID = 'P001'")
d = cursor.fetchone()
cursor.execute("SELECT Deck.DeckName FROM Deck WHERE PlayerID = 'P001'")
e = cursor.fetchall()
cursor.execute("""
SELECT TournamentName FROM Tournament
JOIN RegistrationList ON RegistrationList.TournamentID = Tournament.TournamentID
JOIN Player ON Player.PlayerID = RegistrationList.PlayerID
WHERE Player.PlayerID = 'P001'
""")
f = cursor.fetchall()
cursor.execute("SELECT COUNT(MatchesID) FROM Matches WHERE Player1 = 'P001' OR Player2 = 'P001'")
g = cursor.fetchone()
cursor.execute("SELECT COUNT(MatchesID) FROM Matches WHERE Winner = 'P001'")
h = cursor.fetchone()
#print(h)

cursor.executemany("""
SELECT PlayerID, Username FROM Player;
SELECT SUM(Quantity) FROM PlayerCollection 
WHERE PlayerID = "P001";
SELECT Card.CardName, Card.Rarity FROM Card
JOIN PLayerCollection ON PLayerCollection.CardID = Card.CardID
JOIN PLayer ON PlayerCollection.PlayerID = Player.PlayerID
WHERE Player.PlayerID = 'P001'
    ORDER BY
        CASE Card.Rarity
            WHEN 'Special Illustration Rare' THEN 1
            WHEN 'Illustration Rare'         THEN 2
            WHEN 'Hyper Rare'                THEN 3
            WHEN 'Ultra Rare'                THEN 4
            WHEN 'Ace Spec'                  THEN 5
            WHEN 'Double Rare'               THEN 6
            WHEN 'Rare Holo'                 THEN 7
            WHEN 'Rare'                      THEN 8
            WHEN 'Uncommon'                  THEN 9
            WHEN 'Common'                    THEN 10
            ELSE 11
        END ASC
    LIMIT 1;
""")

print(cursor.fetchmany())

