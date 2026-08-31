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
    #Handle case where no data is found
    if data is None or data == []:
        print("\nNo data found.")
        return
    
    #If 'data' is a single tuple (one record), wrap it in a list
    if isinstance(data, tuple):
        records = [data]
    else:
        records = data

    #Extract headers from the cursor
    headers = [col[0] for col in cursor.description]

    #Calculate dynamic column widths across ALL records and headers
    col_widths = []
    for col_idx, header in enumerate(headers):
        max_len = len(header)
        for row in records:
            #Check the length of the string version of each cell
            max_len = max(max_len, len(str(row[col_idx])))
        col_widths.append(max_len + 4)  #Add padding

    #formatting template
    format_template = "".join([f"{{:<{w}}}" for w in col_widths])

    #print the table structure and data
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
    while True:
        clear_screen()
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
            continue
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
            continue
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
            continue
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

                        cursor.execute("DELETE FROM Matches WHERE Player1 = ? OR Player2 = ? OR Winner = ?", (player[0], player[0], player[0]))
                        cursor.execute("DELETE FROM RegistrationList WHERE PlayerID = ?", (player[0],))
                        cursor.execute("DELETE FROM PlayerCollection WHERE PlayerID = ?", (player[0],))
                        cursor.execute("""
                        DELETE FROM CardInDeck WHERE DeckID IN (
                            SELECT DeckID 
                            FROM Deck 
                            WHERE PlayerID = ?)
                        """, (player[0],))
                        cursor.execute("DELETE FROM Deck WHERE PlayerID = ?", (player[0],))
                        cursor.execute("""
                        DELETE FROM TradeCard WHERE TradeID IN (
                            SELECT TradeID 
                            FROM Trade 
                            WHERE SenderID = ? OR ReceiverID = ?)
                        """, (player[0], player[0]))
                        cursor.execute("DELETE FROM Trade WHERE SenderID = ? OR ReceiverID = ?", (player[0], player[0]))
                        cursor.execute("DELETE FROM PlayerWHERE PlayerID = ?", (player[0],))

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

                        cursor.execute("DELETE FROM Matches WHERE Player1 = ? OR Player2 = ? OR Winner = ?", (player[0], player[0], player[0]))
                        cursor.execute("DELETE FROM RegistrationList WHERE PlayerID = ?", (player[0],))
                        cursor.execute("DELETE FROM PlayerCollection WHERE PlayerID = ?", (player[0],))
                        cursor.execute("""
                        DELETE FROM CardInDeck WHERE DeckID IN (
                            SELECT DeckID 
                            FROM Deck 
                            WHERE PlayerID = ?)
                        """, (player[0],))
                        cursor.execute("DELETE FROM Deck WHERE PlayerID = ?", (player[0],))
                        cursor.execute("""
                        DELETE FROM TradeCard WHERE TradeID IN (
                            SELECT TradeID 
                            FROM Trade 
                            WHERE SenderID = ? OR ReceiverID = ?)
                        """, (player[0], player[0]))
                        cursor.execute("DELETE FROM Trade WHERE SenderID = ? OR ReceiverID = ?", (player[0], player[0]))
                        cursor.execute("DELETE FROM PlayerWHERE PlayerID = ?", (player[0],))

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
            continue
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
    while True:
        clear_screen()
        print("-" * 90)
        print("                             View Card Details")
        print("-" * 90)
        category = input("""
[1] View Specific Card Details                                [3] View all cards
[2] View cards of a specific card type/element type/rarity    [0] Back""")
        
        if category == "0":
            break
        elif category == "1":
            while True:
                clear_screen()
                print("-" * 60)
                print("             View Specific Card Details")
                print("-" * 60)
                choice = input("Search by Card 'Name' or 'ID' (or type 'back'): ").strip().lower()
                if choice == "back":
                    break
                elif choice == "id":
                    while True:
                        card_id = input("Enter Card ID: ").strip()
                        cursor.execute("SELECT * FROM Card WHERE CardID = ?", (card_id,))
                        card = cursor.fetchone()
                        if card:
                            print_as_table(cursor, [card])  # Wrapped in list for table formatting
                            pause_screen()
                            break
                        else:
                            print("\nInvalid Card ID")
                            pause_screen()
                elif choice == "name":
                    while True:
                        cardname = input("Enter Card Name: ").strip()
                        cursor.execute("SELECT * FROM Card WHERE CardName LIKE ?", (f"%{cardname}%",))
                        cards = cursor.fetchall()
                        if cards:
                            print_as_table(cursor, cards)
                        else:
                            print("\nInvalid Card name")
                            pause_screen()
                    
        elif category == "2":
            while True:
                clear_screen()
                print("-" * 60)
                print("             View Cards by Category")
                print("-" * 60)
                choice = input("Select from: Creature, Trainer, Energy, Type, Rarity (or type 'back'): ").strip().lower()
                if choice == "back":
                    break

                elif choice in ["creature", "trainer", "energy"]:
                    while True:
                        # Map input string to your stored database CardType strings
                        type_map = {"creature": "Creature Card", "trainer": "Trainer Card", "energy": "Energy Card"}
                        target_type = type_map[choice]
                        
                        cursor.execute("SELECT COUNT(CardID) FROM Card WHERE CardType = ?", (target_type,))
                        num_cards = cursor.fetchone()[0]
                        print(f"\nTotal Number of {target_type}s: {num_cards}")
                        
                        cursor.execute("SELECT * FROM Card WHERE CardType = ?", (target_type,))
                        cards = cursor.fetchall()
                        if cards:
                            print_as_table(cursor, cards)
                            pause_screen()
                            break
                        else:
                            print(f"\nNo {target_type}s found")
                            pause_screen()

                elif choice == "type":
                    while True:
                        element_type = input("Enter Type (e.g., Fire, Water, Lightning): ").strip()
                        cursor.execute("""
                        SELECT Card.* 
                        FROM Card
                        LEFT JOIN CreatureCard ON CreatureCard.CardID = Card.CardID
                        LEFT JOIN EnergyCard ON EnergyCard.CardID = Card.CardID
                        WHERE CreatureCard.ElementType = ? OR EnergyCard.ElementType = ?
                        """, (element_type, element_type))
                        cards = cursor.fetchall()
                        print(f"\nTotal Cards of Element '{element_type}': {len(cards)}")
                        if cards:
                            print_as_table(cursor, cards)
                            pause_screen()
                            break
                        else:
                            print("\nNo Cards of this Element found")
                            pause_screen()

                elif choice == "rarity":
                    while True:
                        rarity = input("Enter Rarity (e.g., Common, Rare, Ultra Rare): ").strip()
                        cursor.execute("SELECT * FROM Card WHERE Rarity LIKE ?", (f"%{rarity}%",))
                        cards = cursor.fetchall()
                        print(f"\nTotal Cards of Rarity '{rarity}': {len(cards)}")
                        if cards:
                            print_as_table(cursor, cards)
                            pause_screen()
                            break
                        else:
                            print("\nNo Cards of this Rarity found")
                            pause_screen()  

                else:
                    print("Invalid option")
                    pause_screen()

        elif category == "3":
            while True:
                clear_screen()
                print("-" * 60)
                print("             View All Cards")
                print("-" * 60)
                choice = input("Order by id, name, card number or rarity? (or type 'back'): ").strip().lower()
                if choice == "back":
                    break
                elif choice == "name":
                    cursor.execute("""
                    SELECT CardID, CardName, CardType, CardNumber, Rarity, SetName
                    FROM Card
                    JOIN CardSet ON Card.SetId = CardSet.SetID
                    ORDER BY CardName ASC""")
                    cards = cursor.fetchall()
                    if cards:
                        print_as_table(cursor, cards)
                        pause_screen()
                    else:
                        print("No Card Found (gasp)")
                        pause_screen()
                elif choice == "id":
                    cursor.execute("""
                    SELECT CardID, CardName, CardType, CardNumber, Rarity, SetName
                    FROM Card
                    JOIN CardSet ON Card.SetId = CardSet.SetID
                    ORDER BY CardID ASC""")
                    cards = cursor.fetchall()
                    if cards:
                        print_as_table(cursor, cards)
                        pause_screen()
                    else:
                        print("No Card Found (gasp)")
                        pause_screen()
                elif choice == "card number":
                    cursor.execute("""
                    SELECT CardID, CardName, CardType, CardNumber, Rarity, SetName
                    FROM Card
                    JOIN CardSet ON Card.SetId = CardSet.SetID
                    ORDER BY CardNUmber ASC""")
                    cards = cursor.fetchall()
                    if cards:
                        print_as_table(cursor, cards)
                        pause_screen()
                    else:
                        print("No Card Found (gasp)")
                        pause_screen()
                elif choice == "rarity":
                    cursor.execute("""
                    SELECT CardID, CardName, CardType, CardNumber, Rarity, SetName
                    FROM Card
                    JOIN CardSet ON Card.SEtId = CardSet.SetID
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
                        END ASC""")
                    cards = cursor.fetchall()
                    if cards:
                        print_as_table(cursor, cards)
                        pause_screen()
                    else:
                        print("No Card Found (gasp)")
                        pause_screen()
                else:
                    print("Invalid option")
                    pause_screen()

        else:
            print("invalid option")
            pause_screen



