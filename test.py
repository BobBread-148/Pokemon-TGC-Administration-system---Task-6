import sqlite3

conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()

def create_tables():
    try:
        cursor.execute('DROP TABLE IF EXISTS Player;')
        cursor.execute("""               
        CREATE TABLE Player(
            PlayerID TEXT(4) PRIMARY KEY NOT NULL UNIQUE,
            Username TEXT(20) NOT NULL,
            DateJoined DATE DEFAULT(CURRENT_DATE()),
            DateOfBirth DATE NOT NULL,
            PhoneNumber INTEGER(17),
            Email TEXT(30) NOT NULL CHECK (Email LIKE ('%@%'))
        ); """)
        cursor.execute('DROP TABLE IF EXISTS Tournament;')
        cursor.execute("""
        CREATE TABLE Tournament(
            TournamentID TEXT(4) PRIMARY KEY NOT NULL UNIQUE,
            TournamentName TEXT(20) NOT NULL,
            EventDate DATE NOT NULL,
            Location TEXT(30) NOT NULL
            );""")
        cursor.execute('DROP TABLE IF EXISTS RegistrationList;')
        cursor.execute("""
            CREATE TABLE RegistrationList(
            PlayerID TEXT(4) NOT NULL,
            TournamentID TEXT(4) NOT NULL,
            PRIMARY KEY (PlayerID, TournamentID),
            FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID),
            FOREIGN KEY (TournamentID) REFERENCES Tournament(TournamentID)
        ); """)
        cursor.execute('DROP TABLE IF EXISTS Match;')
        cursor.execute("""
        CREATE TABLE Match(
            MatchID TEXT(4) PRIMARY KEY NOT NULL UNIQUE,
            TournamentID TEXT(4) NOT NULL,
            Player1 TEXT(4) NOT NULL,
            Player2 TEXT(4) NOT NULL,
            Winner TEXT(4), 
            MatchStatus TEXT NOT NULL,
            FOREIGN KEY (Player1) REFERENCES RegistrationList(PlayerID),
            FOREIGN KEY (Player2) REFERENCES RegistrationList(PlayerID),
            FOREIGN KEY (TournamentID) REFERENCES Tournament(TournamentID),
            CONSTRAINT check_valid_winner CHECK (Winner = Player1 OR Winner = Player2 OR Winner = NULL),
            CONSTRAINT match_status CHECK (MatchStatus IN ('To be played', 'In progress', 'Finished'))
        ); """)
        cursor.execute('DROP TABLE IF EXISTS TournamentStaff;')
        cursor.execute("""
        CREATE TABLE TournamentStaff(
            TournamentID TEXT(4) NOT NULL,
            StaffID TEXT(4) NOT NULL,
            Role TEXT(20) NOT NULL,
            PRIMARY KEY (TournamentID, StaffID),
            FOREIGN KEY (StaffID) REFERENCES Staff(StaffID),
            FOREIGN KEY (TournamentID) REFERENCES Tournament(TournamentID)
        );""")
        cursor.execute('DROP TABLE IF EXISTS Staff;')
        cursor.execute("""
        CREATE TABLE Staff(
            StaffID TEXT(4) PRIMARY KEY NOT NULL,
            Username TEXT(20) NOT NULL,
            Password TEXT(30) NOT NULL,
            Email TEXT(30) NOT NULL CHECK (Email LIKE ('%@%')),
            PhoneNumber(17) INTEGER NOT NULL,
            Position TEXT(20) NOT NULL
        );""")    
        cursor.execute('DROP TABLE IF EXISTS Card;')
        cursor.execute("""
        CREATE TABLE Card(
            CardID TEXT(4) PRIMARY KEY NOT NULL,
            CardName TEXT(20) NOT NULL,
            CardType TEXT CHECK (CardType IN ('Creature Card', 'Trainer Card', 'Energy Card'))
        );""")
        cursor.execute('DROP TABLE IF EXISTS PlayerCollection;')
        cursor.execute("""
        CREATE TABLE PlayerCollection(
            PlayerID TEXT(4) NOT NULL,
            CardID TEXT(4) NOT NULL,
            Quantity INTEGER(3) NOT NULL,
            PRIMARY KEY(PlayerID, CardID),
            FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID),
            FOREIGN KEY (CardID) REFERENCES Card(CardID)
        );""")
        cursor.execute('DROP TABLE IF EXISTS Deck;')
        cursor.execute("""
        CREATE TABLE Deck(
            DeckID TEXT(4) PRIMARY KEY NOT NULL,
            PlayerID TEXT(4) NOT NULL,
            DeckName TEXT(20) NOT NULL,
            FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
        );""")
        cursor.execute('DROP TABLE IF EXISTS CardInDeck;')
        cursor.execute("""
        CREATE TABLE CardInDeck(
            DeckID TEXT(4) NOT NULL,
            CardID TEXT(4) NOT NULL,
            Quantity INTEGER(3) NOT NULL,
            PRIMARY KEY(DeckID, CardID), 
            FOREIGN KEY (DeckID) REFERENCES Deck(DeckID),
            FOREIGN KEY (CardID) REFERENCES Card(CardID) 
        );""")
        cursor.execute('DROP TABLE IF EXISTS CreatureCard;')
        cursor.execute("""
        CREATE TABLE CreatureCard(
            CardID TEXT(4) PRIMARY KEY NOT NULL,
            EvolutionStage TEXT NOT NULL CHECK (EvolutionStage IN ('Basic pokemon', 'Stage 1', 'Stage 2')),
            HP INTEGER(3) NOT NULL,
            ElementType TEXT NOT NULL,
            RetreatCost INTEGER(3) NOT NULL,
            AttackDetails TEXT,
            FOREIGN KEY (CardID) REFERENCES Card(CardID) 
        );""")
        cursor.execute('DROP TABLE IF EXISTS EnergyCard;')
        cursor.execute("""
        CREATE TABLE EnergyCard(
            CardID TEXT(4) PRIMARY KEY NOT NULL,
            ElementType TEXT NOT NULL,
            EnergyType TEXT NOT NULL CHECK (EnergyType IN ('Basic', 'Special')),
            EnergyAmount INTEGER(3) NOT NULL,
            SpecialEffects TEXT,
            FOREIGN KEY (CardID) REFERENCES Card(CardID)
        );""")
        cursor.execute('DROP TABLE IF EXISTS TrainerCard;')
        cursor.execute("""
        CREATE TABLE TrainerCard(
            CardID TEXT(4) PRIMARY KEY NOT NULL,
            Subtype TEXT NOT NULL CHECK (Subtype IN ('Trainer', 'Item')),
            Rules TEXT,
            FOREIGN KEY (CardID) REFERENCES Card(CardID)
        );""")
        print("success")
    except sqlite3.OperationalError as e:
        print(e)
        

def populating_tables():
    cursor.execute("INSERT INTO Player ")
        
        
def main():
    create_tables()
    
main()
