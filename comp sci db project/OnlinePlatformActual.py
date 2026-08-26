from ast import Try
from builtins import input
import sqlite3
import sys
import os
import datetime
from datetime import datetime, date

sqlite3.register_adapter(date, lambda val: val.isoformat())
sqlite3.register_adapter(datetime, lambda val: val.isoformat())


conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def pause_screen():
    input("\nPress Enter to continue...")


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



def login():
    global user_position, user_firstname
    clear_screen()
    print("----------------------Pokemon TGC Administrator System---------------------- ")
    for i in range(3):
        staff_user = input("Enter Username:")
        staff_password = input("Enter Password:")

        cursor.execute("SELECT FirstName, Position FROM Staff WHERE Username = ? AND Password = ?", (staff_user, staff_password))
        user = cursor.fetchone()
        if user:
            user_position = user[1]
            user_firstname = user[0]
            print("\nLogin successful!")
            print(f"Welcome {user_firstname}.  Role: {user_position}")
            pause_screen()
            return True
        else:
            print("\nInvalid username or password. Please try again.\n")
    print("Too many failed attempts. Access denied.")
    pause_screen()
    return False



def main_menu():
    clear_screen()
    print("Login successful!")
    print(f"Welcome {user_firstname}.  Role: {user_position}\n\n")
    
    if user_position == "Administrator":
        print("=" * 60)
        print("                 POKEMON TCG MAIN MENU")
        print("=" * 60)
        print("  [1] Manage Players       [5] Manage Decks")
        print("  [2] Manage Tournaments   [6] Manage Staff")
        print("  [3] Manage Matches       [7] Analytical Reports")
        print("  [4] Manage Cards         [0] Log Out")
        print("=" * 60)
        return input("\nSelect an option: ").strip()

    elif user_position == "Moderator":
        print("=" * 60)
        print("                 POKEMON TCG MAIN MENU")
        print("=" * 60)
        print("  [1] Manage Players       [4] Manage Cards")
        print("  [2] Manage Tournaments   [5] Manage Decks")
        print("  [3] Manage Matches       [0] Log Out")
        print("=" * 60)
        return input("\nSelect an option: ").strip()

    elif user_position == "Staff":
        print("=" * 60)
        print("                 POKEMON TCG MAIN MENU")
        print("=" * 60)
        print("  [1] Manage Players       [3] Manage Matches")
        print("  [2] Manage Tournaments   [0] Log Out")
        print("=" * 60)
        return input("\nSelect an option: ").strip()



def log_out():
    conn.commit()
    conn.close()
    sys.exit("Logging out... Goodbye!")



def manage_players():
    if user_position in ["Administrator", "Moderator"]:
        clear_screen()
        print("-" * 60)
        print("                     Manage Players")
        print("-" * 60)
        print("  [1] View Account Details     [4] Add New Player")
        print("  [2] Edit Account Details     [5] Delete Player")
        print("  [3] View Player Stats        [0] Back to Main Menu")
        print("")
        return input("\nSelect an option: ").strip()
    elif user_position == "Staff":
        clear_screen()
        print("-" * 60)
        print("                     Manage Players")
        print("-" * 60)
        print("  [1] View Account Details     [4] Add New Player")
        print("  [2] Edit Account Details     [0] Back to Main Menu")
        print("  [3] View Player Stats")
        print("")
        return input("\nSelect an option: ").strip()



def view_account_details():
    clear_screen()
    while True:
        print("-" * 60)
        print("                  View Account Details")
        print("-" * 60)
        search = input("Search by ID, Username, or Email (or type 'back'): ").lower().strip()

        if search == "back":
            break

        elif search == "id":
            while True:
                id_input = input("Enter Player ID (or type 'back'): ").strip().upper()
                if id_input.lower() == "back":
                    break
                
                cursor.execute("SELECT * FROM Player WHERE PlayerID = ?", (id_input,))
                player = cursor.fetchone()
                if player:
                    print_as_table(cursor, player)
                    pause_screen()
                    break
                else:
                    print("No player found with that ID. Please try again.")
                    pause_screen()

        elif search == "username":
            while True:
                username = input("Enter Player Username (or type 'back'): ").strip()
                if username.lower() == "back":
                    break
                
                cursor.execute("SELECT * FROM Player WHERE Username = ?", (username,))
                player = cursor.fetchone()
                if player:
                    print_as_table(cursor, player)
                    pause_screen()
                    break
                else:
                    print("No player found with that username. Please try again.")
                    pause_screen()

        elif search == "email":
            while True:
                email = input("Enter Player Email (or type 'back'): ").strip()
                if email.lower() == "back":
                    break
                
                cursor.execute("SELECT * FROM Player WHERE Email = ?", (email,))
                player = cursor.fetchone()
                if player:
                    print_as_table(cursor, player)
                    pause_screen()
                    break
                else:
                    print("No player found with that email. Please try again.")
                    pause_screen()

        else:
            print("Invalid search option. Please enter 'ID', 'Username', or 'Email'.")
            pause_screen()
        clear_screen()



def edit_account_details():
    clear_screen()
    while True:
        print("-" * 60)
        print("                  Edit Account Details")
        print("-" * 60)
        search = input("(type 'back' to go back)\nFind player to edit by ID or Username: ").lower().strip()

        if search == "back":
            break

        elif search == "id":
            while True:
                id_input = input("Enter Player ID (or type 'back'): ").strip().upper()
                if id_input.lower() == "back":
                    break

                cursor.execute("SELECT * FROM Player WHERE PlayerID = ?", (id_input,))
                player = cursor.fetchone()

                if player:
                    edit_account_details_checks(player, cursor)
                    break

                else:
                    print("No player found with that ID. Please try again.")
                    pause_screen()

        elif search == "username":
            while True:
                username = input("Enter Player username (or type 'back'): ").strip()
                if username.lower() == "back":
                    break
                
                cursor.execute("SELECT * FROM Player WHERE Username = ?", (username,))
                player = cursor.fetchone()
                if player:
                    edit_account_details_checks(player, cursor)
                    break

                else:
                    print("No player found with that username. Please try again.")
                    pause_screen()
        else:
            print("Invalid search option. Please enter 'ID' or 'Username'.")
            pause_screen()
        clear_screen()



def edit_account_details_checks(player, cursor):
    
    print_as_table(cursor, player)

    playerid = player[0]
    print("Please enter the player data you wish to change. If you do not wish to change anything in the specific column, just click enter.")

    while True:
        new_username = input("Enter Username: ")
        if new_username == "":
            new_username = player[1]
            break
        cursor.execute("SELECT Username FROM Player WHERE Username = ? AND PlayerID != ?", (new_username, playerid))
        not_unique = cursor.fetchone()
        if not_unique:
            print("This username already exists")
        else:
            break

    while True:
        new_dob = input("Update Date of Birth (YYYY-MM-DD): ").strip()
        if new_dob == "":
            new_dob = player[3]
            break

        try:
            new_dob = datetime.strptime(new_dob, "%Y-%m-%d").date()
            if new_dob > date.today():
                print("Date of birth cannot be in the future.")
            else:
                break
        except ValueError:
            print("Invalid date. Please enter the date in YYYY-MM-DD format.")
            
    while True:
        new_number = input("Update Phone Number: ").strip()
        if new_number == "":
            new_number = player[4]
            break
        cleaned_number = new_number.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        if 3 <= len(new_number) <= 17 and cleaned_number.isdigit():
            break
        else:
            print("\nPlease enter a valid phone number")

    while True:
        new_email = input("Update Email: ").strip()
        if new_email == "":
            new_email = player[5]
            break
        if "@" in new_email and "." in new_email:
            at_position = new_email.index("@")
            dot_position = new_email.rindex(".")
            if at_position > 0 and dot_position > at_position + 1 and dot_position < len(new_email) - 1:
                break
            else:
                print("\nPlease enter a valid email address")
        else:
            print("\nPlease enter a valid email address")
    
    db_number = new_number

    cursor.execute(
        """
        UPDATE Player 
        SET Username = ?, DateOfBirth = ?, PhoneNumber = ?, Email = ? 
        WHERE PlayerID = ?
        """, 
        (
            new_username, 
            new_dob, 
            db_number, 
            new_email,  
            playerid
        )
    )
    conn.commit()
    print("Player details updated successfully.")
    pause_screen()



