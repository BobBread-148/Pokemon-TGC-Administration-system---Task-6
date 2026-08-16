import sqlite3

conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = OFF;")

def create_tables():
    try:
        cursor.execute("DROP TABLE IF EXISTS TradeCard;")
        cursor.execute("DROP TABLE IF EXISTS CardInDeck;")
        cursor.execute("DROP TABLE IF EXISTS PlayerCollection;")
        cursor.execute("DROP TABLE IF EXISTS RegistrationList;")
        cursor.execute("DROP TABLE IF EXISTS TournamentStaff;")
        cursor.execute("DROP TABLE IF EXISTS Matches;")
        cursor.execute("DROP TABLE IF EXISTS AttackDetails;")
        cursor.execute("DROP TABLE IF EXISTS CardAbility;")
        cursor.execute("DROP TABLE IF EXISTS CreatureCard;")
        cursor.execute("DROP TABLE IF EXISTS TrainerCard;")
        cursor.execute("DROP TABLE IF EXISTS EnergyCard;")
        cursor.execute("DROP TABLE IF EXISTS Trade;")
        cursor.execute("DROP TABLE IF EXISTS Deck;")
        cursor.execute("DROP TABLE IF EXISTS Card;")
        cursor.execute("DROP TABLE IF EXISTS CardSet;")
        cursor.execute("DROP TABLE IF EXISTS Tournament;")
        cursor.execute("DROP TABLE IF EXISTS Staff;")
        cursor.execute("DROP TABLE IF EXISTS Player;")

        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("""               
        CREATE TABLE Player(
            PlayerID TEXT(4) PRIMARY KEY,
            Username TEXT(20) NOT NULL,
            DateJoined DATE DEFAULT (CURRENT_DATE),
            DateOfBirth DATE NOT NULL CHECK (DateOfBirth < CURRENT_DATE),
            PhoneNumber TEXT(17),
            Email TEXT(30) NOT NULL CHECK (Email LIKE '%@%')
        ); """)

        cursor.execute("""
        CREATE TABLE Tournament(
            TournamentID TEXT(4) PRIMARY KEY NOT NULL UNIQUE,
            TournamentName TEXT(20) NOT NULL,
            EventDate DATE NOT NULL,
            Location TEXT(30) NOT NULL,
            EventStatus TEXT DEFAULT 'Upcoming' CHECK (EventStatus IN ('Upcoming', 'Ongoing', 'Finished')) 
        ); """)

        cursor.execute("""
        CREATE TABLE RegistrationList(
            TournamentID TEXT(4) NOT NULL,
            PlayerID TEXT(4) NOT NULL,
            PRIMARY KEY (TournamentID, PlayerID),
            FOREIGN KEY (TournamentID) REFERENCES Tournament(TournamentID),
            FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
        ); """)

        cursor.execute("""
        CREATE TABLE Matches(
            MatchesID TEXT(4) PRIMARY KEY NOT NULL UNIQUE,
            TournamentID TEXT(4) NOT NULL,
            Player1 TEXT(4) NOT NULL,
            Player2 TEXT(4) NOT NULL,
            Winner TEXT(4), 
            MatchStatus TEXT NOT NULL DEFAULT 'To be played',
            Round INTEGER(1) NOT NULL,
            FOREIGN KEY (TournamentID) REFERENCES Tournament(TournamentID),
            FOREIGN KEY (TournamentID, Player1) REFERENCES RegistrationList(TournamentID, PlayerID),
            FOREIGN KEY (TournamentID, Player2) REFERENCES RegistrationList(TournamentID, PlayerID),
            FOREIGN KEY (Winner) REFERENCES Player(PlayerID),
            CONSTRAINT check_valid_winner CHECK (MatchStatus ='Finished' AND Winner IS NOT NULL OR MatchStatus!='Finished'),
            CONSTRAINT match_status CHECK (MatchStatus IN ('To be played', 'In progress', 'Finished'))
        ); """)

        cursor.execute("""
        CREATE TABLE Staff(
            StaffID TEXT(4) PRIMARY KEY NOT NULL,
            FirstName TEXT(20) NOT NULL,
            LastName TEXT(20) NOT NULL,
            Username TEXT(20) NOT NULL,
            Password TEXT(30) NOT NULL,
            Email TEXT(30) NOT NULL CHECK (Email LIKE ('%@%')),
            PhoneNumber TEXT(17) NOT NULL,
            Position TEXT(20) NOT NULL CHECK (Position IN ('Administrator', 'Moderator', 'Staff'))
        );""")  

        cursor.execute("""
        CREATE TABLE TournamentStaff(
            TournamentID TEXT(4) NOT NULL,
            StaffID TEXT(4) NOT NULL,
            Role TEXT(20) NOT NULL CHECK (Role IN ('Judge', 'Organiser', 'Scorekeeper', 'Demonstrator', 'Support Staff')),
            PRIMARY KEY (TournamentID, StaffID),
            FOREIGN KEY (StaffID) REFERENCES Staff(StaffID),
            FOREIGN KEY (TournamentID) REFERENCES Tournament(TournamentID)
        );""")

        cursor.execute("""
        CREATE TABLE CardSet(
            SetID TEXT PRIMARY KEY,
            SetName TEXT(20) NOT NULL,
            Series TEXT(20) NOT NULL,
            ReleaseDate DATE NOT NULL
        );""")        

        cursor.execute("""
        CREATE TABLE Card(
            CardID TEXT PRIMARY KEY,
            SetID TEXT NOT NULL,
            CardName TEXT(20) NOT NULL,
            CardType TEXT NOT NULL CHECK (CardType IN ('Creature Card', 'Trainer Card', 'Energy Card')),
            CardNumber TEXT NOT NULL,
            Rarity TEXT NOT NULL,
            FOREIGN KEY (SetID) REFERENCES CardSet(SetID)
        );""")

        cursor.execute("""
        CREATE TABLE PlayerCollection(
            PlayerID TEXT(4) NOT NULL,
            CardID TEXT NOT NULL,
            Quantity INTEGER(3) NOT NULL,
            PRIMARY KEY(PlayerID, CardID),
            FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID),
            FOREIGN KEY (CardID) REFERENCES Card(CardID)
        );""")

        cursor.execute("""
        CREATE TABLE Deck(
            DeckID TEXT(4) PRIMARY KEY NOT NULL,
            PlayerID TEXT(4) NOT NULL,
            DeckName TEXT(20) NOT NULL,
            FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
        );""")

        cursor.execute("""
        CREATE TABLE CardInDeck(
            DeckID TEXT(4) NOT NULL,
            CardID TEXT NOT NULL,
            Quantity INTEGER(3) NOT NULL CHECK (Quantity > 0),
            PRIMARY KEY(DeckID, CardID), 
            FOREIGN KEY (DeckID) REFERENCES Deck(DeckID),
            FOREIGN KEY (CardID) REFERENCES Card(CardID) 
        );""")

        cursor.execute("""
        CREATE TABLE CreatureCard(
            CardID TEXT PRIMARY KEY NOT NULL,
            EvolutionStage TEXT NOT NULL CHECK (EvolutionStage IN ('Basic pokemon', 'Stage 1', 'Stage 2')),
            HP INTEGER(3) NOT NULL,
            ElementType TEXT NOT NULL,
            RetreatCost INTEGER(3) NOT NULL,
            Weakness TEXT,
            Resistance TEXT,
            FOREIGN KEY (CardID) REFERENCES Card(CardID) 
        );""")

        cursor.execute("""
        CREATE TABLE CardAbility(
            AbilityID TEXT PRIMARY KEY,
            CardID TEXT NOT NULL,
            AbilityName TEXT NOT NULL,
            AbilityType TEXT NOT NULL,
            Description TEXT NOT NULL,
            FOREIGN KEY (CardID) REFERENCES Card(CardID)
        ); """)

        cursor.execute("""
        CREATE TABLE AttackDetails(
            AttackID TEXT PRIMARY KEY NOT NULL,
            CardID TEXT NOT NULL,
            AttackName TEXT(20) NOT NULL,
            DamageValue INTEGER,
            DamageModifier TEXT CHECK(DamageModifier IN ('+', '×') OR DamageModifier IS NULL),
            EnergyCost INTEGER(3) NOT NULL,
            Effect TEXT,
            FOREIGN KEY (CardID) REFERENCES Card(CardID)
        );""")

        cursor.execute("""
        CREATE TABLE EnergyCard(
            CardID TEXT(4) PRIMARY KEY NOT NULL,
            ElementType TEXT NOT NULL,
            EnergyType TEXT NOT NULL CHECK (EnergyType IN ('Basic', 'Special')),
            SpecialEffects TEXT,
            FOREIGN KEY (CardID) REFERENCES Card(CardID)
        );""")

        cursor.execute("""
        CREATE TABLE TrainerCard(
            CardID TEXT(4) PRIMARY KEY NOT NULL,
            Subtype TEXT NOT NULL CHECK (Subtype IN ('Tool', 'Item', 'Supporter', 'Stadium', 'ACE SPEC')),
            Rules TEXT,
            FOREIGN KEY (CardID) REFERENCES Card(CardID)
        );""")

        cursor.execute("""
        CREATE TABLE Trade(
            TradeID TEXT(4) PRIMARY KEY NOT NULL,
            SenderID TEXT(4) NOT NULL,
            ReceiverID TEXT(4) NOT NULL Check (ReceiverID <> SenderID),
            TradeDate DATE NOT NULL,
            TradeStatus TEXT(10) NOT NULL CHECK (TradeStatus IN ('Pending', 'Completed')),
            FOREIGN KEY (SenderID) REFERENCES Player(PlayerID),
            FOREIGN KEY (ReceiverID) References Player(PlayerID)
        );""")

        cursor.execute("""
        CREATE TABLE TradeCard(
            TradeID TEXT(4),
            CardID TEXT(4),
            Owner TEXT(4),
            Quantity INTEGER(3) NOT NULL CHECK (Quantity > 0),
            PRIMARY KEY(TradeID, CardID),
            FOREIGN KEY (TradeID) REFERENCES Trade(TradeID),
            FOREIGN KEY (CardID) References Card(CardID)
        );""")
        print("success")

    except sqlite3.OperationalError as e:
        print(e)
        

def populating_tables():
    cursor.execute("INSERT INTO Player VALUES ('P001', 'galaxy_fq_', '27-07-2021', '19-09-2008', NULL, 'fajar.208@gmail.com')")
        
        
def main():
    create_tables()
    conn.commit()
    conn.close()
    
main()

