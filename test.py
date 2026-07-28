import sqlite3

conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()

try:
    cursor.execute('DROP TABLE IF EXISTS "Player";')
    cursor.execute("""               
    CREATE TABLE Player(
        PlayerID TEXT PRIMARY KEY NOT NULL,
        Username TEXT NOT NULL,
        DateJoined DATE NOT NULL,
        DateOfBirth DATE NOT NULL,
        PhoneNumber INTEGER,
        Email TEXT NOT NULL
    ); """)
    cursor.execute('DROP TABLE IF EXISTS "RegistrationList";')
    cursor.execute("""
        CREATE TABLE RegistrationList(
        PlayerID TEXT NOT NULL,
        TournamentID TEXT NOT NULL,
        PRIMARY KEY (PlayerID, TournamentID),
        FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
        FOREIGN KEY (TouramentID) REFERENCES Tournament(TournamentID)
    ); """)
    
except sqlite3.OperationalError as e:
    print(e)