def edit_card():
    while True:
        clear_screen()
        print("-" * 60)
        print("                  Edit Card Details")
        print("-" * 60)

        category = input("""
[1] Edit Creature Card
[2] Edit Trainer Card
[3] Edit Energy Card
[0] Back

Select an option: """).strip()

        if category == "0":
            break

        elif category in ["1", "2", "3"]:

            type_map = {
                "1": "Creature Card",
                "2": "Trainer Card",
                "3": "Energy Card"
            }

            card_type = type_map[category]

            while True:
                clear_screen()
                print("-" * 60)
                print(f"              Edit {card_type}")
                print("-" * 60)

                choice = input(
                    "Enter Card ID or Card Name (or type 'back'): "
                ).strip()

                if choice.lower() == "back":
                    break

                cursor.execute("""
                    SELECT *
                    FROM Card
                    WHERE (CardID = ? OR CardName = ?)
                    AND CardType = ?
                """, (choice, choice, card_type))

                card = cursor.fetchone()

                if card:
                    edit_card_details_checks(card, cursor, card_type)
                    break
                else:
                    print("\nCard not found.")
                    pause_screen()

        else:
            print("Invalid option.")
            pause_screen()



def edit_card_details_checks(card, cursor, card_type):

    cardid = card[0]

    while True:
        clear_screen()
        print("-" * 60)
        print("                  Edit Card Details")
        print("-" * 60)

        print_as_table(cursor, [card])

        print("\nPlease enter the card data you wish to change.")
        print("If you do not wish to change a field, just press Enter.")

        # ==========================================
        # COMMON CARD DETAILS
        # ==========================================

        # Card Name
        while True:
            new_cardname = input(
                f"Update Card Name [{card[2]}]: "
            ).strip()

            if new_cardname == "":
                new_cardname = card[2]
                break

            cursor.execute("""
                SELECT CardID
                FROM Card
                WHERE CardName = ?
                AND CardID != ?
            """, (new_cardname, cardid))

            if cursor.fetchone():
                print("A card with that name already exists.")
            else:
                break

        # Set ID
        while True:
            new_setid = input(
                f"Update Set ID [{card[1]}]: "
            ).strip()

            if new_setid == "":
                new_setid = card[1]
                break

            cursor.execute("""
                SELECT SetID
                FROM CardSet
                WHERE SetID = ?
            """, (new_setid,))

            if cursor.fetchone():
                break

            print("Invalid Set ID.")

        # Card Number
        while True:
            new_cardnumber = input(
                f"Update Card Number [{card[4]}]: "
            ).strip()

            if new_cardnumber == "":
                new_cardnumber = card[4]
                break

            cursor.execute("""
                SELECT CardID
                FROM Card
                WHERE CardNumber = ?
                AND CardID != ?
            """, (new_cardnumber, cardid))

            if cursor.fetchone():
                print("A card with that number already exists.")
            else:
                break

        # Rarity
        new_rarity = input(
            f"Update Rarity [{card[5]}]: "
        ).strip()

        if new_rarity == "":
            new_rarity = card[5]

        # ==========================================
        # UPDATE CARD
        # ==========================================

        cursor.execute("""
            UPDATE Card
            SET SetID = ?,
                CardName = ?,
                CardNumber = ?,
                Rarity = ?
            WHERE CardID = ?
        """, (
            new_setid,
            new_cardname,
            new_cardnumber,
            new_rarity,
            cardid
        ))

        # ==========================================
        # CREATURE CARD
        # ==========================================

        if card_type == "Creature Card":

            cursor.execute("""
                SELECT EvolutionStage,
                       HP,
                       ElementType,
                       RetreatCost,
                       Weakness,
                       Resistance
                FROM CreatureCard
                WHERE CardID = ?
            """, (cardid,))

            creature = cursor.fetchone()

            # Evolution Stage
            new_evolution = input(
                f"Update Evolution Stage [{creature[0]}]: "
            ).strip()

            if new_evolution == "":
                new_evolution = creature[0]

            # HP
            while True:
                new_hp = input(
                    f"Update HP [{creature[1]}]: "
                ).strip()

                if new_hp == "":
                    new_hp = creature[1]
                    break

                if new_hp.isdigit() and int(new_hp) > 0:
                    new_hp = int(new_hp)
                    break

                print("HP must be a positive number.")

            # Element Type
            new_element = input(
                f"Update Element Type [{creature[2]}]: "
            ).strip()

            if new_element == "":
                new_element = creature[2]

            # Retreat Cost
            while True:
                new_retreat = input(
                    f"Update Retreat Cost [{creature[3]}]: "
                ).strip()

                if new_retreat == "":
                    new_retreat = creature[3]
                    break

                if new_retreat.isdigit() and int(new_retreat) >= 0:
                    new_retreat = int(new_retreat)
                    break

                print("Retreat Cost must be a number.")

            # Weakness
            new_weakness = input(
                f"Update Weakness [{creature[4]}]: "
            ).strip()

            if new_weakness == "":
                new_weakness = creature[4]

            # Resistance
            new_resistance = input(
                f"Update Resistance [{creature[5]}]: "
            ).strip()

            if new_resistance == "":
                new_resistance = creature[5]

            cursor.execute("""
                UPDATE CreatureCard
                SET EvolutionStage = ?,
                    HP = ?,
                    ElementType = ?,
                    RetreatCost = ?,
                    Weakness = ?,
                    Resistance = ?
                WHERE CardID = ?
            """, (
                new_evolution,
                new_hp,
                new_element,
                new_retreat,
                new_weakness,
                new_resistance,
                cardid
            ))

        # ==========================================
        # TRAINER CARD
        # ==========================================

        elif card_type == "Trainer Card":

            cursor.execute("""
                SELECT Subtype, Rules
                FROM TrainerCard
                WHERE CardID = ?
            """, (cardid,))

            trainer = cursor.fetchone()

            # Subtype
            new_subtype = input(
                f"Update Subtype [{trainer[0]}]: "
            ).strip()

            if new_subtype == "":
                new_subtype = trainer[0]

            # Rules
            new_rules = input(
                f"Update Rules [{trainer[1]}]: "
            ).strip()

            if new_rules == "":
                new_rules = trainer[1]

            cursor.execute("""
                UPDATE TrainerCard
                SET Subtype = ?,
                    Rules = ?
                WHERE CardID = ?
            """, (
                new_subtype,
                new_rules,
                cardid
            ))

        # ==========================================
        # ENERGY CARD
        # ==========================================

        elif card_type == "Energy Card":

            cursor.execute("""
                SELECT ElementType,
                       EnergyType,
                       SpecialEffects
                FROM EnergyCard
                WHERE CardID = ?
            """, (cardid,))

            energy = cursor.fetchone()

            # Element Type
            new_element = input(
                f"Update Element Type [{energy[0]}]: "
            ).strip()

            if new_element == "":
                new_element = energy[0]

            # Energy Type
            new_energytype = input(
                f"Update Energy Type [{energy[1]}]: "
            ).strip()

            if new_energytype == "":
                new_energytype = energy[1]

            # Special Effects
            new_effects = input(
                f"Update Special Effects [{energy[2]}]: "
            ).strip()

            if new_effects == "":
                new_effects = energy[2]

            cursor.execute("""
                UPDATE EnergyCard
                SET ElementType = ?,
                    EnergyType = ?,
                    SpecialEffects = ?
                WHERE CardID = ?
            """, (
                new_element,
                new_energytype,
                new_effects,
                cardid
            ))

        # ==========================================
        # EDIT / ADD ATTACKS AND ABILITIES
        # ==========================================

        if card_type == "Creature Card":

            # ==========================================
            # ATTACKS
            # ==========================================

            while True:
                attack_choice = input("""
Would you like to:
[1] Edit an existing attack
[2] Add a new attack
[3] Finish attacks

Select an option: """).strip()

                if attack_choice == "1":
                    edit_attack(cardid)

                elif attack_choice == "2":
                    add_attack(cardid)

                elif attack_choice == "3":
                    break

                else:
                    print("Invalid option.")
                    pause_screen()

            # ==========================================
            # ABILITIES
            # ==========================================

            while True:
                ability_choice = input("""
Would you like to:
[1] Edit an existing ability
[2] Add a new ability
[3] Finish abilities

Select an option: """).strip()

                if ability_choice == "1":
                    edit_ability(cardid)

                elif ability_choice == "2":
                    add_ability(cardid)

                elif ability_choice == "3":
                    break

                else:
                    print("Invalid option.")
                    pause_screen()

        # ==========================================
        # SAVE CHANGES
        # ==========================================

        conn.commit()

        print("\nCard details updated successfully!")
        pause_screen()
        break



