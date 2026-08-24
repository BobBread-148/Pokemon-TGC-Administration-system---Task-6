import sqlite3
import json
import os

conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")


with open("data/card data/sets.json", encoding="utf-8") as file:
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

def insert_creature(card):

    stage = card.get("subtypes", ["Basic"])[0]
    if stage == "Basic":
        stage = "Basic pokemon"

    hp = int(card.get("hp", 0))

    element = card.get("types", ["Colorless"])[0]

    retreat = len(card.get("retreatCost", []))

    weakness = None
    if card.get("weaknesses"):
        weakness = card["weaknesses"][0]["type"]

    resistance = None
    if card.get("resistances"):
        resistance = card["resistances"][0]["type"]

    cursor.execute("""
    INSERT OR IGNORE INTO CreatureCard
    VALUES (?,?,?,?,?,?,?)
    """, (
        card["id"],
        stage,
        hp,
        element,
        retreat,
        weakness,
        resistance
    ))

def insert_trainer(card):

    subtype = card.get("subtypes", ["Item"])[0]

    if subtype == "Pokémon Tool":
        subtype = "Tool"

    rules = "\n".join(card.get("rules", []))

    cursor.execute("""
    INSERT OR IGNORE INTO TrainerCard
    VALUES (?,?,?)
    """,
    (
        card["id"],
        subtype,
        rules
    ))

def insert_energy(card):

    energy_type = card.get("subtypes", ["Basic"])[0]

    element = card.get("types", ["Colorless"])[0]

    special_effects = "\n".join(card.get("rules", []))

    cursor.execute("""
    INSERT OR IGNORE INTO EnergyCard
    VALUES (?,?,?,?)
    """, (
        card["id"],
        element,
        energy_type,
        special_effects
    ))

def insert_ability(card):

    if "abilities" not in card:
        return

    for i, ability in enumerate(card["abilities"], start=1):

        ability_id = f'{card["id"]}-AB{i}'

        cursor.execute("""
        INSERT OR IGNORE INTO CardAbility
        VALUES (?,?,?,?,?)
        """, (
            ability_id,
            card["id"],
            ability["name"],
            ability["type"],
            ability["text"]
        ))

def insert_attack(card):

    if "attacks" not in card:
        return

    for i, attack in enumerate(card["attacks"], start=1):

        attack_id = f'{card["id"]}-AT{i}'

        damage = attack.get("damage")

        damage_value = None
        damage_modifier = None

        if damage and damage not in ["—", "-"]:
            try:
                if damage.endswith("+"):
                    damage_modifier = "+"
                    damage_value = int(damage[:-1])

                elif damage.endswith("×"):
                    damage_modifier = "×"
                    damage_value = int(damage[:-1])

                else:
                    damage_value = int(damage)

            except ValueError:
                damage_value = None


        cursor.execute("""
        INSERT OR IGNORE INTO AttackDetails
        VALUES (?,?,?,?,?,?,?)
        """, (
            attack_id,
            card["id"],
            attack["name"],
            damage_value,
            damage_modifier,
            len(attack.get("cost", [])),
            attack.get("text")
        ))

def import_cards():
    for filename in os.listdir("data/card data"):
        if filename.endswith(".json") and filename != "sets.json":
            print("importing", filename)

            with open("data/card data/" + filename, encoding="utf-8") as file:
                cards = json.load(file)

            for card in cards:
                insert_set(card)
                insert_card(card)

                supertype = card.get("supertype")

                if supertype == "Pokémon":
                    insert_creature(card)
                    insert_ability(card)
                    insert_attack(card)

                elif supertype == "Trainer":
                    insert_trainer(card)

                elif supertype == "Energy":
                    insert_energy(card)

    conn.commit()
    print("Card import complete!")

def insert_player(player):
    cursor.execute("""
    INSERT OR IGNORE INTO Player VALUES (?,?,?,?,?,?)
    """,
    (
        player["PlayerID"],
        player["Username"],
        player["DateJoined"],
        player["DateOfBirth"],
        player["PhoneNumber"],
        player["Email"]
    ))

def import_players():
    with open("data/players.json", encoding="utf-8") as file:
        players = json.load(file)

    for player in players:
        insert_player(player)

    conn.commit()
    print("Player import complete!")

def insert_staff(staff):
    cursor.execute("""
    INSERT OR IGNORE INTO Staff
    VALUES (?,?,?,?,?,?,?,?)
    """,
    (
        staff["StaffID"],
        staff["FirstName"],
        staff["LastName"],
        staff["Username"],
        staff["Password"],
        staff["Email"],
        staff["PhoneNumber"],
        staff["Position"]
    ))


def import_staff():
    with open("data/staff.json", encoding="utf-8") as file:
        staff_members = json.load(file)

    for staff in staff_members:
        insert_staff(staff)

    conn.commit()
    print("Staff import complete!")
import json

def insert_venue(venue):
    cursor.execute(
        """
        INSERT OR IGNORE INTO Venue (VenueID, VenueName, VenueCity, VenueCountry)
        VALUES (?, ?, ?, ?)
        """,
        (
            venue["VenueID"],
            venue["VenueName"],
            venue["VenueCity"],
            venue["VenueCountry"]
        )
    )

def import_venues():
    try:
        with open("data/venue.json", "r", encoding="utf-8") as file:
            venues = json.load(file)

        for venue in venues:
            insert_venue(venue)

        conn.commit()
        print("Venue import complete!")
    except FileNotFoundError:
        print("Error: 'data/venue.json' file not found.")