def view_player_stats():
    clear_screen()
    while True:
        print("-" * 60)
        print("                  View Player Stats")
        print("-" * 60)
        search = input("(type 'back' to go back)\nSearch for Player by ID or Username: ").lower().strip()
        
        if search == "back":
            break

        elif search == "id":
            while True:
                id_input = input("Enter Player ID (or type 'back'): ").strip().upper()
                if id_input.lower() == "back":
                    break
                
                cursor.execute("SELECT * FROM Player WHERE PlayerID = ?", (id_input,))
                player = cursor.fetchone()
                if player:
                    player_stats(player)
                    break
                else:
                    print("No player found with that ID. Please try again.")
                    pause_screen()

        elif search == "username":
            while True:
                username = input("Enter Player Username (or type 'back'): ").strip()
                if username.lower() == "back":
                    break
                
                cursor.execute("SELECT * FROM Player WHERE Username = ?", (username,))
                player = cursor.fetchone()
                if player:
                    player_stats(player)
                    break
                else:
                    print("No player found with that username. Please try again.")
                    pause_screen()

        else:
            print("Invalid search option. Please enter 'ID' or 'Username'.")
            pause_screen()
        clear_screen()



def player_stats(player):
    cursor.execute("SELECT PlayerID, Username FROM Player WHERE PlayerID = ?", (player[0],))
    a = cursor.fetchone()
    player_id = a[0]
    player_username = a[1]

    cursor.execute("SELECT SUM(Quantity) FROM PlayerCollection WHERE PlayerID = ?", (player[0],))
    b = cursor.fetchone()
    player_totalcards = b[0] if (b and b[0] is not None) else 0

    cursor.execute("""
    SELECT Card.CardName FROM Card
    JOIN PlayerCollection ON PlayerCollection.CardID = Card.CardID
    JOIN Player ON PlayerCollection.PlayerID = Player.PlayerID
    WHERE Player.PlayerID = ?
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
    """, (player[0],))
    c = cursor.fetchone()
    player_rarestcard = c[0] if c else "None"

    cursor.execute("SELECT COUNT(DeckID) FROM Deck WHERE PlayerID = ?", (player[0],))
    d = cursor.fetchone()
    player_totaldecks = d[0] if (d and d[0] is not None) else 0

    cursor.execute("SELECT Deck.DeckName FROM Deck WHERE PlayerID = ?", (player[0],))
    e = cursor.fetchall()
    player_decknames = ", ".join([row[0] for row in e]) if e else "None"

    cursor.execute("""
    SELECT TournamentName FROM Tournament
    JOIN RegistrationList ON RegistrationList.TournamentID = Tournament.TournamentID
    JOIN Player ON Player.PlayerID = RegistrationList.PlayerID
    WHERE Player.PlayerID = ?
    """, (player[0],))
    f = cursor.fetchall()
    player_tournaments = ", ".join([row[0] for row in f]) if f else "None"

    cursor.execute("SELECT COUNT(MatchesID) FROM Matches WHERE Player1 = ? OR Player2 = ?", [player[0], player[0]])
    g = cursor.fetchone()
    player_totalmatches = g[0] if (g and g[0] is not None) else 0

    cursor.execute("SELECT COUNT(MatchesID) FROM Matches WHERE Winner = ?", (player[0],))
    h = cursor.fetchone()
    player_totalwins = h[0] if (h and h[0] is not None) else 0

    stat_template = "  {:<25} : {}"

    print("\nPlayer Statistics Summary")
    print("-" * 55)
    print(stat_template.format("Player ID", player_id))
    print(stat_template.format("Username", player_username))
    print(stat_template.format("Total Cards Owned", player_totalcards))
    print(stat_template.format("Rarest Card", player_rarestcard))
    print(stat_template.format("Total Decks Owned", player_totaldecks))
    print(stat_template.format("Decks", player_decknames))
    print(stat_template.format("Tournaments Entered", player_tournaments))
    print(stat_template.format("Total Matches Played", player_totalmatches))
    print(stat_template.format("Total Wins", player_totalwins))
    print("-" * 55)
    pause_screen()



def add_new_player():
    clear_screen()
    print("-" * 60)
    print("                  Add New Player")
    print("-" * 60)
    
    cursor.execute("SELECT MAX(PlayerID) FROM Player;")
    result = cursor.fetchone()

    if result[0] is None:
        next_number = 1
    else:
        next_number = int(result[0][1:]) + 1

    player_id = f"P{next_number:03d}"
    date_joined = date.today()

    print(f"New Player ID: {player_id}")
    print(f"Registration Date  : {date_joined}\n")

    while True:
        username = input("Enter Username: ")

        if username == "":
            print("Enter a valid username:")
            continue

        cursor.execute("SELECT Username FROM Player WHERE Username = ?", (username,))
        not_unique = cursor.fetchone()

        if not_unique:
            print("This username already exists")
        else:
            break

    while True:
        dob = input("Update Date of Birth (YYYY-MM-DD): ").strip()

        if dob == "":
            print("Enter a valid date of birth:")
            continue

        try:
            dob = datetime.strptime(dob, "%Y-%m-%d").date()

            if dob > date.today():
                print("Date of birth cannot be in the future.")
            else:
                break

        except ValueError:
            print("Invalid date. Please enter the date in YYYY-MM-DD format.")
            
    while True:
        number = input("Update Phone Number: ").strip()

        if number == "":
            number = None
            break

        cleaned_number = number.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")

        if 3 <= len(cleaned_number) <= 17 and cleaned_number.isdigit():
            break
        else:
            print("\nPlease enter a valid phone number:")

    while True:
        email = input("Update Email: ").strip()

        if email == "":
            print("\nPlease enter a valid email:")
            continue

        if "@" in email and "." in email:
            at_position = email.index("@")
            dot_position = email.rindex(".")

            if at_position > 0 and dot_position > at_position + 1 and dot_position < len(email) - 1:
                break
            else:
                print("\nPlease enter a valid email")
        else:
            print("E\nPlease enter a valid email")

    db_number = number

    cursor.execute(
        """
        INSERT INTO Player (PlayerID, Username, DateOfBirth, PhoneNumber, Email, DateJoined) 
        VALUES (?, ?, ?, ?, ?, ?)
        """, 
        (player_id, username, dob, db_number, email, date_joined)
    )
    conn.commit()
    print(f"\nNew player '{username}' added successfully.")
    pause_screen()



