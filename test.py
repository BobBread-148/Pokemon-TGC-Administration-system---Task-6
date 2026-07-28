import sqlite3

conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()

try:
    cursor.execute('DROP TABLE IF EXISTS "Player"')
    cursor.execute("""
    CREATE TABLE "Players"(
        PlayerID TEXT NOT NULL,
        Username TEXT NOT NULL,
        DateJoined DATE NOT NULL,
        DateOfBirth DATE NOT NULL,
        
    )               
                   """)