def edit_attack(card_id):

    cursor.execute("""
        SELECT AttackID, AttackName, Damage, EnergyCost, Effect
        FROM AttackDetails
        WHERE CardID = ?
    """, (card_id,))

    attacks = cursor.fetchall()

    if not attacks:
        print("\nThis card has no attacks to edit.")
        pause_screen()
        return

    print("\nExisting Attacks:")
    print_as_table(cursor, attacks)

    while True:
        attack_id = input("\nEnter Attack ID to edit (or type 'back'): ").strip()

        if attack_id.lower() == "back":
            return

        cursor.execute("""
            SELECT AttackID, AttackName, Damage, EnergyCost, Effect
            FROM AttackDetails
            WHERE AttackID = ?
            AND CardID = ?
        """, (attack_id, card_id))

        attack = cursor.fetchone()

        if attack:
            break

        print("Invalid Attack ID.")

    # Attack Name
    new_name = input(
        f"Update Attack Name [{attack[1]}]: "
    ).strip()

    if new_name == "":
        new_name = attack[1]

    # Damage
    new_damage = input(
        f"Update Damage [{attack[2]}]: "
    ).strip()

    if new_damage == "":
        new_damage = attack[2]

    # Energy Cost
    new_energy = input(
        f"Update Energy Cost [{attack[3]}]: "
    ).strip()

    if new_energy == "":
        new_energy = attack[3]

    # Effect
    new_effect = input(
        f"Update Effect [{attack[4]}]: "
    ).strip()

    if new_effect == "":
        new_effect = attack[4]

    cursor.execute("""
        UPDATE AttackDetails
        SET AttackName = ?,
            Damage = ?,
            EnergyCost = ?,
            Effect = ?
        WHERE AttackID = ?
    """, (
        new_name,
        new_damage,
        new_energy,
        new_effect,
        attack_id
    ))

    conn.commit()

    print(f"\nAttack {attack_id} updated successfully!")
    pause_screen()