def delete_player():
    
    while True:
        clear_screen()
        print("-" * 60)
        print("                  Delete Player")
        print("-" * 60)
        search = input("(type 'back' to go back)\nFind player to delete by ID or Username: ").lower().strip()

        if search == "back":
            break

        elif search == "id":
            while True:
                id_input = input("Enter Player ID (or type 'back'): ").strip().upper()
                if id_input.lower() == "back":
                    break
                
                cursor.execute("SELECT * FROM Player WHERE PlayerID = ?", (id_input,))
                player = cursor.fetchone()

                if player:
                    print_as_table(cursor, player)
                    confirm = input(f"Are you sure you want to delete player '{player[1]}'? (yes/no): ").lower().strip()

                    if confirm == "yes":

                        # Delete matches involving this player
                        cursor.execute("""
                        DELETE FROM Matches
                        WHERE Player1 = ? OR Player2 = ? OR Winner = ?
                        """, (player[0], player[0], player[0]))

                        # Delete tournament registrations
                        cursor.execute("""
                        DELETE FROM RegistrationList
                        WHERE PlayerID = ?
                        """, (player[0],))

                        # Delete player's card collection
                        cursor.execute("""
                        DELETE FROM PlayerCollection
                        WHERE PlayerID = ?
                        """, (player[0],))

                        # Delete cards from the player's decks
                        cursor.execute("""
                        DELETE FROM CardInDeck
                        WHERE DeckID IN (
                            SELECT DeckID
                            FROM Deck
                            WHERE PlayerID = ?
                        )
                        """, (player[0],))

                        # Delete player's decks
                        cursor.execute("""
                        DELETE FROM Deck
                        WHERE PlayerID = ?
                        """, (player[0],))

                        # Delete trade cards belonging to the player's trades
                        cursor.execute("""
                        DELETE FROM TradeCard
                        WHERE TradeID IN (
                            SELECT TradeID
                            FROM Trade
                            WHERE SenderID = ? OR ReceiverID = ?
                        )
                        """, (player[0], player[0]))

                        # Delete player's trades
                        cursor.execute("""
                        DELETE FROM Trade
                        WHERE SenderID = ? OR ReceiverID = ?
                        """, (player[0], player[0]))

                        # Finally delete the player
                        cursor.execute("""
                        DELETE FROM Player
                        WHERE PlayerID = ?
                        """, (player[0],))

                        conn.commit()

                        print(f"Player '{player[1]}' deleted successfully.")
                        pause_screen()
                        break

                    elif confirm == "no":
                        print("Deletion cancelled.")
                        pause_screen()
                        break

                    else:
                        print("\nPlease select from 'yes' or 'no'")

                else:
                    print("No player found with that ID. Please try again.")
                    pause_screen()

        elif search == "username":
            while True:
                username = input("Enter Player Username (or type 'back'): ").strip()

                if username.lower() == "back":
                    break
                
                cursor.execute("SELECT * FROM Player WHERE Username = ?", (username,))
                player = cursor.fetchone()

                if player:
                    print_as_table(cursor, player)
                    confirm = input(f"Are you sure you want to delete player '{player[1]}'? (yes/no): ").lower().strip()

                    if confirm == "yes":

                        # Delete matches involving this player
                        cursor.execute("""
                        DELETE FROM Matches
                        WHERE Player1 = ? OR Player2 = ? OR Winner = ?
                        """, (player[0], player[0], player[0]))

                        # Delete tournament registrations
                        cursor.execute("""
                        DELETE FROM RegistrationList
                        WHERE PlayerID = ?
                        """, (player[0],))

                        # Delete player's card collection
                        cursor.execute("""
                        DELETE FROM PlayerCollection
                        WHERE PlayerID = ?
                        """, (player[0],))

                        # Delete cards from the player's decks
                        cursor.execute("""
                        DELETE FROM CardInDeck
                        WHERE DeckID IN (
                            SELECT DeckID
                            FROM Deck
                            WHERE PlayerID = ?
                        )
                        """, (player[0],))

                        # Delete player's decks
                        cursor.execute("""
                        DELETE FROM Deck
                        WHERE PlayerID = ?
                        """, (player[0],))

                        # Delete trade cards belonging to the player's trades
                        cursor.execute("""
                        DELETE FROM TradeCard
                        WHERE TradeID IN (
                            SELECT TradeID
                            FROM Trade
                            WHERE SenderID = ? OR ReceiverID = ?
                        )
                        """, (player[0], player[0]))

                        # Delete player's trades
                        cursor.execute("""
                        DELETE FROM Trade
                        WHERE SenderID = ? OR ReceiverID = ?
                        """, (player[0], player[0]))

                        # Finally delete the player
                        cursor.execute("""
                        DELETE FROM Player
                        WHERE PlayerID = ?
                        """, (player[0],))

                        conn.commit()

                        print(f"Player '{player[1]}' deleted successfully.")
                        pause_screen()
                        break

                    elif confirm == "no":
                        print("Deletion cancelled.")
                        pause_screen()
                        break

                    else:
                        print("\nPlease select from 'yes' or 'no'")

                else:
                    print("No player found with that username. Please try again.")
                    pause_screen()

        else:
            print("Invalid search option. Please enter 'ID' or 'Username'.")
            pause_screen()

        clear_screen()



def manage_tournaments():
    if user_position in ["Administrator", "Moderator"]:
        clear_screen()
        print("-" * 75)
        print("                           Manage Tournaments")
        print("-" * 75)
        print("  [1] View Tournament Details                 [4] Create New Tournament")
        print("  [2] Edit Tournament Details                 [5] Delete Tournament")
        print("  [3] Register/Remove player from Tournament  [0] Back to Main Menu")
        print("")
        return input("\nSelect an option: ").strip()
    elif user_position == "Staff":
        clear_screen()
        print("-" * 50)
        print("              Manage Tournaments")
        print("-" * 50)
        print("  [1] View Tournament Details")
        print("  [2] Register/Remove player from Tournament")
        print("  [0] Back to Main Menu")
        print("")
        return input("\nSelect an option: ").strip()



def view_tournament_details():
    clear_screen()
    while True:
        print("-" * 60)
        print("                     View Tournament Details")
        print("-" * 60)
        category = input("""
[1] View All Tournaments        [3] View specific Tournament Details
[2] View Upcoming Tournament    [0] Back
        """)
        if category == '0':
            break
        elif category == '1':
            table = cursor.execute("""
            SELECT *, COUNT(REGISTRATIONLIST.PlayerID) AS PLayersRegistered 
            FROM TOURNAMENT
            LEFT JOIN REGISTRATIONLIST ON REGISTRATIONLIST.TOURNAMENTID = TOURNAMENT.TOURNAMENTID
            GROUP BY TOURNAMENT.TOURNAMENTID 
            ORDER BY EventDate DESC;
            """) 
            if table:
                print_as_table(cursor, table.fetchall())
                pause_screen()
            else:
                print("No tournaments found.")
                pause_screen()
        elif category == '2':
            table =cursor.execute("""
            SELECT *, COUNT(REGISTRATIONLIST.PlayerID) AS PLayersRegistered 
            FROM TOURNAMENT
            LEFT JOIN REGISTRATIONLIST ON REGISTRATIONLIST.TOURNAMENTID = TOURNAMENT.TOURNAMENTID
            WHERE eventstatus = 'Upcoming'
            GROUP BY TOURNAMENT.TOURNAMENTID 
            ORDER BY EventDate DESC;
            """)
            if table:
                print_as_table(cursor, table.fetchall())
                pause_screen()
            else:
                print("No upcoming tournaments found.")
                pause_screen()
        elif category == '3':
            while True:
                search = input("Search by TournamentID or Tournament Name (ype 'id', 'name' or 'back'): ").lower().strip()
                if search == "back":
                    break
                elif search == "id":
                    while True:
                        id_input = input("Enter Tournament ID (or type 'back'): ").strip().upper()
                        if id_input.lower() == "back":
                            break
                        cursor.execute("SELECT * FROM Tournament WHERE TournamentID = ?", (id_input,))
                        tournament = cursor.fetchone()
                        if tournament:
                            print_as_table(cursor, tournament)
                            pause_screen()
                            break
                        else:
                            print("No tournament found with that ID. Please try again.")
                            pause_screen()
                elif search == "name":
                    while True:
                        name_input = input("Enter Tournament Name (or type 'back'): ").strip()
                        if name_input.lower() == "back":
                            break
                        cursor.execute("SELECT * FROM Tournament WHERE TournamentName = ?", (name_input,))
                        tournament = cursor.fetchone()
                        if tournament:
                            print_as_table(cursor, tournament)
                            pause_screen()
                            break
                        else:
                            print("No tournament found with that name. Please try again.")
                            pause_screen()
                else:
                    print("Invalid search option. Please enter 'id', 'name', or 'back'.")
                    pause_screen()
        else:
            print("Invalid option. Please select a valid category.")
            pause_screen()
        clear_screen()



def edit_tournament_details():
    clear_screen()

    while True:
        print("-" * 60)
        print("                  Edit Tournament Details")
        print("-" * 60)
        search = input("(type 'back' to go back)\nFind tournament to edit by ID or Name: ").lower().strip()

        if search == "back":
            break

        elif search == "id":
            while True:
                id_input = input("Enter Tournament ID (or type 'back'): ").strip().upper()
                if id_input.lower() == "back":
                    break
                cursor.execute("SELECT * FROM Tournament WHERE TournamentID = ?",(id_input,))
                tournament = cursor.fetchone()

                if tournament:
                    edit_tournament_details_checks(tournament, cursor)
                    break
                else:
                    print("No Tournament found with that ID. Please try again.")
                    pause_screen()

        elif search == "name":
            while True:
                name_input = input("Enter Tournament Name (or type 'back'): ").strip()
                if name_input.lower() == "back":
                    break
                cursor.execute("SELECT * FROM Tournament WHERE TournamentName = ?",(name_input,))
                tournament = cursor.fetchone()

                if tournament:
                    edit_tournament_details_checks(tournament, cursor)
                    break
                else:
                    print("No Tournament found with that name. Please try again.")
                    pause_screen()
        else:
            print("Invalid search option. Please enter 'ID' or 'Name'.")
            pause_screen()
        clear_screen()