def insert_tournament(tournament):
    cursor.execute(
        """
        INSERT OR IGNORE INTO Tournament (TournamentID, TournamentName, EventDate, VenueID, EventStatus)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            tournament["TournamentID"],
            tournament["TournamentName"],
            tournament["EventDate"],
            tournament["VenueID"],
            tournament["EventStatus"]
        )
    )

def import_tournaments():
    try:
        with open("data/tournaments.json", "r", encoding="utf-8") as file:
            tournaments = json.load(file)

        for tournament in tournaments:
            insert_tournament(tournament)

        conn.commit()
        print("Tournament import complete!")
    except FileNotFoundError:
        print("Error: 'data/tournaments.json' file not found.")



def insert_registration(registration):
    cursor.execute("""
    INSERT OR IGNORE INTO RegistrationList
    VALUES (?,?)
    """,
    (
        registration["TournamentID"],
        registration["PlayerID"]
    ))
    
def import_registrations():
    with open("data/registration lists.json", encoding="utf-8") as file:
        registrations = json.load(file)

    for registration in registrations:
        insert_registration(registration)

    conn.commit()
    print("Registration import complete!")

def insert_tournament_staff(tournament_staff):
    cursor.execute("""
    INSERT OR IGNORE INTO TournamentStaff
    VALUES (?,?,?)
    """,
    (
        tournament_staff["TournamentID"],
        tournament_staff["StaffID"],
        tournament_staff["Role"]
    ))

def import_tournament_staff():
    with open("data/tournament staff.json", encoding="utf-8") as file:
        tournament_staff_list = json.load(file)

    for tournament_staff in tournament_staff_list:
        insert_tournament_staff(tournament_staff)

    conn.commit()
    print("Tournament Staff import complete!")

def insert_match(match):
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO Matches
        VALUES (?,?,?,?,?,?,?)
        """,
        (
            match["MatchesID"],
            match["TournamentID"],
            match["Player1"],
            match["Player2"],
            match["Winner"],
            match["MatchStatus"],
            match["Round"]
        ))

    except sqlite3.IntegrityError:
        print("FAILED MATCH:")
        print(match)
        raise


def import_matches():
    with open("data/matches.json", encoding="utf-8") as file:
        matches = json.load(file)

    for match in matches:
        insert_match(match)

    conn.commit()
    print("Matches import complete!")

def import_player_collection():

    with open("data/player_collection.json") as f:
        data = json.load(f)

    for row in data:
        cursor.execute("""
            INSERT OR IGNORE INTO PlayerCollection
            (
                PlayerID,
                CardID,
                Quantity
            )
            VALUES (?, ?, ?)
        """, (
            row["PlayerID"],
            row["CardID"],
            row["Quantity"]
        ))

    conn.commit()
    print("Player Collection import complete!")

def import_decks():
    with open("data/decks.json", "r") as f:
        decks = json.load(f)

    for deck in decks:
        cursor.execute("""
            INSERT OR IGNORE INTO Deck(
                DeckID,
                PlayerID,
                DeckName
            )
            VALUES (?, ?, ?)
        """,
        (
            deck["DeckID"],
            deck["PlayerID"],
            deck["DeckName"]
        ))

    conn.commit()
    print(f"Imported {len(decks)} decks")

def import_cardindeck():
    with open("data/cardindeck.json", "r") as f:
        cards = json.load(f)

    for card in cards:
        cursor.execute("""
            INSERT OR IGNORE INTO CardInDeck(
                DeckID,
                CardID,
                Quantity
            )
            VALUES (?, ?, ?)
        """, (
            card["DeckID"],
            card["CardID"],
            card["Quantity"]
        ))

    conn.commit()
    print(f"Imported {len(cards)} CardInDeck rows")

def import_trades():
    with open("data/trades.json", "r") as f:
        trades = json.load(f)

    for trade in trades:
        cursor.execute("""
            INSERT OR IGNORE INTO Trade(
                TradeID,
                SenderID,
                ReceiverID,
                TradeDate,
                TradeStatus
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            trade["TradeID"],
            trade["SenderID"],
            trade["ReceiverID"],
            trade["TradeDate"],
            trade["TradeStatus"]
        ))

    conn.commit()
    print(f"Imported {len(trades)} trades")

def import_tradecards():
    with open("data/tradecard.json", "r") as f:
        tradecards = json.load(f)

    for tradecard in tradecards:
        cursor.execute("""
            INSERT OR IGNORE INTO TradeCard(
                TradeID,
                CardID,
                Owner,
                Quantity
            )
            VALUES (?, ?, ?, ?)
        """, (
            tradecard["TradeID"],
            tradecard["CardID"],
            tradecard["Owner"],
            tradecard["Quantity"]
        ))

    conn.commit()
    print(f"Imported {len(tradecards)} TradeCard rows")

def main():
    import_cards()
    import_players()
    import_staff()
    import_venues()
    import_tournaments()
    import_registrations()
    import_tournament_staff()
    import_matches()
    import_player_collection()
    import_decks()
    import_cardindeck()
    import_trades()
    import_tradecards()
    conn.commit()
    
    tables = [
        "Player",
        "CardSet",
        "Card",
        "AttackDetails",
        "CardAbility",
        "CreatureCard",
        "TrainerCard",
        "EnergyCard",
        "Tournament",
        "Venue",
        "Staff",
        "RegistrationList",
        "TournamentStaff",
        "Matches",
        "PlayerCollection",
        "Deck",
        "CardInDeck",
        "Trade",
        "TradeCard"
    ]
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table}: {count} rows")


    print("\nChecking foreign keys...")

    cursor.execute("PRAGMA foreign_key_check")
    errors = cursor.fetchall()

    if errors:
        print("Foreign key errors found:")
        for error in errors:
            print(error)
    else:
        print("No foreign key errors ✅")
    conn.close()
    
    
main()      