def edit_ability(card_id):

    cursor.execute("""
        SELECT AbilityID, AbilityName, AbilityType, Description
        FROM CardAbility
        WHERE CardID = ?
    """, (card_id,))

    abilities = cursor.fetchall()

    if not abilities:
        print("\nThis card has no abilities to edit.")
        pause_screen()
        return

    print("\nExisting Abilities:")
    print_as_table(cursor, abilities)

    while True:
        ability_id = input("\nEnter Ability ID to edit (or type 'back'): ").strip()

        if ability_id.lower() == "back":
            return

        cursor.execute("""
            SELECT AbilityID, AbilityName, AbilityType, Description
            FROM CardAbility
            WHERE AbilityID = ?
            AND CardID = ?
        """, (ability_id, card_id))

        ability = cursor.fetchone()

        if ability:
            break

        print("Invalid Ability ID.")

    # Ability Name
    new_name = input(
        f"Update Ability Name [{ability[1]}]: "
    ).strip()

    if new_name == "":
        new_name = ability[1]

    # Ability Type
    new_type = input(
        f"Update Ability Type [{ability[2]}]: "
    ).strip()

    if new_type == "":
        new_type = ability[2]

    # Description
    new_description = input(
        f"Update Description [{ability[3]}]: "
    ).strip()

    if new_description == "":
        new_description = ability[3]

    cursor.execute("""
        UPDATE CardAbility
        SET AbilityName = ?,
            AbilityType = ?,
            Description = ?
        WHERE AbilityID = ?
    """, (
        new_name,
        new_type,
        new_description,
        ability_id
    ))

    conn.commit()

    print(f"\nAbility {ability_id} updated successfully!")
    pause_screen()



def add_attack(card_id):

    cursor.execute("""
        SELECT AttackID
        FROM AttackDetails
        WHERE CardID = ?
    """, (card_id,))

    attacks = cursor.fetchall()

    if not attacks:
        next_number = 1
    else:
        numbers = []

        for attack in attacks:
            attack_id = attack[0]
            number = int(attack_id.split("-AT")[1])
            numbers.append(number)

        next_number = max(numbers) + 1

    attack_id = f"{card_id}-AT{next_number}"

    while True:
        attack_name = input("Attack Name: ").strip()

        if attack_name != "":
            break

        print("Attack Name cannot be blank.")

    while True:
        damage = input("Damage: ").strip()

        if damage != "":
            break

        print("Damage cannot be blank.")

    while True:
        energy_cost = input("Energy Cost: ").strip()

        if energy_cost != "":
            break

        print("Energy Cost cannot be blank.")

    effect = input("Effect: ").strip()

    cursor.execute("""
        INSERT INTO AttackDetails
        (AttackID, CardID, AttackName, Damage, EnergyCost, Effect)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        attack_id,
        card_id,
        attack_name,
        damage,
        energy_cost,
        effect
    ))

    conn.commit()

    print(f"\nAttack {attack_id} added successfully!")



def add_ability(card_id):

    cursor.execute("""
        SELECT AbilityID
        FROM CardAbility
        WHERE CardID = ?
    """, (card_id,))

    abilities = cursor.fetchall()

    if not abilities:
        next_number = 1
    else:
        numbers = []

        for ability in abilities:
            ability_id = ability[0]
            number = int(ability_id.split("-AB")[1])
            numbers.append(number)

        next_number = max(numbers) + 1

    ability_id = f"{card_id}-AB{next_number}"

    while True:
        ability_name = input("Ability Name: ").strip()

        if ability_name != "":
            break

        print("Ability Name cannot be blank.")

    ability_type = input("Ability Type: ").strip()
    description = input("Description: ").strip()

    cursor.execute("""
        INSERT INTO CardAbility
        (AbilityID, CardID, AbilityName, AbilityType, Description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        ability_id,
        card_id,
        ability_name,
        ability_type,
        description
    ))

    conn.commit()

    print(f"\nAbility {ability_id} added successfully!")