def edit_tournament_details_checks(tournament, cursor):
    print_as_table(cursor, tournament)
    tournamentid = tournament[0]
    print("Please enter the tournament data you wish to change. If you do not wish to change anything in the specific column, just click enter.")

    while True:
        new_tournamentname = input("Update tournament name: ").strip()
        if new_tournamentname == "":
            new_tournamentname = tournament[1]
            break
        cursor.execute("SELECT TournamentID FROM Tournament WHERE TournamentName = ? AND TournamentID != ?",(new_tournamentname, tournamentid))
        if cursor.fetchone():
            print("A tournament with that name already exists.")
        else:
            break

    while True:
        new_date = input("Update start date (YYYY-MM-DD): ").strip()
        if new_date == "":
            new_date = tournament[2]
            break
        try:
            new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date. Please enter the date in YYYY-MM-DD format.")

    while True:
        new_location = input("Update tournament location (city, country): ").strip()
        if new_location == "":
            new_location = tournament[3]
            break

        if "," not in new_location:
            print("Invalid location. Please enter it in the format city, country.")
            continue

        city, country = new_location.split(",", 1)
        if city.strip() == "" or country.strip() == "":
            print("Invalid location. Please enter it in the format city, country.")
            continue
        new_location = f"{city.strip()}, {country.strip()}"
        break

    while True:
        new_status = input("Update status (Upcoming, Ongoing, Finished): ").strip()
        if new_status == "":
            new_status = tournament[4]
            break

        if new_status in ['Upcoming', 'Ongoing', 'Finished']:
            break
        print("Invalid status. Please enter Upcoming, Ongoing, or Finished.")

    cursor.execute(
        """
        UPDATE Tournament
        SET TournamentName = ?, EventDate = ?, Location = ?, EventStatus = ?
        WHERE TournamentID = ?
        """,
        (
            new_tournamentname,
            new_date,
            new_location,
            new_status,
            tournamentid
        ))

    conn.commit()

    print("Tournament details updated successfully.")
    pause_screen()



def register_remove_players():
    while True:
        clear_screen()
        print("-" * 60)
        print("                  Tournament Registration")
        print("-" * 60)
        choice = input("(type 'back' to go back)\nWould you like to register a player [1] or remove a player [2] from a tournament? ").lower().strip()

        if choice == "back":
            break

        elif choice == "1":
            clear_screen()
            print("-" * 60)
            print("                  Register New Player")
            print("-" * 60)

            tournament_id = input("Enter Tournament ID: ").strip().upper()

            if tournament_id == "":
                print("\nEnter a valid Tournament ID.")
                pause_screen()
                continue

            cursor.execute(
                "SELECT 1 FROM Tournament WHERE TournamentID = ?",
                (tournament_id,)
            )

            if not cursor.fetchone():
                print("\nError: Tournament ID does not exist.")
                pause_screen()
                continue

            player_id = input("Enter Player ID: ").strip().upper()

            if player_id == "":
                print("\nEnter a valid Player ID.")
                pause_screen()
                continue

            cursor.execute(
                "SELECT 1 FROM Player WHERE PlayerID = ?",
                (player_id,)
            )

            if not cursor.fetchone():
                print("\nError: Player ID does not exist.")
                pause_screen()
                continue

            cursor.execute(
                """
                SELECT 1
                FROM RegistrationList
                WHERE TournamentID = ? AND PlayerID = ?
                """,
                (tournament_id, player_id)
            )

            if cursor.fetchone():
                print("\nError: This player is already registered for this tournament.")
                pause_screen()
                continue

            cursor.execute(
                """
                INSERT INTO RegistrationList (TournamentID, PlayerID)
                VALUES (?, ?)
                """,
                (tournament_id, player_id)
            )

            conn.commit()

            print("\nPlayer successfully added.")
            pause_screen()

        elif choice == "2":
            clear_screen()
            print("-" * 60)
            print("                  Remove Player from Tournament")
            print("-" * 60)

            tournament_id = input("Enter Tournament ID: ").strip().upper()

            if tournament_id == "":
                print("\nEnter a valid Tournament ID.")
                pause_screen()
                continue

            player_id = input("Enter Player ID: ").strip().upper()

            if player_id == "":
                print("\nEnter a valid Player ID.")
                pause_screen()
                continue

            cursor.execute(
                """
                SELECT 1
                FROM RegistrationList
                WHERE TournamentID = ? AND PlayerID = ?
                """,
                (tournament_id, player_id)
            )

            if not cursor.fetchone():
                print("\nError: No such registration found.")
                pause_screen()
                continue

            # Check whether the player is already involved in a match
            cursor.execute(
                """
                SELECT 1
                FROM Matches
                WHERE TournamentID = ?
                AND (Player1 = ? OR Player2 = ?)
                """,
                (tournament_id, player_id, player_id)
            )

            if cursor.fetchone():
                print("\nError: This player is involved in a match and cannot be removed.")
                pause_screen()
                continue

            cursor.execute(
                """
                DELETE FROM RegistrationList
                WHERE TournamentID = ? AND PlayerID = ?
                """,
                (tournament_id, player_id)
            )

            conn.commit()

            print("\nPlayer successfully removed from tournament.")
            pause_screen()

        else:
            print("\nInvalid choice. Please enter 1, 2, or 'back'.")
            pause_screen()