def create_card():
    while True:
        clear_screen()
        print("-" * 60)
        print("                     Create Card")
        print("-" * 60)

        category = input("""
[1] Create Creature Card
[2] Create Trainer Card
[3] Create Energy Card
[0] Back

Select an option: """).strip()

        if category == "0":
            break

        elif category not in ["1", "2", "3"]:
            print("Invalid option.")
            pause_screen()
            continue

        type_map = {
            "1": "Creature Card",
            "2": "Trainer Card",
            "3": "Energy Card"
        }

        card_type = type_map[category]

        # ==========================================
        # GENERATE CARD ID
        # ==========================================

        cursor.execute("SELECT MAX(CardID) FROM Card;")
        result = cursor.fetchone()

        if result[0] is None:
            next_number = 1
        else:
            next_number = int(result[0][1:]) + 1

        card_id = f"C{next_number:03d}"

        # ==========================================
        # CARD NAME
        # ==========================================

        while True:
            card_name = input("Card Name: ").strip()

            if card_name == "":
                print("Card Name cannot be blank.")
                continue

            cursor.execute("""
                SELECT CardID
                FROM Card
                WHERE CardName = ?
            """, (card_name,))

            if cursor.fetchone():
                print("A card with that name already exists.")
            else:
                break

        # ==========================================
        # SET ID
        # ==========================================

        while True:
            set_id = input("Set ID: ").strip()

            cursor.execute("""
                SELECT SetID
                FROM CardSet
                WHERE SetID = ?
            """, (set_id,))

            if cursor.fetchone():
                break

            print("Invalid Set ID.")

        # ==========================================
        # CARD NUMBER
        # ==========================================

        while True:
            card_number = input("Card Number: ").strip()

            if card_number == "":
                print("Card Number cannot be blank.")
                continue

            cursor.execute("""
                SELECT CardID
                FROM Card
                WHERE CardNumber = ?
            """, (card_number,))

            if cursor.fetchone():
                print("A card with that number already exists.")
            else:
                break

        # ==========================================
        # RARITY
        # ==========================================

        while True:
            rarity = input("Rarity: ").strip()

            if rarity != "":
                break

            print("Rarity cannot be blank.")

        # ==========================================
        # INSERT CARD
        # ==========================================

        cursor.execute("""
            INSERT INTO Card
            (CardID, SetID, CardName, CardType, CardNumber, Rarity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            card_id,
            set_id,
            card_name,
            card_type,
            card_number,
            rarity
        ))

        # ==========================================
        # CREATURE CARD
        # ==========================================

        if category == "1":

            evolution = input("Evolution Stage: ").strip()

            while True:
                hp = input("HP: ").strip()

                if hp.isdigit() and int(hp) > 0:
                    hp = int(hp)
                    break

                print("HP must be a positive number.")

            element = input("Element Type: ").strip()

            while True:
                retreat_cost = input("Retreat Cost: ").strip()

                if retreat_cost.isdigit() and int(retreat_cost) >= 0:
                    retreat_cost = int(retreat_cost)
                    break

                print("Retreat Cost must be a number.")

            weakness = input("Weakness: ").strip()
            resistance = input("Resistance: ").strip()

            cursor.execute("""
                INSERT INTO CreatureCard
                (CardID, EvolutionStage, HP, ElementType,
                 RetreatCost, Weakness, Resistance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                card_id,
                evolution,
                hp,
                element,
                retreat_cost,
                weakness,
                resistance
            ))

        # ==========================================
        # TRAINER CARD
        # ==========================================

        elif category == "2":

            subtype = input("Subtype: ").strip()
            rules = input("Rules: ").strip()

            cursor.execute("""
                INSERT INTO TrainerCard
                (CardID, Subtype, Rules)
                VALUES (?, ?, ?)
            """, (
                card_id,
                subtype,
                rules
            ))

        # ==========================================
        # ENERGY CARD
        # ==========================================

        elif category == "3":

            element = input("Element Type: ").strip()
            energy_type = input("Energy Type: ").strip()
            special_effects = input("Special Effects: ").strip()

            cursor.execute("""
                INSERT INTO EnergyCard
                (CardID, ElementType, EnergyType, SpecialEffects)
                VALUES (?, ?, ?, ?)
            """, (
                card_id,
                element,
                energy_type,
                special_effects
            ))

        conn.commit()

        print(f"\nCard {card_id} created successfully!")

        # ==========================================
        # ADD ATTACKS / ABILITIES
        # ==========================================

        if category == "1":

            while True:
                add_attack_choice = input("\nWould you like to add an attack? (y/n): ").strip().lower()

                if add_attack_choice == "y":
                    add_attack(card_id)

                    while True:
                        another_attack = input("\nWould you like to add another attack? (y/n): ").strip().lower()

                        if another_attack == "y":
                            add_attack(card_id)
                        elif another_attack == "n":
                            break
                        else:
                            print("Please enter y or n.")

                    break

                elif add_attack_choice == "n":
                    break

                else:
                    print("Please enter y or n.")

            while True:
                add_ability_choice = input("\nWould you like to add an ability? (y/n): ").strip().lower()

                if add_ability_choice == "y":
                    add_ability(card_id)

                    while True:
                        another_ability = input("\nWould you like to add another ability? (y/n): ").strip().lower()

                        if another_ability == "y":
                            add_ability(card_id)
                        elif another_ability == "n":
                            break
                        else:
                            print("Please enter y or n.")

                    break

                elif add_ability_choice == "n":
                    break

                else:
                    print("Please enter y or n.")

        pause_screen()
        break



def delete_card():
    """
    Safely removes a card entry by wiping all child foreign key 
    dependencies before deleting the master card record.
    """
    print("\n------------------- Delete Card -------------------")
    card_id = input("Enter the Card ID you wish to delete: ").strip()

    # Step 1: Verify the card actually exists in the database
    cursor.execute("SELECT CardName, CardType FROM Card WHERE CardID = ?", (card_id,))
    card = cursor.fetchone()
    
    if not card:
        print(f"Error: No card found with ID '{card_id}'.")
        return

    card_name, card_type = card[2], card[3]

    # Step 2: Gather stats from child tables to alert the administrator
    cursor.execute("SELECT SUM(Quantity) FROM PlayerCollection WHERE CardID = ?", (card_id,))
    count_collection = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(Quantity) FROM CardInDeck WHERE CardID = ?", (card_id,))
    count_decks = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM TradeCard WHERE CardID = ?", (card_id,))
    count_trades = cursor.fetchone()[0] or 0

    # Step 3: Present confirmation prompt if data is attached
    if count_collection > 0 or count_decks > 0 or count_trades > 0:
        print(f"\n[⚠️ CRITICAL SYSTEM WARNING]")
        print(f"Card Name: '{card_name}' (Type: {card_type})")
        print(f"• Linked in Player Inventories : {count_collection} copies")
        print(f"• Attached to active Player Decks : {count_decks} copies")
        print(f"• Flagged in open/past Trade Offers : {count_trades} records")
        
        confirm = input("\nThis action is irreversible. Wipe all dependencies and proceed? (yes/no): ").lower().strip()
        if confirm != "yes":
            print("Deletion aborted. No changes were made to the database.")
            return

    try:
        # Step 4: Delete from cross-reference / transaction junction tables
        cursor.execute("DELETE FROM CardInDeck WHERE CardID = ?", (card_id,))
        cursor.execute("DELETE FROM PlayerCollection WHERE CardID = ?", (card_id,))
        cursor.execute("DELETE FROM TradeCard WHERE CardID = ?", (card_id,))

        # Step 5: Delete from component / attribute sub-tables
        cursor.execute("DELETE FROM CardAbility WHERE CardID = ?", (card_id,))
        cursor.execute("DELETE FROM AttackDetails WHERE CardID = ?", (card_id,))

        # Step 6: Delete from card identity sub-type tables
        cursor.execute("DELETE FROM CreatureCard WHERE CardID = ?", (card_id,))
        cursor.execute("DELETE FROM TrainerCard WHERE CardID = ?", (card_id,))
        cursor.execute("DELETE FROM EnergyCard WHERE CardID = ?", (card_id,))

        # Step 7: Delete the root master record from the main Card table
        cursor.execute("DELETE FROM Card WHERE CardID = ?", (card_id,))

        # Commit everything to the database in a single transaction blocks
        conn.commit()
        print(f"\nSuccess! '{card_name}' (ID: {card_id}) and all references completely removed.")

    except sqlite3.Error as error:
        conn.rollback()
        print(f"\n[DATABASE ERROR] Deletion failed. Transaction rolled back safely.")
        print(f"Reason: {error}")



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
    clear_screen()
    while True:
        print("-" * 90)
        print("                            View Staff Details")
        print("-" * 90)
        print("  [1] View all Staff Details             [3] search for specific staff member by id or username")
        print("  [2] Search for staff members by role   [0] Back to Main Menu ")
        choice = input("").strip()

        if choice == "0":
            break

        elif choice == "1":
            cursor.execute("SELECT * FROM Staff ORDER BY Position ASC, StaffID ASC")
            staff = cursor.fetchall()
            print_as_table(cursor, staff)
            pause_screen()

        elif choice == "2":
            while True:
                role = input("Enter Staff role (or type 'back'): ").strip()
                if role == "back":
                    break
                elif role in ['Staff', 'Moderator', 'Administrator']:
                    cursor.execute("SELECT * FROM Staff WHERE Position = ? ORDER BY FirstName", (role,))
                    staff = cursor.fetchall()
                    if staff:
                        print_as_table(cursor, staff)
                        pause_screen()
                        break
                    else:
                        print("No staff members found with that role. Please try again.")
                        pause_screen()
                else:
                    print("invalid role entered.")

        elif choice == "3":
            while True:
                search = input("Enter Staff ID or username (or type 'back'): ").strip().lower()
                if role == "back":
                    break

                elif search == 'id':
                    while True:
                        staffid = input("Enter Staff ID (or back):").strip().upper()
                        if staffid == "BACK":
                            break
                        cursor.execute("SELECT * FROM Staff WHERE StaffID = ?", (staffid,))
                        staff = cursor.one()
                        if staff:
                            print_as_table(cursor, staff)
                            pause_screen()
                            break
                        else:
                            print("No staff member found with that ID. Please try again.")
                            pause_screen()
                elif search == 'username':
                    while True:
                        staffuser = input("Enter Staff Username (or back):").strip().lower()
                        if staffid == "back":
                            break
                        cursor.execute("SELECT * FROM Staff WHERE Username = ?", (staffuser,))
                        staff = cursor.one()
                        if staff:
                            print_as_table(cursor, staff)
                            pause_screen()
                            break
                        else:
                            print("No staff member found with that username. Please try again.")
                            pause_screen()
                else:
                    print("invalid role entered.")
                    pause_screen()