def create_new_tournament():
    while True:
        clear_screen()
        print("-" * 60)
        print("                  Create New Tournament")
        print("-" * 60)
        
        cursor.execute("SELECT MAX(TournamentID) FROM Tournament;")
        result = cursor.fetchone()
    
        if result is None or result[0] is None:
            next_number = 1
        else:
            current_id = result[0]
            next_number = int(current_id[1:]) + 1
    
        tournament_id = f"T{next_number:03d}"
    
        print(f"Generated Tournament ID: {tournament_id}")
    
        # Tournament name
        while True:
            name = input("Enter Tournament Name (or 'back' to go back): ").strip()

            if name.lower() == "back":
                return

            if name == "":
                print("Tournament name cannot be empty.")
            elif len(name) > 20:
                print("Tournament name must be 20 characters or fewer.")
            else:
                break

        # Event date
        while True:
            eventdate = input("Enter Event Date (YYYY-MM-DD): ").strip()

            try:
                eventdate = datetime.strptime(eventdate, "%Y-%m-%d").date()

                if eventdate < date.today():
                    print("Event date cannot be in the past.")
                else:
                    break

            except ValueError:
                print("Invalid date. Please enter the date in YYYY-MM-DD format.")

        # Location
        while True:
            location = input("Enter Event Location (city, country): ").strip()

            if "," not in location:
                print("Please enter the location in the format: city, country")
                continue

            city, country = location.split(",", 1)

            if city.strip() == "" or country.strip() == "":
                print("Please enter both a city and country.")
            elif len(location) > 30:
                print("Location must be 30 characters or fewer.")
            else:
                break

        # Determine event status
        if eventdate == date.today():
            eventstatus = "Ongoing"
        else:
            eventstatus = "Upcoming"

        cursor.execute(
            """
            INSERT INTO Tournament 
            (TournamentID, TournamentName, EventDate, Location, EventStatus) 
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                tournament_id,
                name,
                eventdate,
                location,
                eventstatus
            )
        )

        conn.commit()

        print(f"\nNew Tournament '{name}' added successfully.")
        pause_screen()
        break



def cancel_tournament():
    while True:
        clear_screen()
        print("-" * 60)
        print("                  Cancel Tournament")
        print("-" * 60)
        search = input("(type 'back' to go back)\nFind Tournament to cancel by ID or Name: ").lower().strip()

        if search == "back":
            break

        elif search == "id":
            while True:
                id_input = input("Enter Tournament ID (or type 'back'): ").strip().upper()

                if id_input.lower() == "back":
                    break

                cursor.execute(
                    "SELECT * FROM Tournament WHERE TournamentID = ?",
                    (id_input,)
                )
                tournament = cursor.fetchone()

                if tournament:
                    print_as_table(cursor, tournament)

                    # Don't allow finished tournaments to be cancelled
                    if tournament[4] == "Finished":
                        print("Finished tournaments cannot be cancelled.")
                        pause_screen()
                        break

                    confirm = input(
                        f"Are you sure you want to cancel tournament "
                        f"'{tournament[1]}'? (yes/no): "
                    ).lower().strip()

                    if confirm == "yes":

                        # Delete matches for this tournament
                        cursor.execute(
                            "DELETE FROM Matches WHERE TournamentID = ?",
                            (tournament[0],)
                        )

                        # Delete tournament registrations
                        cursor.execute(
                            "DELETE FROM RegistrationList WHERE TournamentID = ?",
                            (tournament[0],)
                        )

                        # Delete tournament staff
                        cursor.execute(
                            "DELETE FROM TournamentStaff WHERE TournamentID = ?",
                            (tournament[0],)
                        )

                        # Delete tournament
                        cursor.execute(
                            "DELETE FROM Tournament WHERE TournamentID = ?",
                            (tournament[0],)
                        )

                        conn.commit()

                        print(
                            f"Tournament '{tournament[1]}' "
                            f"cancelled successfully."
                        )
                        pause_screen()
                        break

                    elif confirm == "no":
                        print("Cancellation cancelled.")
                        pause_screen()
                        break

                    else:
                        print("Please enter 'yes' or 'no'.")

                else:
                    print("No tournament found with that ID. Please try again.")
                    pause_screen()

        elif search == "name":
            while True:
                name = input(
                    "Enter Tournament name (or type 'back'): "
                ).strip()

                if name.lower() == "back":
                    break

                cursor.execute(
                    "SELECT * FROM Tournament WHERE TournamentName = ?",
                    (name,)
                )
                tournament = cursor.fetchone()

                if tournament:
                    print_as_table(cursor, tournament)

                    # Don't allow finished tournaments to be cancelled
                    if tournament[4] == "Finished":
                        print("Finished tournaments cannot be cancelled.")
                        pause_screen()
                        break

                    confirm = input(
                        f"Are you sure you want to cancel tournament "
                        f"'{tournament[1]}'? (yes/no): "
                    ).lower().strip()

                    if confirm == "yes":

                        # Delete matches for this tournament
                        cursor.execute(
                            "DELETE FROM Matches WHERE TournamentID = ?",
                            (tournament[0],)
                        )

                        # Delete tournament registrations
                        cursor.execute(
                            "DELETE FROM RegistrationList WHERE TournamentID = ?",
                            (tournament[0],)
                        )

                        # Delete tournament staff
                        cursor.execute(
                            "DELETE FROM TournamentStaff WHERE TournamentID = ?",
                            (tournament[0],)
                        )

                        # Delete tournament
                        cursor.execute(
                            "DELETE FROM Tournament WHERE TournamentID = ?",
                            (tournament[0],)
                        )

                        conn.commit()

                        print(
                            f"Tournament '{tournament[1]}' "
                            f"cancelled successfully."
                        )
                        pause_screen()
                        break

                    elif confirm == "no":
                        print("Cancellation cancelled.")
                        pause_screen()
                        break

                    else:
                        print("Please enter 'yes' or 'no'.")

                else:
                    print("No tournament found with that name. Please try again.")
                    pause_screen()

        else:
            print("Invalid search option. Please enter 'ID' or 'Name'.")
            pause_screen()

        clear_screen()



def manage_matches():
    if user_position in ["Administrator", "Moderator"]:
        clear_screen()
        print("-" * 75)
        print("                       Manage Matches")
        print("-" * 75)
        print("  [1] View Match Details           [4] Delete Match")
        print("  [2] Edit Match Details           [0] Back to Main Menu ")
        print("  [3] Create match  ")
        print("")
        return input("\nSelect an option: ").strip()
    elif user_position == "Staff":
        clear_screen()
        print("-" * 50)
        print("              Manage Matches")
        print("-" * 50)
        print("  [1] View Match Details")
        print("  [2] Edit Match Details")
        print("  [0] Back to Main Menu")
        print("")
        return input("\nSelect an option: ").strip()



def view_match_details():
    while True:
        clear_screen()
        print("-" * 60)
        print("                     View Match Details")
        print("-" * 60)
        category = input("""
[1] View All Matches in a Tournament        [3] View a Player's Matches
[2] View Specific Match Details             [0] Back
""")
        if category == "0":
            break

        elif category == "1":
            clear_screen()
            print("-" * 60)
            print("             View all Matches in a Tournament")
            print("-" * 60)

            tournament_id = input("Enter Tournament ID: ").strip()

            cursor.execute("""
            SELECT 
                Matches.MatchesID,
                Player1.PlayerID || ' - ' || Player1.Username AS Player1,
                Player2.PlayerID || ' - ' || Player2.Username AS Player2,
                WinnerPlayer.PlayerID || ' - ' || WinnerPlayer.Username AS Winner,
                Matches.MatchStatus,
                Matches.Round
            FROM Matches
            JOIN Player AS Player1 ON Matches.Player1 = Player1.PlayerID
            JOIN Player AS Player2 ON Matches.Player2 = Player2.PlayerID
            LEFT JOIN Player AS WinnerPlayer ON Matches.Winner = WinnerPlayer.PlayerID
            WHERE Matches.TournamentID = ?""", (tournament_id,))

            matches = cursor.fetchall()
            if matches:
                cursor.execute("SELECT COUNT(MatchesID) FROM Matches WHERE TournamentID =?", (tournament_id,))
                num_matches = cursor.fetchone()
                print(f"Total number of matches: {num_matches}")
                print_as_table(cursor, matches)
                pause_screen()
            else:
                print("\nNo matches found for that ID, did you enter the ID correctly?")
                pause_screen()

        elif category == "2":
            clear_screen()
            print("-" * 60)
            print("             View specific Matches details")
            print("-" * 60)

            matches_id = input("Enter Match ID: ").strip()

            cursor.execute("""
            SELECT 
                Matches.MatchesID,
                Player1.PlayerID || ' - ' || Player1.Username AS Player1,
                Player2.PlayerID || ' - ' || Player2.Username AS Player2,
                WinnerPlayer.PlayerID || ' - ' || WinnerPlayer.Username AS Winner,
                Matches.MatchStatus,
                Matches.Round
            FROM Matches
            JOIN Player AS Player1 ON Matches.Player1 = Player1.PlayerID
            JOIN Player AS Player2 ON Matches.Player2 = Player2.PlayerID
            LEFT JOIN Player AS WinnerPlayer ON Matches.Winner = WinnerPlayer.PlayerID
            WHERE Matches.MatchesID = ?""", (matches_id,))

            matches = cursor.fetchone()
            if matches:
                print_as_table(cursor, matches)
                pause_screen()
            else:
                print("\nNo Match found with that ID")
                pause_screen()

        elif category == "3":
            clear_screen()
            print("-" * 60)
            print("         View Matches details of a Player")
            print("-" * 60)

            player_id = input("Enter Player ID: ").strip()

            cursor.execute("SELECT 1 FROM Player WHERE PlayerID = ?", (player_id,))
            player_exists = cursor.fetchone()

            if not player_exists:
                print("No player found with that ID, please try again.")
                pause_screen()
                continue

            cursor.execute("""
            SELECT 
                Matches.MatchesID,
                Player1.PlayerID || ' - ' || Player1.Username AS Player1,
                Player2.PlayerID || ' - ' || Player2.Username AS Player2,
                WinnerPlayer.PlayerID || ' - ' || WinnerPlayer.Username AS Winner,
                Matches.MatchStatus,
                Matches.Round
            FROM Matches
            JOIN Player AS Player1 ON Matches.Player1 = Player1.PlayerID
            JOIN Player AS Player2 ON Matches.Player2 = Player2.PlayerID
            LEFT JOIN Player AS WinnerPlayer ON Matches.Winner = WinnerPlayer.PlayerID
            WHERE Matches.Player1 = ? OR Matches.Player2 = ?""", (player_id, player_id))

            matches = cursor.fetchall()
            if matches:
                print_as_table(cursor, matches)
                pause_screen()
            else:
                print("\nNo matches found for that player ID")
                pause_screen() 

        else:
            print("Invalid search option. Please enter 'ID' or 'Name'.")
            pause_screen()

        clear_screen()

                

def create_new_match():
    while True:
        clear_screen()
        print("-" * 60)
        print("                  Create New Match")
        print("-" * 60)
        
        cursor.execute("SELECT MAX(MatchesID) FROM Matches;")
        result = cursor.fetchone()
    
        if result is None or result[0] is None:
            next_number = 1
        else:
            current_id = result[0]
            next_number = int(current_id[1:]) + 1
    
        matches_id = f"M{next_number:03d}"
        match_status = "To be played"
        match_winner = None

        print(f"Generated Match ID: {matches_id}")
        print(f"Match Status: {match_status}")
        print(f"Match winner: None")
    
        while True:
            tournament_id = input("Enter Tournament ID (or 'back' to go back): ").strip()

            if tournament_id.lower() == "back":
                return

            cursor.execute("SELECT * FROM Tournament WHERE TournamentID = ?", (tournament_id,))
            tourney = cursor.fetchone()
            if tourney:
                break
            else:
                print("No Tournament exists with that ID. Please try again:")
                pause_screen()

        while True:
            player1 = input("Enter the first player's ID:").strip()
            cursor.execute("SELECT * FROM Player WHERE PlayerID = ?", (player1,))
            player1_exists = cursor.fetchone()

            if player1_exists:
                cursor.execute("SELECT * FROM RegistrationList WHERE PlayerID = ? AND TournamentID = ?", (player1, tournament_id))
                player1_registered = cursor.fetchone()

                if player1_registered:

                    player2 = input("Enter the second player's ID:").strip()

                    if player2 == player1:
                        print("A player cannot play against themselves.")
                        pause_screen()
                        continue

                    cursor.execute("SELECT * FROM Player WHERE PlayerID = ?", (player2,))
                    player2_exists = cursor.fetchone()
                    
                    if player2_exists:
                        cursor.execute("SELECT * FROM RegistrationList WHERE PlayerID = ? AND TournamentID = ?", (player2, tournament_id))
                        player2_registered = cursor.fetchone()
                        if player2_registered:
                            break
                        else:
                            print(f"Player {player2} isn't registered for the tournament")
                            pause_screen()
                    else:
                        print("\nInvalid player ID, please try again")
                        pause_screen()
                else:
                    print(f"Player {player1} isn't registered for the tournament")
                    pause_screen()
            else:
                print("\nInvalid player ID, please try again")
                pause_screen()

        while True:
            round_number = input("Enter round number")
            if round_number.isdigit():
                break
            else:
                print("\nEnter a valid number:")
                pause_screen()

        cursor.execute("""
            INSERT INTO Matches (MatchesID, tournamentID, Player1, Player2, Winner, MatchStatus, Round) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (matches_id, tournament_id, player1, player2, match_winner, match_status, round_number))

        conn.commit()

        print(f"\nMatch added successfully.")
        pause_screen()
        break



def edit_match_details():
    clear_screen()
    while True:
        print("-" * 60)
        print("                  Edit Match Details")
        print("-" * 60)

        while True:
            id_input = input("Enter Tournament ID (or type 'back'): ").strip().upper()
            if id_input.lower() == "back":
                break
            cursor.execute("SELECT * FROM Matches WHERE MatchesID = ?",(id_input,))
            matches = cursor.fetchone()

            if matches:
                edit_match_details_checks(matches, cursor)
                break
            else:
                print("No Match found with that ID. Please try again.")
                pause_screen()
            clear_screen()



def edit_match_details_checks(matches, cursor):
    print_as_table(cursor, matches)

    matchid = matches[0]

    print("Please enter the match data you wish to change.")
    print("If you do not wish to change anything in a specific column, just click enter.")

    # Tournament ID
    while True:
        tournamentid = input("Enter Tournament ID: ")

        if tournamentid == "":
            tournamentid = matches[1]
            break

        cursor.execute(
            """
            SELECT TournamentID
            FROM Tournament
            WHERE TournamentID = ?
            """,
            (tournamentid,)
        )

        if cursor.fetchone():
            break
        else:
            print("Enter a valid Tournament ID.")
            pause_screen()

    # Player 1
    while True:
        player1 = input("Enter Player 1 ID: ")

        if player1 == "":
            player1 = matches[2]
            break

        cursor.execute(
            """
            SELECT PlayerID
            FROM RegistrationList
            WHERE TournamentID = ? AND PlayerID = ?
            """,
            (tournamentid, player1)
        )

        if cursor.fetchone():
            break
        else:
            print("Player 1 must be registered for this tournament.")
            pause_screen()

    # Player 2
    while True:
        player2 = input("Enter Player 2 ID: ")

        if player2 == "":
            player2 = matches[3]
            break

        if player2 == player1:
            print("Player 1 and Player 2 cannot be the same player.")
            pause_screen()
            continue

        cursor.execute(
            """
            SELECT PlayerID
            FROM RegistrationList
            WHERE TournamentID = ? AND PlayerID = ?
            """,
            (tournamentid, player2)
        )

        if cursor.fetchone():
            break
        else:
            print("Player 2 must be registered for this tournament.")
            pause_screen()

    # Winner
    while True:
        winner = input("Enter winner (Player ID): ")

        # User wants to keep existing winner
        if winner == "":
            winner = matches[4]

            # If there is no existing winner, that's fine
            if winner is None:
                break

            # Make sure existing winner is still one of the new players
            if winner == player1 or winner == player2:
                break

            print(
                "The current winner is no longer one of the players "
                "in this match."
            )
            print("Please enter a new winner.")
            pause_screen()
            continue

        # User entered a new winner
        if winner == player1 or winner == player2:
            break

        print("Winner must be either Player 1 or Player 2.")
        pause_screen()

    # Match Status
    while True:
        match_status = input(
            "Enter Match Status "
            "('To be played', 'In progress', 'Finished'): "
        )

        if match_status == "":
            match_status = matches[5]
            break

        elif match_status in [
            "To be played",
            "In progress",
            "Finished"
        ]:
            break

        else:
            print(
                "Enter from 'To be played', "
                "'In progress', or 'Finished'."
            )
            pause_screen()

    # Make Winner and MatchStatus agree
    if match_status == "Finished":

        # Finished matches MUST have a winner
        while winner is None:
            print("A finished match must have a winner.")

            winner = input("Enter winner (Player ID): ")

            if winner == player1 or winner == player2:
                break

            print("Winner must be either Player 1 or Player 2.")
            pause_screen()

    else:

        # Unfinished matches cannot have a winner
        winner = None

    # Round
    while True:
        round_input = input("Enter round number: ")

        if round_input == "":
            round_number = matches[6]
            break

        try:
            round_number = int(round_input)

            if round_number > 0:
                break

            print("Round number must be greater than 0.")
            pause_screen()

        except ValueError:
            print("Enter a valid whole number.")
            pause_screen()

    # Update Match
    cursor.execute(
        """
        UPDATE Matches
        SET TournamentID = ?,
            Player1 = ?,
            Player2 = ?,
            Winner = ?,
            MatchStatus = ?,
            Round = ?
        WHERE MatchesID = ?
        """,
        (
            tournamentid,
            player1,
            player2,
            winner,
            match_status,
            round_number,
            matchid
        )
    )

    conn.commit()

    print("Match details updated successfully.")
    pause_screen()



def delete_match():
    while True:
        clear_screen()
        print("-" * 60)
        print("                  Delete Match")
        print("-" * 60)

        id_input = input("Enter Match ID to delete (or type 'back'): ").strip().upper()
        
        if id_input == "BACK":
            break

        cursor.execute("SELECT * FROM Matches WHERE MatchesID = ?", (id_input,))
        matches = cursor.fetchone()

        if matches:
            print_as_table(cursor, matches)
            if matches[5] == "Finished":
                print("Finished matches cannot be cancelled.")
                pause_screen()
                continue  

            confirm = input(f"Are you sure you want to cancel this match? (yes/no): ").lower().strip()
            if confirm == "yes":
                cursor.execute("DELETE FROM Matches WHERE MatchesID = ?", (matches[0],))
                conn.commit()
                print("Match cancelled successfully")
                pause_screen()
                break  

            elif confirm == "no":
                print("Cancellation cancelled.")
                pause_screen()
                break 
                
            else:
                print("Please enter 'yes' or 'no'.")
                pause_screen()
        else:
            print("No match found with that ID. Please try again.")
            pause_screen()

        clear_screen()



def manage_cards():
    if user_position in ["Administrator", "Moderator"]:
        clear_screen()
        print("-" * 75)
        print("                       Manage Cards")
        print("-" * 75)
        print("  [1] View Card Details           [4] Delete Card")
        print("  [2] Edit Card Details           [0] Back to Main Menu ")
        print("  [3] Create Card  ")
        print("")
        return input("\nSelect an option: ").strip()
    elif user_position == "Staff":
        return