def edit_staff_details():
    clear_screen()

    while True:
        print("-" * 60)
        print("                  Edit Staff Details")
        print("-" * 60)

        search = input("(type 'back' to go back)\nFind staff member to edit by ID or Username: ").strip().lower()

        if search == "back":
            break

        elif search == "id":
            while True:
                staff_id = input("Enter Staff ID (or type 'back'): ").strip().upper()

                if staff_id.lower() == "back":
                    break

                cursor.execute("SELECT * FROM Staff WHERE StaffID = ?", (staff_id,))
                staff = cursor.fetchone()

                if staff:
                    edit_staff_details_checks(staff, cursor)
                    break
                else:
                    print("\nNo staff member found with that ID. Please try again.")
                    pause_screen()

        elif search == "username":
            while True:
                username = input("Enter Staff Username (or type 'back'): ").strip()

                if username.lower() == "back":
                    break

                cursor.execute("SELECT * FROM Staff WHERE Username = ?", (username,))
                staff = cursor.fetchone()

                if staff:
                    edit_staff_details_checks(staff, cursor)
                    break
                else:
                    print("\nNo staff member found with that username. Please try again.")
                    pause_screen()

        else:
            print("\nInvalid search option. Please enter 'ID' or 'Username'.")
            pause_screen()

        clear_screen()



def edit_staff_details_checks(staff, cursor):
    print_as_table(cursor, staff)

    staffid = staff[0]

    print("\nPlease enter the staff data you wish to change.")
    print("If you do not wish to change anything, just press Enter.")

    while True:
        new_firstname = input("Update First Name: ").strip()

        if new_firstname == "":
            new_firstname = staff[1]
            break

    while True:
        new_lastname = input("Update Last Name: ").strip()

        if new_lastname == "":
            new_lastname = staff[2]
            break

    while True:
        new_username = input("Update Username: ").strip()

        if new_username == "":
            new_username = staff[3]
            break
        cursor.execute("""
            SELECT StaffID
            FROM Staff
            WHERE Username = ? AND StaffID != ?
        """, (new_username, staffid))

        if cursor.fetchone():
            print("This username already exists.")
        else:
            break

    while True:
        new_password = input("Update Password: ").strip()

        if new_password == "":
            new_password = staff[4]
            break
        if len(new_password) < 8:
            print("Password must be at least 8 characters long.")
            continue
        if not any(char.isupper() for char in new_password):
            print("Password must contain at least one uppercase letter.")
            continue
        if not any(char.islower() for char in new_password):
            print("Password must contain at least one lowercase letter.")
            continue
        if not any(not char.isalnum() for char in new_password):
            print("Password must contain at least one symbol (e.g., !, @, #, $, etc.).")
            continue
        break

    while True:
        new_email = input("Update Email: ").strip()

        if new_email == "":
            new_email = staff[5]
            break
        if "@" in new_email and "." in new_email:
            at_position = new_email.index("@")
            dot_position = new_email.rindex(".")

            if at_position > 0 and dot_position > at_position + 1 and dot_position < len(new_email) - 1:
                break
            else:
                print("\nPlease enter a valid email")
        else:
            print("E\nPlease enter a valid email")

    while True:
        new_phone = input("Update Phone Number: ").strip()
        if new_phone == "":
            new_phone = None
            break

        cleaned_number = new_phone.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")

        if 3 <= len(cleaned_number) <= 17 and cleaned_number.isdigit():
            break
        else:
            print("\nPlease enter a valid phone number:")

    while True:
        new_position = input("Update Position (Administrator/Moderator/Staff): ").strip()

        if new_position == "":
            new_position = staff[7]
            break

        if new_position in ["Administrator", "Moderator", "Staff"]:
            break
        else:
            print("Invalid position. Please enter Administrator, Moderator or Staff.")

    cursor.execute("""
        UPDATE Staff
        SET FirstName = ?,
            LastName = ?,
            Username = ?,
            Password = ?,
            Email = ?,
            PhoneNumber = ?,
            Position = ?
        WHERE StaffID = ?
    """, (
        new_firstname,
        new_lastname,
        new_username,
        new_password,
        new_email,
        new_phone,
        new_position,
        staffid
    ))

    conn.commit()

    print("\nStaff member updated successfully.")
    pause_screen()



def create_new_staff_member():
    clear_screen()
    print("-" * 60)
    print("                  Add New Staff Member")
    print("-" * 60)
    
    cursor.execute("SELECT MAX(StaffID) FROM Staff;")
    result = cursor.fetchone()

    if result[0] is None:
        next_number = 1
    else:
        next_number = int(result[0][1:]) + 1

    staff_id = f"S{next_number:03d}"

    print(f"Staff ID: {staff_id}")

    while True:
        firstname = input("Enter FirstName: ")

        if firstname == "":
            print("Name can not be blank:")
            pause_screen()
        else:
            break

    while True:
        lastname = input("Enter LastName: ")

        if lastname == "":
            print("Name can not be blank:")
            pause_screen()
        else:
            break

    while True:
        username = input("Enter Username: ")

        if username == "":
            print("Enter a valid username:")
            continue

        cursor.execute("SELECT Username FROM Staff WHERE Username = ?", (username,))
        not_unique = cursor.fetchone()

        if not_unique:
            print("This username already exists")
        else:
            break

    while True:
        password = input("Enter password: ").strip()

        if password == "":
            print("Enter a password:")
            pause_screen()
        elif len(password) < 8:
            print("Password must be at least 8 characters long.")
            pause_screen()
        elif not any(char.isupper() for char in password):
            print("Password must contain at least one uppercase letter.")
            pause_screen()
        elif not any(char.islower() for char in password):
            print("Password must contain at least one lowercase letter.")
            pause_screen()
        elif not any(not char.isalnum() for char in password):
            print("Password must contain at least one symbol (e.g., !, @, #, $, etc.).")
            pause_screen()
        else:
            break
    while True:
        number = input("Enter Phone Number: ").strip()

        if number == "":
            print("\nPhone number cannot be blank.")
            pause_screen()
            continue

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

    while True:
        position = input("Enter position: ")

        if position in ['Staff', 'Moderator', 'Administrator']:
            break
        else:
            print("Enter position from 'Staff', 'Moderator' or 'Administrator'")
            pause_screen()

    db_number = number

    cursor.execute(
        """
        INSERT INTO Staff (StaffID, FirstName, LastName, Username, Password, Email, PhoneNumber, Position)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (staff_id, firstname, lastname, username, password, email, db_number, position)
    )

    conn.commit()

    print(f"\nNew staff member '{username}' added successfully.")
    pause_screen()



def delete_staff_member():
    while True:
        clear_screen()
        print("-" * 60)
        print("                  Delete Staff Member")
        print("-" * 60)
        search = input("(type 'back' to go back)\nFind Staff member to delete by ID or Username: ").lower().strip()

        if search == "back":
            break

        elif search == "id":
            while True:
                id_input = input("Enter Staff ID (or type 'back'): ").strip().upper()
                if id_input.lower() == "back":
                    break
                
                cursor.execute("SELECT * FROM Staff WHERE StaffID = ?", (id_input,))
                staff = cursor.fetchone()

                if staff:
                    print_as_table(cursor, staff)
                    
                    # FIXED: Added a loop just for confirmation so typos don't break the record search
                    while True:
                        confirm = input("Are you sure you want to delete staff member? (yes/no): ").lower().strip()

                        if confirm == "yes":
                            cursor.execute("DELETE FROM TournamentStaff WHERE StaffID = ?", (id_input,))
                            cursor.execute("DELETE FROM Staff WHERE StaffID = ?", (id_input,))
                            conn.commit()

                            print(f"Staff member deleted successfully.")
                            pause_screen()
                            break

                        elif confirm == "no":
                            print("Deletion cancelled.")
                            pause_screen()
                            break

                        else:
                            print("\nPlease select from 'yes' or 'no'")
                    
                    # Breaks out of the id_input loop back to the main search selection screen
                    break

                else:
                    print("No staff member found. Please try again.")
                    pause_screen()

        elif search == "username":
            while True:
                username = input("Enter Staff username (or type 'back'): ").strip()
                if username.lower() == "back":
                    break
                
                cursor.execute("SELECT * FROM Staff WHERE Username = ?", (username,))
                staff = cursor.fetchone()

                if staff:
                    print_as_table(cursor, staff)
                    while True:
                        confirm = input("Are you sure you want to delete staff member? (yes/no): ").lower().strip()

                        if confirm == "yes":
                            cursor.execute("""
                                DELETE FROM TournamentStaff
                                WHERE staffid in (
                                    SELECT StaffID FROM Staff WHERE username = ?
                                );""", (username,))
                            cursor.execute("DELETE FROM Staff WHERE Username = ?", (username,))
                            conn.commit()

                            print(f"Staff member deleted successfully.")
                            pause_screen()
                            break

                        elif confirm == "no":
                            print("Deletion cancelled.")
                            pause_screen()
                            break

                        else:
                            print("\nPlease select from 'yes' or 'no'")
                    break

                else:
                    print("No staff member found. Please try again.")
                    pause_screen()
        else:
            print("Invalid search option. Please enter 'ID' or 'Username'.")
            pause_screen()

        clear_screen()


def generate_analytical_reports():
    while True:
        clear_screen()
        print("-" * 90)
        print("                           Generate Analytical Reports")
        print("-" * 90)
        print("  [1] Display the players with the largest card collections.")
        print("  [2] Display the most commonly owned card")
        print("  [3] Display cards ordered by rarity.")
        print("  [4] Calculate the maximum and minimum HP. ")
        print("  [5] Display the total number of players/cards/decks/tournaments/tournament registries")
        print("  [0] Back to main menu")
        choice = input("")
        if choice == "0":
            break
        elif choice == "1":
            clear_screen()
            print("-" * 90)
            print("Players With The Largest Collections")
            print("-" * 90)
            cursor.execute("""
                SELECT Player.PlayerID, Player.Username, SUM(PlayerCollection.Quantity) AS "Number of Cards"
                FROM Player 
                JOIN PlayerCollection ON PlayerCollection.PlayerID = Player.PlayerID
                GROUP BY Player.PlayerID
                ORDER BY "Number of Cards" DESC
                LIMIT 10;""")
            players = cursor.fetchall()
            if players:
                print_as_table(cursor, players)
                pause_screen()
            else:
                print("No players found")
                pause_screen()

        elif choice == "2":
            clear_screen()
            print("-" * 90)
            print("Most Commonly Owned Cards")
            print("-" * 90)
            cursor.execute("""
               SELECT *, SUM(PlayerCollection.Quantity) AS 'Total Owned'
                FROM Card 
                JOIN PlayerCollection ON PlayerCollection.CardID = Card.CardID
                GROUP BY Card.CardID
                ORDER BY "Total Owned" DESC
                LIMIT 10""")
            cards = cursor.fetchall()
            if cards:
                print_as_table(cursor, cards)
            else:
                print("No cards found")
                pause_screen()

            print("")
            print("-" * 90)
            print("Most Commonly Owned Creature Cards")
            print("-" * 90)
            cursor.execute("""
               SELECT *, SUM(PlayerCollection.Quantity) AS 'Total Owned'
                FROM Card 
                JOIN PlayerCollection ON PlayerCollection.CardID = Card.CardID
                WHERE Card.CardType = 'Creature Card'
                GROUP BY Card.CardID
                ORDER BY "Total Owned" DESC
                LIMIT 10""")
            cards = cursor.fetchall()
            if cards:
                print_as_table(cursor, cards)
            else:
                print("No cards found")
                pause_screen()

            print("")
            print("-" * 90)
            print("Most Commonly Owned Trainer Cards")
            print("-" * 90)
            cursor.execute("""
               SELECT *, SUM(PlayerCollection.Quantity) AS 'Total Owned'
                FROM Card 
                JOIN PlayerCollection ON PlayerCollection.CardID = Card.CardID
                WHERE Card.CardType = 'Trainer Card'
                GROUP BY Card.CardID
                ORDER BY "Total Owned" DESC
                LIMIT 10""")
            cards = cursor.fetchall()
            if cards:
                print_as_table(cursor, cards)
            else:
                print("No cards found")
                pause_screen()

            print("")
            print("-" * 90)
            print("Most Commonly Owned Energy Cards")
            print("-" * 90)
            cursor.execute("""
               SELECT *, SUM(PlayerCollection.Quantity) AS 'Total Owned'
                FROM Card 
                JOIN PlayerCollection ON PlayerCollection.CardID = Card.CardID
                WHERE Card.CardType = 'Energy Card'
                GROUP BY Card.CardID
                ORDER BY "Total Owned" DESC
                LIMIT 10""")
            cards = cursor.fetchall()
            if cards:
                print_as_table(cursor, cards)
                pause_screen()
            else:
                print("No cards found")
                pause_screen()

        elif choice == "3":
            clear_screen()
            print("-" * 90)
            print("Cards Ordered By Rarity")
            print("-" * 90)
            cursor.execute("""
            SELECT * FROM Card
            ORDER BY
                CASE Card.Rarity
                    WHEN 'Special Illustration Rare' THEN 1
                    WHEN 'Illustration Rare'         THEN 2
                    WHEN 'Hyper Rare'                THEN 3
                    WHEN 'Ultra Rare'                THEN 4
                    WHEN 'ACE SPEC Rare'             THEN 5
                    WHEN 'Double Rare'               THEN 6
                    WHEN 'Rare Holo'                 THEN 7
                    WHEN 'Rare'                      THEN 8
                    WHEN 'Uncommon'                  THEN 9
                    WHEN 'Common'                    THEN 10
                    ELSE 11
                END ASC""")
            cards = cursor.fetchall()
            if cards:
                print_as_table(cursor, cards)
                pause_screen()
            else:
                print("no cards found")
                pause_screen()

        elif choice == "4":
            clear_screen()
            cursor.execute("""
                SELECT Card.CardID, Card.CardName, Card.CardNumber, Card.Rarity, CreatureCard.HP
                FROM Card
                JOIN CreatureCard ON Card.CardID = CreatureCard.CardID
                ORDER BY HP DESC
                LIMIT 1;
            """)
            highesthp = cursor.fetchone()
            cursor.execute("""
                SELECT Card.CardID, Card.CardName, Card.CardNumber, Card.Rarity, CreatureCard.HP
                FROM Card
                JOIN CreatureCard ON Card.CardID = CreatureCard.CardID
                ORDER BY HP ASC
                LIMIT 1;
            """)
            lowesthp = cursor.fetchone()
            if highesthp and lowesthp:
                print("Card with the Highest HP:")
                print_as_table(cursor, highesthp)
                print("\nCard with the Lowest HP:")
                print_as_table(cursor, lowesthp)
                pause_screen()
            else:
                print("no cards found")
                pause_screen()

        elif choice == "5":
            clear_screen()
            cursor.execute("SELECT COUNT(PlayerID) FROM Players")
            players = cursor.fetchone() 
            cursor.execute("SELECT COUNT(CardID) FROM Card")
            cards = cursor.fetchone()  
            cursor.execute("SELECT COUNT(DeckID) FROM Deck")
            decks = cursor.fetchone()   
            cursor.execute("SELECT COUNT(tournamentID) FROM tournament")
            tournaments = cursor.fetchone()   
            cursor.execute("SELECT COUNT(PlayerID) FROM RegistrationList")
            registerations = cursor.fetchone() 
            cursor.execute("SELECT COUNT(MatchesID) FROM Matches WHERE MatchStatus = 'Finished'")
            matches = cursor.fetchone() 

            stat_template = "  {:<25} : {}"

            print("-" * 55)
            print(stat_template.format("Total PLayers", players[0]))
            print(stat_template.format("Total Cards", cards[0]))
            print(stat_template.format("Total Decks", decks[0]))
            print(stat_template.format("Total Tournaments", tournaments[0]))
            print(stat_template.format("Total Tournament Registrations", registrations[0]))
            print(stat_template.format("Total Matches Played", player_totalmatches[0]))
            print("-" * 55)
            pause_screen()

        else:
            print("Invalid option selected")
            pause_screen()



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
                        if user_position in ['Moderator', 'Administrator']:
                            delete_player()
                        else:
                            continue
                    else:
                        continue
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
                        if user_position in ['Moderator', 'Administrator']:
                            register_remove_players()
                        else: 
                            continue
                    elif manage_tournaments_option == "4":
                        if user_position in ['Moderator', 'Administrator']:
                            create_new_tournament()
                        else: 
                            continue
                    elif manage_tournaments_option == "5":
                        if user_position in ['Moderator', 'Administrator']:
                            cancel_tournament()
                        else: 
                            continue
                    else: 
                        continue
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
                        if user_position in ['Moderator', 'Administrator']:
                            create_new_match()
                        else: 
                            continue
                    elif manage_matches_option == "4":
                        if user_position in ['Moderator', 'Administrator']:
                            delete_match()
                        else: 
                            continue
                    else: 
                        continue
            elif menu_option == "4" and user_position in ['Moderator', 'Administrator']:
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
                        continue
            elif menu_option == "5" and user_position in ['Moderator', 'Administrator']:
                while True:
                    manage_decks_option = manage_decks()
                    if manage_decks_option == "0":
                        break
                    elif manage_decks_option == "1":
                        view_deck_cards()
                    elif manage_decks_option == "2":
                        view_all_decks_containing_specific_card()
                    else: 
                        continue
            elif menu_option == "6" and user_position == 'Administrator':
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
                        continue
            elif menu_option == "7" and user_position == 'Administrator':
                generate_analytical_reports()
            else:
                continue



main()