def view_card_details():
    #search specific card by cardID OR cardName
    #view list of cards by element/type/rarity AND count total number of cards
    #view all cards sorted by HP DESC
    #view all cards with HP higher than a specific value
    while True:
        clear_screen()
        print("-" * 60)
        print("                     View Card Details")
        print("-" * 60)
        category = input("""
[1] View Specific Card Details                     [4] View cards with HP higher than -
[2] View all cards of a specific element/rarity    [0] Back
[3] View all cards""")
        
        if category == "0":
            break
        elif category == "1":
            while True:
                clear_screen()
                print("-" * 60)
                print("             View Specific Card Details")
                print("-" * 60)

                while True:
                    choice = input("Search by Card 'Name' or 'ID' (or type 'back')").strip().lower()
                    if choice == "back":
                        break
                    elif choice == "id":
                        card_id = input("Enter Card ID:")
                        cursor.execute("SELECT * FROM Card WHERE CardID = ?", (card_id,))
                        card = cursor.fetchone()
                        if card:
                            print_as_table(cursor, card)
                            pause_screen()
                        else:
                            print("\nInvalid Card ID")
                            pause_screen()
                    elif choice == "name":
                        cardname = input("Enter Card Name:")
                        cursor.execute("SELECT * FROM Card WHERE CardName = ?", (cardname,))
                        card = cursor.fetchone()
                        if card:
                            print_as_table(cursor, card)
                            pause_screen()
                        else:
                            print("\nInvalid Card name")
                            pause_screen()
        elif category == "2":
            while True:
                clear_screen()
                print("-" * 60)
                print("             View All card of  a specific type")
                print("-" * 60)

                while True:
                    choice = input("Select from: Creature, Trainer, Energy, Element, Rarity (or type 'back')").strip().lower()
                    if choice == "back":
                        break
                    elif choice == "creature":
                        cursor.execute("SELECT COUNT(CardID) FROM Card WHERE CardType = 'Creature Card'")
                        num_cards = cursor.fetchone()[0]
                        print(f"Total Number of Creature Cards: {num_cards}")
                        cursor.execute("SELECT * FROM Card WHERE CardType = 'Creature Card'")
                        cards = cursor.fetchall()
                        if cards:
                            print_as_table(cursor, cards)
                            pause_screen()
                        else:
                            print("\nNo Creature Cards found")
                            pause_screen()
                    elif choice == "trainer":
                        cursor.execute("SELECT COUNT(CardID) FROM Card WHERE CardType = 'Trainer Card'")
                        num_cards = cursor.fetchone()[0]
                        print(f"Total Number of Trainer Cards: {num_cards}")
                        cursor.execute("SELECT * FROM Card WHERE CardType = 'Trainer Card'")
                        cards = cursor.fetchall()
                        if cards:
                            print_as_table(cursor, cards)
                            pause_screen()
                        else:
                            print("\nNo Trainer Cards found")
                            pause_screen()
                    elif choice == "energy":
                        cursor.execute("SELECT COUNT(CardID) FROM Card WHERE CardType = 'Energy Card'")
                        num_cards = cursor.fetchone()[0]
                        print(f"Total Number of Energy Cards: {num_cards}")
                        cursor.execute("SELECT * FROM Card WHERE CardType = 'Energy Card'")
                        cards = cursor.fetchall()
                        if cards:
                            print_as_table(cursor, cards)
                            pause_screen()
                        else:
                            print("\nNo Energy Cards found")
                            pause_screen()
                    elif choice == "element":
                        element = input("Enter Element:")
                        cursor.execute("""
                            SELECT * FROM C
                        """)
                        cursor.execute("SELECT COUNT(CardID) FROM Card WHERE CardType = 'Energy Card'")
                        num_cards = cursor.fetchone()[0]
                        print(f"Total Number of Energy Cards: {num_cards}")
                        cursor.execute("SELECT * FROM Card WHERE CardType = 'Energy Card'")
                        cards = cursor.fetchall()
                        if cards:
                            print_as_table(cursor, cards)
                            pause_screen()
                        else:
                            print("\nNo Energy Cards found")
                            pause_screen()
                    

                

                            




def edit_card():
    pass

def create_card():
    pass

def delete_card():
    pass


def manage_decks():
    if user_position in ["Administrator", "Moderator"]:
        clear_screen()
        print("-" * 75)
        print("                       Manage Decks")
        print("-" * 75)
        print("  [1] View all cards in a Deck")
        print("  [2] View all decks containing a specific card")
        print("  [0] Back to Main Menu  ")
        print("")
        return input("\nSelect an option: ").strip()
    elif user_position == "Staff":
        return



def view_deck_cards():
    while True:
        clear_screen()
        print("-" * 60)
        print("                     View Cards in a Deck")
        print("-" * 60)
        category = input("Seach by Deck 'Name' or 'ID' (or type 'back')").strip().lower()
        
        if category == "back":
            break
        elif category == "id":
            while True:
                deck_id = input("Enter Deck ID:")
                cursor.execute("SELECT * FROM Deck WHERE DeckID = ?", (deck_id,))
                deck = cursor.fetchone()
                if deck:

                    cursor.execute("""
                    SELECT Deck.DeckID, Deck.DeckName, Player.Username, 
                    SUM(CardInDeck.Quantity) AS 'Total Cards In Deck',
                    COUNT(CardInDeck.CardID) AS 'Number of Unique Cards', 
                    SUM(CASE WHEN Card.CardType = 'Creature Card' THEN CardInDeck.Quantity ELSE 0 END) AS 'Creature Cards',
                    SUM(CASE WHEN Card.CardType = 'Trainer Card' THEN CardInDeck.Quantity ELSE 0 END) AS 'Trainer Cards',
                    SUM(CASE WHEN Card.CardType = 'Energy Card' THEN CardInDeck.Quantity ELSE 0 END) AS 'Energy Cards'
                    FROM Deck
                    JOIN Player ON Player.PlayerID = Deck.PlayerID
                    JOIN CardInDeck ON CardInDeck.DeckID = Deck.DeckID
                    JOIN Card ON Card.CardID = CardInDeck.CardID
                    WHERE Deck.deckid = ?
                    GROUP BY Deck.DeckID, Deck.DeckName, Player.Username;""", (deck_id,))

                    deck_stats = cursor.fetchone()
                    print_as_table(cursor, deck_stats)

                    cursor.execute("""
                    SELECT Card.CardID, CardName, Rarity 
                    FROM Card 
                    JOIN CardInDeck ON CardInDeck.CardID = Card.CardID
                    WHERE CardInDeck.DeckID = ?
                    ORDER BY CASE 
                                WHEN UPPER(Card.Rarity) LIKE '%SPECIAL ILLUSTRATION%' THEN 1
                                WHEN UPPER(Card.Rarity) LIKE '%ILLUSTRATION RARE%'   THEN 2
                                WHEN UPPER(Card.Rarity) LIKE '%HYPER RARE%'          THEN 3
                                WHEN UPPER(Card.Rarity) LIKE '%ULTRA RARE%'          THEN 4
                                WHEN UPPER(Card.Rarity) LIKE '%ACE SPEC%'            THEN 5
                                WHEN UPPER(Card.Rarity) LIKE '%DOUBLE RARE%'         THEN 6
                                WHEN UPPER(Card.Rarity) LIKE '%RARE HOLO%'           THEN 7
                                WHEN UPPER(Card.Rarity) LIKE '%RARE%'                THEN 8
                                WHEN UPPER(Card.Rarity) LIKE '%UNCOMMON%'            THEN 9
                                WHEN UPPER(Card.Rarity) LIKE '%COMMON%'              THEN 10
                                ELSE 11
                            END ASC;""", (deck_id,))

                    cards = cursor.fetchall()
                    print_as_table(cursor, cards)
                    pause_screen()
                    break

                else:
                    print("\nDeck not found, try again.")
                    pause_screen()
                    clear_screen()
        
        elif category == "name":
            while True:
                deck_name = input("Enter Deck Name:")
                cursor.execute("SELECT * FROM Deck WHERE DeckName = ?", (deck_name,))
                deck = cursor.fetchone()
                if deck:

                    cursor.execute("""
                    SELECT Deck.DeckID, Deck.DeckName, Player.Username, 
                    SUM(CardInDeck.Quantity) AS 'Total Cards In Deck',
                    COUNT(CardInDeck.CardID) AS 'Number of Unique Cards', 
                    SUM(CASE WHEN Card.CardType = 'Creature Card' THEN CardInDeck.Quantity ELSE 0 END) AS 'Creature Cards',
                    SUM(CASE WHEN Card.CardType = 'Trainer Card' THEN CardInDeck.Quantity ELSE 0 END) AS 'Trainer Cards',
                    SUM(CASE WHEN Card.CardType = 'Energy Card' THEN CardInDeck.Quantity ELSE 0 END) AS 'Energy Cards'
                    FROM Deck
                    JOIN Player ON Player.PlayerID = Deck.PlayerID
                    JOIN CardInDeck ON CardInDeck.DeckID = Deck.DeckID
                    JOIN Card ON Card.CardID = CardInDeck.CardID
                    WHERE Deck.DeckName = ?
                    GROUP BY Deck.DeckID, Deck.DeckName, Player.Username;""", (deck_name,))

                    deck_stats = cursor.fetchone()
                    print_as_table(cursor, deck_stats)

                    cursor.execute("""
                    SELECT Card.CardID, CardName, Rarity 
                    FROM Card 
                    JOIN CardInDeck ON CardInDeck.CardID = Card.CardID
                    JOIN Deck ON CardInDeck.DeckID = Deck.DeckID
                    WHERE Deck.DeckName = ?
                    ORDER BY CASE 
                                WHEN UPPER(Card.Rarity) LIKE '%SPECIAL ILLUSTRATION%' THEN 1
                                WHEN UPPER(Card.Rarity) LIKE '%ILLUSTRATION RARE%'   THEN 2
                                WHEN UPPER(Card.Rarity) LIKE '%HYPER RARE%'          THEN 3
                                WHEN UPPER(Card.Rarity) LIKE '%ULTRA RARE%'          THEN 4
                                WHEN UPPER(Card.Rarity) LIKE '%ACE SPEC%'            THEN 5
                                WHEN UPPER(Card.Rarity) LIKE '%DOUBLE RARE%'         THEN 6
                                WHEN UPPER(Card.Rarity) LIKE '%RARE HOLO%'           THEN 7
                                WHEN UPPER(Card.Rarity) LIKE '%RARE%'                THEN 8
                                WHEN UPPER(Card.Rarity) LIKE '%UNCOMMON%'            THEN 9
                                WHEN UPPER(Card.Rarity) LIKE '%COMMON%'              THEN 10
                                ELSE 11
                            END ASC;""", (deck_name,))

                    cards = cursor.fetchall()
                    print_as_table(cursor, cards)
                    pause_screen()
                    break

                else:
                    print("\nDeck not found, try again.")
                    pause_screen()
                    clear_screen()
        else:
            print("Invalid option")
            pause_screen()

                    
                    
def view_all_decks_containing_specific_card():
    #search by cardID
    #display list of deckID, deckName, Quantity containing that card
    while True:
        clear_screen()
        print("-" * 60)
        print("                     View All Decks Containing A Specific Card")
        print("-" * 60)
        category = input("Seach for Card by 'Name' or 'ID' (or type 'back')").strip().lower()

        if category == "back":
            break
        elif category == "id":
            while True:
                card_id = input("Enter Card ID:")
                cursor.execute("SELECT * FROM Card WHERE CardID = ?", (card_id,))
                card = cursor.fetchone()
                if card:
                    cursor.execute("""
                    SELECT Deck.DeckID, Deck.DeckName, CardInDeck.Quantity  
                    FROM CardInDeck
                    JOIN Deck ON CardInDeck.DeckID = Deck.DeckID
                    WHERE CardInDeck.CardID = ?""", (card_id,))
                    decks = cursor.fetchall()
                    if decks:
                        print_as_table(cursor, decks)
                        pause_screen()
                    else:
                        print("\n No decks contain this card")
                        pause_screen()
                else:
                    print("\nCard not found")
                    pause_screen()


        elif category == "name":
            while True:
                card_name = input("Enter Card Name:")
                cursor.execute("SELECT * FROM Card WHERE CardName = ?", (card_name,))
                card = cursor.fetchone()
                if card:
                    cursor.execute("""
                    SELECT Deck.DeckID, Deck.DeckName, CardInDeck.Quantity  
                    FROM CardInDeck
                    JOIN Deck ON CardInDeck.DeckID = Deck.DeckID
                    JOIN Card ON CardInDeck.CardID = Card.CardID
                    WHERE Card.CardName = ?""", (card_name,))
                    decks = cursor.fetchall()
                    if decks:
                        print_as_table(cursor, decks)
                        pause_screen()
                    else:
                        print("\n No decks contain this card")
                        pause_screen()
                else:
                    print("\nCard not found")
                    pause_screen()
        else:
            print("Enter 'id', 'name' or 'Back'")
            pause_screen()



def manage_staff():
    if user_position == "Administrator":
        clear_screen()
        print("-" * 75)
        print("                     Manage Staff Members")
        print("-" * 75)
        print("  [1] View Staff Details             [4] Delete Staff Member")
        print("  [2] Edit Staff Details             [0] Back to Main Menu ")
        print("  [3] Create New Staff Member")
        print("")
        return input("\nSelect an option: ").strip()
    elif user_position in ["Staff", "Moderator"]:
        return



def view_staff_details():
    #view all staff details (ordered by role)
    #search for staff members by role
    #search for specific staff member by id or username
    pass

def edit_staff_details():
    #edit by id
    pass

def create_new_staff_member():
    #straighforward
    pass

def delete_staff_member():
    #straightforward
    pass

def generate_analytical_reports():
    pass

    #• Display the players with the largest card collections. (top 10)
    #• Display the most commonly owned card (SELECT * FROM Card)
    #• Display the rarest cards in the database. (top 10)
    #• Calculate the maximum and minimum HP. 
    #• Display the total number of players/cards/decks/tournaments/tournament registries






def main():
    if login():
        while True:
            menu_option = main_menu()
            if menu_option == "0":
                log_out()
            elif menu_option == "1":
                while True: 
                    manage_players_option = manage_players()
                    if manage_players_option == "0":
                        break
                    elif manage_players_option == "1":
                        view_account_details()
                    elif manage_players_option == "2":
                        edit_account_details()
                    elif manage_players_option == "3":
                        view_player_stats()
                    elif manage_players_option == "4":
                        add_new_player()
                    elif manage_players_option == "5":
                        delete_player()
                    else:
                        print("Invalid option selected.")
                        pause_screen()
            elif menu_option == "2":
                while True:
                    manage_tournaments_option = manage_tournaments()
                    if manage_tournaments_option == "0":
                        break
                    elif manage_tournaments_option == "1":
                        view_tournament_details()
                    elif manage_tournaments_option == "2":
                        edit_tournament_details()
                    elif manage_tournaments_option == "3":
                        register_remove_players()
                    elif manage_tournaments_option == "4":
                        create_new_tournament()
                    elif manage_tournaments_option == "5":
                        cancel_tournament()
                    else: 
                        print("Invalid option selected.")
                        pause_screen()
            elif menu_option == "3":
                while True:
                    manage_matches_option = manage_matches()
                    if manage_matches_option == "0":
                        break
                    elif manage_matches_option == "1":
                        view_match_details()
                    elif manage_matches_option == "2":
                        edit_match_details()
                    elif manage_matches_option == "3":
                        create_new_match()
                    elif manage_matches_option == "4":
                        delete_match()
                    else: 
                        print("Invalid option selected.")
                        pause_screen()
            elif menu_option == "4":
                while True:
                    manage_cards_option = manage_cards()
                    if manage_cards_option == "0":
                        break
                    elif manage_cards_option == "1":
                        view_card_details()
                    elif manage_cards_option == "2":
                        edit_card()
                    elif manage_cards_option == "3":
                        create_card()
                    elif manage_cards_option == "4":
                        delete_card()
                    else: 
                        print("Invalid option selected.")
                        pause_screen()
            elif menu_option == "5":
                while True:
                    manage_decks_option = manage_decks()
                    if manage_decks_option == "0":
                        break
                    elif manage_decks_option == "1":
                        view_deck_cards()
                    elif manage_decks_option == "2":
                        view_all_decks_containing_specific_card()
                    else: 
                        print("Invalid option selected.")
                        pause_screen()
            elif menu_option == "6":
                while True:
                    manage_staff_option = manage_staff()
                    if manage_staff_option == "0":
                        break
                    elif manage_staff_option == "1":
                        view_staff_details()
                    elif manage_staff_option == "2":
                        edit_staff_details()
                    elif manage_staff_option == "3":
                        create_new_staff_member()
                    elif manage_staff_option == "4":
                        delete_staff_member()
                    else:
                        print("Invalid option selected.")
                        pause_screen()
            elif menu_option == "7":
                generate_analytical_reports()
            else:
                print("Invalid option selected, please try again.")
                pause_screen()



main()
