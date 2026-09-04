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
                    print("No player found with that ID. Please try again.\n")

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
                    print("No player found with that username. Please try again.\n")

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
                    print("No player found with that email. Please try again.\n")
        else:
            continue
        clear_screen()



def edit_account_details():
    while True:
        clear_screen()
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
                    print("No player found with that ID. Please try again.\n")

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
                    print("No player found with that username. Please try again.\n")
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
        if 3 <= len(cleaned_number) <= 17 and cleaned_number.isdigit():
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

    cursor.execute("""
        UPDATE Player 
        SET Username = ?, DateOfBirth = ?, PhoneNumber = ?, Email = ? 
        WHERE PlayerID = ?
        """,(new_username, new_dob, db_number, new_email, playerid))
    conn.commit()
    print("Player details updated successfully.")
    pause_screen()



def view_player_stats():
    while True:
        clear_screen()
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
                    print("No player found with that ID. Please try again.\n")

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
                    print("No player found with that username. Please try again.\n")
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
        username = input("(type 'back' at any time to cancel\nEnter Username: ").strip()
        if username == "":
            print("Enter a valid username:")
            continue
        elif username.lower() == 'back':
            break

        cursor.execute("SELECT Username FROM Player WHERE Username = ?", (username,))
        not_unique = cursor.fetchone()
        if not_unique:
            print("This username already exists")
        else:
            break

    while True:
        dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
        if dob == "":
            print("Enter a valid date of birth:")
            continue
        elif dob == "back":
            break

        try:
            dob = datetime.strptime(dob, "%Y-%m-%d").date()
            if dob > date.today():
                print("Date of birth cannot be in the future.")
            else:
                break
        except ValueError:
            print("Invalid date. Please enter the date in YYYY-MM-DD format.")
            
    while True:
        number = input("Enter Phone Number: ").strip()
        if number == "":
            number = None
            break
        elif number == "back":
            break

        cleaned_number = number.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        if 3 <= len(cleaned_number) <= 17 and cleaned_number.isdigit():
            break
        else:
            print("\nPlease enter a valid phone number:")

    while True:
        email = input("Enter Email: ").strip()
        if email == "":
            print("\nPlease enter a valid email:")
            continue
        elif email == "back":
            break

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
    cursor.execute("""
        INSERT INTO Player (PlayerID, Username, DateOfBirth, PhoneNumber, Email, DateJoined) 
        VALUES (?, ?, ?, ?, ?, ?)""", 
        (player_id, username, dob, db_number, email, date_joined))
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
                        cursor.execute("DELETE FROM Player WHERE PlayerID = ?", (player[0],))

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
                    print("No player found with that ID. Please try again.\n")

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
                        cursor.execute("DELETE FROM Player WHERE PlayerID = ?", (player[0],))

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
                    print("No player found with that username. Please try again.\n")
        else:
            continue
        clear_screen()



def manage_tournaments():
    if user_position in ["Administrator", "Moderator"]:
        clear_screen()
        print("-" * 75)
        print("                           Manage Tournaments")
        print("-" * 75)
        print("  [1] View Tournament Details                 [5] Create New Tournament")
        print("  [2] Register/Remove player from Tournament  [6] Delete Tournament")
        print("  [3] View Venues                             [0] Back to Main Menu")
        print("  [4] Edit Tournament Details")
        print("")
        return input("\nSelect an option: ").strip()
    elif user_position == "Staff":
        clear_screen()
        print("-" * 50)
        print("              Manage Tournaments")
        print("-" * 50)
        print("  [1] View Tournament Details")
        print("  [2] Register/Remove player from Tournament")
        print("  [3] View Venues")
        print("  [0] Back to Main Menu")
        print("")
        return input("\nSelect an option: ").strip()



def view_tournament_details():
    while True:
        clear_screen()
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
                            print("No tournament found with that ID. Please try again.\n")
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
                            print("No tournament found with that name. Please try again.\n")
                else:
                    continue
        else:
            continue
        clear_screen()



def view_venues():
    while True:
        clear_screen()
        cursor.execute("SELECT * FROM Venue")
        venues = cursor.fetchall()
        print_as_table(cursor, venues)
        choice = input("Click enter to go back")
        if choice == "":
            break


def edit_tournament_details():
    while True:
        clear_screen()
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
                    # Pass conn along with tournament and cursor
                    edit_tournament_details_checks(tournament, cursor, conn)
                    break
                else:
                    print("No Tournament found with that ID. Please try again.\n")

        elif search == "name":
            while True:
                name_input = input("Enter Tournament Name (or type 'back'): ").strip()
                if name_input.lower() == "back":
                    break
                cursor.execute("SELECT * FROM Tournament WHERE TournamentName = ?",(name_input,))
                tournament = cursor.fetchone()

                if tournament:
                    # Pass conn along with tournament and cursor
                    edit_tournament_details_checks(tournament, cursor, conn)
                    break
                else:
                    print("No Tournament found with that name. Please try again.\n")
        else:
            continue
        clear_screen()


def edit_tournament_details_checks(tournament, cursor, conn): 
    print_as_table(cursor, tournament)
    tournamentid = tournament[0]
    print("Please enter the tournament data you wish to change. If you do not wish to change anything in the specific column, just click enter.")

    #Update Tournament Name
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

    #Update Start Date
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

    #Update Venue ID
    print("\n--- Available Venues ---")
    cursor.execute("SELECT VenueID, VenueName, VenueCity, VenueCountry FROM Venue")
    venues = cursor.fetchall()
    for v in venues:
        print(f"ID: {v[0]} | {v[1]} ({v[2]}, {v[3]})")
    print("------------------------\n")

    while True:
        new_venue_id = input("Update tournament Venue ID: ").strip()
        if new_venue_id == "":
            new_venue_id = tournament[3] 
            break

        #Check if the input is a valid number
        if not new_venue_id.isdigit():
            print("Invalid input. Please enter a numerical Venue ID.")
            continue

        new_venue_id = int(new_venue_id)

        #Check if the Venue ID actually exists 
        cursor.execute("SELECT VenueID FROM Venue WHERE VenueID = ?", (new_venue_id,))
        if cursor.fetchone() is None:
            print(f"Error: Venue ID {new_venue_id} does not exist. Please choose a valid ID.")
            continue
        
        break

    #Update Status
    while True:
        new_status = input("Update status (Upcoming, Ongoing, Finished): ").strip()
        if new_status == "":
            new_status = tournament[4]
            break
        elif new_status in ['Upcoming', 'Ongoing', 'Finished']:
            break
        else:
            print("Invalid status. Please enter Upcoming, Ongoing, or Finished.")

    #Execute Update Statement
    cursor.execute("""
        UPDATE Tournament
        SET TournamentName = ?, EventDate = ?, VenueID = ?, EventStatus = ?
        WHERE TournamentID = ?""",
        (new_tournamentname, new_date, new_venue_id, new_status, tournamentid))

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
            while True:
                clear_screen()
                print("-" * 60)
                print("                  Register New Player")
                print("-" * 60)

                tournament_id = input("Enter Tournament ID: ").strip().upper()
                if tournament_id == "":
                    continue

                cursor.execute("SELECT 1 FROM Tournament WHERE TournamentID = ?",(tournament_id,))
                if not cursor.fetchone():
                    print("\nError: Tournament ID does not exist.")
                    pause_screen()
                    continue

                player_id = input("Enter Player ID: ").strip().upper()
                if player_id == "":
                    print("\nEnter a valid Player ID.")
                    pause_screen()
                    continue

                cursor.execute("SELECT 1 FROM Player WHERE PlayerID = ?",(player_id,))
                if not cursor.fetchone():
                    print("\nError: Player ID does not exist.")
                    pause_screen()
                    continue

                cursor.execute("SELECT 1 FROM RegistrationList WHERE TournamentID = ? AND PlayerID = ?",(tournament_id, player_id))
                if cursor.fetchone():
                    print("\nError: This player is already registered for this tournament.")
                    pause_screen()
                    continue

                cursor.execute("INSERT INTO RegistrationList (TournamentID, PlayerID) VALUES (?, ?)",(tournament_id, player_id))

                conn.commit()
                print("\nPlayer successfully added.")
                pause_screen()

        elif choice == "2":
            while True:
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

                cursor.execute("SELECT 1 FROM RegistrationList WHERE TournamentID = ? AND PlayerID = ?",(tournament_id, player_id))
                if not cursor.fetchone():
                    print("\nError: No such registration found.")
                    pause_screen()
                    continue

                # Check whether the player is already involved in a match
                cursor.execute("SELECT 1 FROM Matches WHERE TournamentID = ? AND (Player1 = ? OR Player2 = ?)",(tournament_id, player_id, player_id))
                if cursor.fetchone():
                    print("\nError: This player is involved in a match and cannot be removed.")
                    pause_screen()
                    continue

                cursor.execute("DELETE FROM RegistrationList WHERE TournamentID = ? AND PlayerID = ?",(tournament_id, player_id))

                conn.commit()
                print("\nPlayer successfully removed from tournament.")
                pause_screen()
        else:
            continue



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
    
        #Tournament name
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

        #Event date
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

        #Venue ID Selection and Verification
        print("\n--- Available Venues ---")
        cursor.execute("SELECT VenueID, VenueName, VenueCity, VenueCountry FROM Venue")
        venues = cursor.fetchall()
        for v in venues:
            print(f"ID: {v[0]} | {v[1]} ({v[2]}, {v[3]})")
        print("------------------------\n")

        while True:
            venue_input = input("Enter Venue ID: ").strip()

            if venue_input == "":
                print("Venue ID cannot be empty.")
                continue

            if not venue_input.isdigit():
                print("Invalid input. Please enter a numerical Venue ID.")
                continue

            venue_id = int(venue_input)

            #Check if the Venue ID actually exists in the Venue table
            cursor.execute("SELECT VenueID FROM Venue WHERE VenueID = ?", (venue_id,))
            if cursor.fetchone() is None:
                print(f"Error: Venue ID {venue_id} does not exist. Please choose a valid ID.")
                continue

            break

        #Determine event status
        if eventdate == date.today():
            eventstatus = "Ongoing"
        else:
            eventstatus = "Upcoming"

        #Database Insert Query 
        cursor.execute("""
            INSERT INTO Tournament 
            (TournamentID, TournamentName, EventDate, VenueID, EventStatus) 
            VALUES (?, ?, ?, ?, ?)
            """,(tournament_id, name, eventdate, venue_id, eventstatus))

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

                    #Don't allow finished tournaments to be cancelled
                    if tournament[4] == "Finished":
                        print("Finished tournaments cannot be cancelled.")
                        pause_screen()
                        break

                    confirm = input(
                        f"Are you sure you want to cancel tournament "
                        f"'{tournament[1]}'? (yes/no): "
                    ).lower().strip()

                    if confirm == "yes":

                        #Delete other fields to prevent foreign key integrity errors
                        cursor.execute("DELETE FROM Matches WHERE TournamentID = ?",(tournament[0],))
                        cursor.execute("DELETE FROM RegistrationList WHERE TournamentID = ?",(tournament[0],))
                        cursor.execute("DELETE FROM TournamentStaff WHERE TournamentID = ?",(tournament[0],))
                        cursor.execute("DELETE FROM Tournament WHERE TournamentID = ?",(tournament[0],))
                        conn.commit()

                        print(f"Tournament '{tournament[1]}' " f"cancelled successfully.")
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
                name = input("Enter Tournament name (or type 'back'): ").strip()

                if name.lower() == "back":
                    break
                cursor.execute("SELECT * FROM Tournament WHERE TournamentName = ?",(name,))
                tournament = cursor.fetchone()

                if tournament:
                    print_as_table(cursor, tournament)

                    #Don't allow finished tournaments to be cancelled
                    if tournament[4] == "Finished":
                        print("Finished tournaments cannot be cancelled.")
                        pause_screen()
                        break

                    confirm = input(
                        f"Are you sure you want to cancel tournament "
                        f"'{tournament[1]}'? (yes/no): "
                    ).lower().strip()

                    if confirm == "yes":

                        #Delete other fields to prevent foreign key integrity errors
                        cursor.execute("DELETE FROM Matches WHERE TournamentID = ?",(tournament[0],))
                        cursor.execute("DELETE FROM RegistrationList WHERE TournamentID = ?",(tournament[0],))
                        cursor.execute("DELETE FROM TournamentStaff WHERE TournamentID = ?",(tournament[0],))
                        cursor.execute("DELETE FROM Tournament WHERE TournamentID = ?",(tournament[0],))
                        conn.commit()

                        print(f"Tournament '{tournament[1]}' "f"cancelled successfully.")
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
""").strip()

        if category == "0":
            break

        #View all matches in a tournament
        elif category == "1":
            clear_screen()
            print("-" * 60)
            print("             View all Matches in a Tournament")
            print("-" * 60)

            tournament_id = input("Enter Tournament ID: ").strip()

            #Check that the tournament exists first
            cursor.execute(
                "SELECT TournamentID FROM Tournament WHERE TournamentID = ?",
                (tournament_id,)
            )

            tournament_exists = cursor.fetchone()

            if not tournament_exists:
                print("\nNo tournament found with that ID.")
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
                JOIN Player AS Player1
                    ON Matches.Player1 = Player1.PlayerID
                JOIN Player AS Player2
                    ON Matches.Player2 = Player2.PlayerID
                LEFT JOIN Player AS WinnerPlayer
                    ON Matches.Winner = WinnerPlayer.PlayerID
                WHERE Matches.TournamentID = ?
            """, (tournament_id,))

            matches = cursor.fetchall()

            if matches:
                cursor.execute(
                    "SELECT COUNT(MatchesID) FROM Matches WHERE TournamentID = ?",
                    (tournament_id,)
                )

                num_matches = cursor.fetchone()

                print(f"Total number of matches: {num_matches[0]}")
                print_as_table(cursor, matches)
                pause_screen()

            else:
                print("\nNo matches found for that tournament.")
                pause_screen()

        # View specific match details
        elif category == "2":
            clear_screen()
            print("-" * 60)
            print("             View specific Match details")
            print("-" * 60)

            matches_id = input("Enter Match ID: ").strip().upper()

            cursor.execute("""
                SELECT 
                    Matches.MatchesID,
                    Player1.PlayerID || ' - ' || Player1.Username AS Player1,
                    Player2.PlayerID || ' - ' || Player2.Username AS Player2,
                    WinnerPlayer.PlayerID || ' - ' || WinnerPlayer.Username AS Winner,
                    Matches.MatchStatus,
                    Matches.Round
                FROM Matches
                JOIN Player AS Player1
                    ON Matches.Player1 = Player1.PlayerID
                JOIN Player AS Player2
                    ON Matches.Player2 = Player2.PlayerID
                LEFT JOIN Player AS WinnerPlayer
                    ON Matches.Winner = WinnerPlayer.PlayerID
                WHERE Matches.MatchesID = ?
            """, (matches_id,))

            matches = cursor.fetchone()

            if matches:
                print_as_table(cursor, matches)
                pause_screen()

            else:
                print("\nNo Match found with that ID.")
                pause_screen()

        # View a player's matches
        elif category == "3":
            clear_screen()
            print("-" * 60)
            print("         View Matches details of a Player")
            print("-" * 60)

            player_id = input("Enter Player ID: ").strip().upper()

            cursor.execute(
                "SELECT 1 FROM Player WHERE PlayerID = ?",
                (player_id,)
            )

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
                JOIN Player AS Player1
                    ON Matches.Player1 = Player1.PlayerID
                JOIN Player AS Player2
                    ON Matches.Player2 = Player2.PlayerID
                LEFT JOIN Player AS WinnerPlayer
                    ON Matches.Winner = WinnerPlayer.PlayerID
                WHERE Matches.Player1 = ? OR Matches.Player2 = ?
            """, (player_id, player_id))

            matches = cursor.fetchall()

            if matches:
                print_as_table(cursor, matches)
                pause_screen()

            else:
                print("\nNo matches found for that player ID.")
                pause_screen()

        else:
            continue

        clear_screen()


# Create new match: handles create new match for the system.
def create_new_match():
    while True:
        clear_screen()
        print("-" * 60)
        print("                  Create New Match")
        print("-" * 60)

        # Generate the next Match ID
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
        print("Match winner: None")

        # Select tournament
        while True:
            tournament_id = input(
                "Enter Tournament ID (or 'back' to go back): "
            ).strip().upper()

            if tournament_id == "BACK":
                return

            cursor.execute("""
                SELECT TournamentID, EventStatus
                FROM Tournament
                WHERE TournamentID = ?
            """, (tournament_id,))

            tourney = cursor.fetchone()

            if not tourney:
                print("No Tournament exists with that ID. Please try again.")
                pause_screen()
                continue

            # A finished tournament should not receive new matches
            if tourney[1] == "Finished":
                print("You cannot create a match for a finished tournament.")
                pause_screen()
                continue

            break

        # Select Player 1 and Player 2
        while True:
            player1 = input(
                "Enter the first player's ID: "
            ).strip().upper()

            cursor.execute(
                "SELECT * FROM Player WHERE PlayerID = ?",
                (player1,)
            )

            player1_exists = cursor.fetchone()

            if not player1_exists:
                print("\nInvalid player ID, please try again.")
                pause_screen()
                continue

            # Check Player 1 is registered for the tournament
            cursor.execute("""
                SELECT *
                FROM RegistrationList
                WHERE PlayerID = ? AND TournamentID = ?
            """, (player1, tournament_id))

            player1_registered = cursor.fetchone()

            if not player1_registered:
                print(
                    f"Player {player1} isn't registered for the tournament."
                )
                pause_screen()
                continue

            player2 = input(
                "Enter the second player's ID: "
            ).strip().upper()

            if player2 == player1:
                print("A player cannot play against themselves.")
                pause_screen()
                continue

            cursor.execute(
                "SELECT * FROM Player WHERE PlayerID = ?",
                (player2,)
            )

            player2_exists = cursor.fetchone()

            if not player2_exists:
                print("\nInvalid player ID, please try again.")
                pause_screen()
                continue

            # Check Player 2 is registered for the tournament
            cursor.execute("""
                SELECT *
                FROM RegistrationList
                WHERE PlayerID = ? AND TournamentID = ?
            """, (player2, tournament_id))

            player2_registered = cursor.fetchone()

            if not player2_registered:
                print(
                    f"Player {player2} isn't registered for the tournament."
                )
                pause_screen()
                continue

            break

        # Enter round number
        while True:
            round_input = input("Enter round number: ").strip()

            try:
                round_number = int(round_input)

                if round_number > 0:
                    break

                print("Round number must be greater than 0.")
                pause_screen()

            except ValueError:
                print("Enter a valid whole number.")
                pause_screen()

        # Prevent duplicate matches between the same players
        # in the same tournament and round.
        cursor.execute("""
            SELECT MatchesID
            FROM Matches
            WHERE TournamentID = ?
              AND Round = ?
              AND (
                    (Player1 = ? AND Player2 = ?)
                    OR
                    (Player1 = ? AND Player2 = ?)
                  )
        """, (
            tournament_id,
            round_number,
            player1,
            player2,
            player2,
            player1
        ))

        duplicate_match = cursor.fetchone()

        if duplicate_match:
            print(
                f"\nThese players already have a match "
                f"in Round {round_number} of this tournament."
            )
            pause_screen()
            continue

        # Insert the new match
        cursor.execute("""
            INSERT INTO Matches
                (MatchesID, TournamentID, Player1, Player2,
                 Winner, MatchStatus, Round)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            matches_id,
            tournament_id,
            player1,
            player2,
            match_winner,
            match_status,
            round_number
        ))

        conn.commit()

        print("\nMatch added successfully.")
        pause_screen()
        break


# Edit match details: handles edit match details for the system.
def edit_match_details():
    clear_screen()

    while True:
        print("-" * 60)
        print("                  Edit Match Details")
        print("-" * 60)

        id_input = input(
            "Enter Match ID (or type 'back'): "
        ).strip().upper()

        if id_input == "BACK":
            break

        cursor.execute(
            "SELECT * FROM Matches WHERE MatchesID = ?",
            (id_input,)
        )

        matches = cursor.fetchone()

        if matches:
            edit_match_details_checks(matches, cursor)
            break

        else:
            print("No Match found with that ID. Please try again.")
            pause_screen()

        clear_screen()


# Edit match details checks: handles edit match details checks for the system.
def edit_match_details_checks(matches, cursor):
    print_as_table(cursor, matches)

    matchid = matches[0]

    print("Please enter the match data you wish to change.")
    print("If you do not wish to change anything in a specific column, "
          "just click Enter.")
    print("Type 'back' at any time to cancel the edit.")

    while True:
        tournamentid = input("Enter Tournament ID: ").strip().upper()

        if tournamentid == "":
            tournamentid = matches[1]
            break

        elif tournamentid == "BACK":
            return

        cursor.execute("""
            SELECT TournamentID, EventStatus
            FROM Tournament
            WHERE TournamentID = ?
        """, (tournamentid,))

        tournament = cursor.fetchone()

        if not tournament:
            print("Enter a valid Tournament ID.")
            pause_screen()
            continue

        # Do not allow a match to be moved into a finished tournament.
        if tournament[1] == "Finished":
            print("A match cannot be assigned to a finished tournament.")
            pause_screen()
            continue

        break

    while True:
        player1 = input("Enter Player 1 ID: ").strip().upper()

        if player1 == "":
            player1 = matches[2]

        elif player1 == "BACK":
            return

        # Check that Player 1 exists
        cursor.execute("""
            SELECT PlayerID
            FROM Player
            WHERE PlayerID = ?
        """, (player1,))

        if not cursor.fetchone():
            print("Enter a valid Player 1 ID.")
            pause_screen()
            continue

        # Check Player 1 is registered for the selected tournament
        cursor.execute("""
            SELECT PlayerID
            FROM RegistrationList
            WHERE TournamentID = ? AND PlayerID = ?
        """, (tournamentid, player1))

        if cursor.fetchone():
            break

        print("Player 1 must be registered for this tournament.")
        pause_screen()

    # ---------------------------------------------------------
    # Player 2
    # ---------------------------------------------------------
    while True:
        player2 = input("Enter Player 2 ID: ").strip().upper()

        if player2 == "":
            player2 = matches[3]

        elif player2 == "BACK":
            return

        if player2 == player1:
            print("Player 1 and Player 2 cannot be the same player.")
            pause_screen()
            continue

        # Check that Player 2 exists
        cursor.execute("""
            SELECT PlayerID
            FROM Player
            WHERE PlayerID = ?
        """, (player2,))

        if not cursor.fetchone():
            print("Enter a valid Player 2 ID.")
            pause_screen()
            continue

        # Check Player 2 is registered for the selected tournament
        cursor.execute("""
            SELECT PlayerID
            FROM RegistrationList
            WHERE TournamentID = ? AND PlayerID = ?
        """, (tournamentid, player2))

        if cursor.fetchone():
            break

        print("Player 2 must be registered for this tournament.")
        pause_screen()

    while True:
        round_input = input("Enter round number: ").strip()

        if round_input == "":
            round_number = matches[6]
            break

        elif round_input.upper() == "BACK":
            return

        try:
            round_number = int(round_input)

            if round_number > 0:
                break

            print("Round number must be greater than 0.")
            pause_screen()

        except ValueError:
            print("Enter a valid whole number.")
            pause_screen()

    cursor.execute("""
        SELECT MatchesID
        FROM Matches
        WHERE TournamentID = ?
          AND Round = ?
          AND MatchesID != ?
          AND (
                (Player1 = ? AND Player2 = ?)
                OR
                (Player1 = ? AND Player2 = ?)
              )
    """, (
        tournamentid,
        round_number,
        matchid,
        player1,
        player2,
        player2,
        player1
    ))

    duplicate_match = cursor.fetchone()

    if duplicate_match:
        print(
            f"\nThese players already have a match "
            f"in Round {round_number} of this tournament."
        )
        pause_screen()
        return

    while True:
        winner = input("Enter winner (Player ID): ").strip().upper()

        if winner == "":
            winner = matches[4]

        elif winner == "BACK":
            return

        # If there is no winner yet, allow NULL.
        if winner == "":
            winner = None
            break

        # Winner must be one of the two players.
        if winner == player1 or winner == player2:
            break

        print("Winner must be either Player 1 or Player 2.")
        pause_screen()

    while True:
        match_status = input(
            "Enter Match Status "
            "('To be played', 'In progress', 'Finished'): "
        ).strip()

        if match_status == "":
            match_status = matches[5]
            break

        elif match_status.lower() == "back":
            return

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


    if match_status == "Finished":

        # A finished match MUST have a winner.
        while winner is None:
            print("A finished match must have a winner.")

            winner = input("Enter winner (Player ID): ").strip().upper()

            if winner == "BACK":
                return

            if winner == player1 or winner == player2:
                break

            print("Winner must be either Player 1 or Player 2.")
            pause_screen()

    else:
        # Unfinished matches cannot have a winner.
        winner = None

    cursor.execute("""
        UPDATE Matches
        SET TournamentID = ?,
            Player1 = ?,
            Player2 = ?,
            Winner = ?,
            MatchStatus = ?,
            Round = ?
        WHERE MatchesID = ?
    """, (
        tournamentid,
        player1,
        player2,
        winner,
        match_status,
        round_number,
        matchid
    ))

    conn.commit()

    print("Match details updated successfully.")
    pause_screen()


# Delete match: handles delete match for the system.
def delete_match():
    while True:
        clear_screen()
        print("-" * 60)
        print("                  Delete Match")
        print("-" * 60)

        id_input = input(
            "Enter Match ID to delete (or type 'back'): "
        ).strip().upper()

        if id_input == "BACK":
            break

        cursor.execute(
            "SELECT * FROM Matches WHERE MatchesID = ?",
            (id_input,)
        )

        matches = cursor.fetchone()

        if matches:
            print_as_table(cursor, matches)

            # Finished matches cannot be deleted.
            if matches[5] == "Finished":
                print("Finished matches cannot be cancelled.")
                pause_screen()
                continue

            confirm = input(
                "Are you sure you want to cancel this match? (yes/no): "
            ).lower().strip()

            if confirm == "yes":
                cursor.execute(
                    "DELETE FROM Matches WHERE MatchesID = ?",
                    (matches[0],)
                )

                conn.commit()

                print("Match cancelled successfully.")
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




VALID_RARITIES = {
    "Common", "Uncommon", "Rare", "Rare Holo", "Double Rare",
    "Ultra Rare", "Illustration Rare", "Special Illustration Rare",
    "Hyper Rare", "Ace Spec"
}

VALID_CARD_TYPES = {
    "1": "Creature Card",
    "2": "Trainer Card",
    "3": "Energy Card"
}


def _get_next_card_id():
    """Return the next available C### style CardID."""
    cursor.execute("SELECT CardID FROM Card")
    ids = cursor.fetchall()
    numbers = []
    for row in ids:
        value = row[0]
        if isinstance(value, str) and value.startswith("C") and value[1:].isdigit():
            numbers.append(int(value[1:]))
    next_number = max(numbers, default=0) + 1
    return f"C{next_number:03d}"


def _get_next_child_id(card_id, table, column, prefix):
    """Return the next C###-AT# / C###-AB# style child ID."""
    cursor.execute(
        f"SELECT {column} FROM {table} WHERE CardID = ?", (card_id,)
    )
    ids = cursor.fetchall()
    numbers = []
    marker = f"-{prefix}"
    for row in ids:
        value = row[0]
        if isinstance(value, str) and marker in value:
            suffix = value.rsplit(marker, 1)[-1]
            if suffix.isdigit():
                numbers.append(int(suffix))
    return f"{card_id}{marker}{max(numbers, default=0) + 1}"


def _ask_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be blank.")


def _ask_rarity(current=None):
    while True:
        prompt = "Rarity"
        if current is not None:
            prompt += f" [{current}]"
        value = input(f"Update {prompt}: " if current is not None else "Rarity: ").strip()
        if not value and current is not None:
            return current
        if value in VALID_RARITIES:
            return value
        print("Invalid rarity. Please choose a valid rarity.")


def manage_cards():
    if user_position not in ["Administrator", "Moderator"]:
        print("You do not have permission to manage cards.")
        pause_screen()
        return "0"

    clear_screen()
    print("-" * 75)
    print("                       Manage Cards")
    print("-" * 75)
    print("  [1] View Card Details           [4] Delete Card")
    print("  [2] Edit Card Details           [0] Back to Main Menu")
    print("  [3] Create Card")
    print("")
    return input("\nSelect an option: ").strip()


def view_card_details():
    while True:
        clear_screen()
        print("-" * 90)
        print("                             View Card Details")
        print("-" * 90)
        category = input("""
[1] View Specific Card Details                                [3] View all cards
[2] View cards of a specific card type/element type/rarity    [0] Back

Select an option: """).strip().lower()

        if category == "0":
            return

        if category == "1":
            while True:
                clear_screen()
                print("-" * 60)
                print("             View Specific Card Details")
                print("-" * 60)
                choice = input("Search by Card 'Name' or 'ID' (or type 'back'): ").strip().lower()
                if choice == "back":
                    break
                if choice not in ("id", "name"):
                    print("Please enter 'id', 'name', or 'back'.")
                    pause_screen()
                    continue

                if choice == "id":
                    while True:
                        card_id = input("Enter Card ID (or type 'back'): ").strip()
                        if card_id.lower() == "back":
                            break
                        cursor.execute("SELECT * FROM Card WHERE CardID = ?", (card_id,))
                        card = cursor.fetchone()
                        if card:
                            print_as_table(cursor, [card])
                            pause_screen()
                            break
                        print("\nInvalid Card ID")
                        pause_screen()
                else:
                    while True:
                        cardname = input("Enter Card Name (or type 'back'): ").strip()
                        if cardname.lower() == "back":
                            break
                        cursor.execute(
                            "SELECT * FROM Card WHERE CardName LIKE ? ORDER BY CardName ASC",
                            (f"%{cardname}%",)
                        )
                        cards = cursor.fetchall()
                        if cards:
                            print_as_table(cursor, cards)
                            pause_screen()
                            break
                        print("\nNo matching Card Name found.")
                        pause_screen()

        elif category == "2":
            while True:
                clear_screen()
                print("-" * 60)
                print("             View Cards by Category")
                print("-" * 60)
                choice = input(
                    "Select from: Creature, Trainer, Energy, Type, Rarity (or type 'back'): "
                ).strip().lower()
                if choice == "back":
                    break

                if choice in ("creature", "trainer", "energy"):
                    target_type = {
                        "creature": "Creature Card",
                        "trainer": "Trainer Card",
                        "energy": "Energy Card"
                    }[choice]
                    cursor.execute(
                        "SELECT COUNT(*) FROM Card WHERE CardType = ?", (target_type,)
                    )
                    num_cards = cursor.fetchone()[0]
                    print(f"\nTotal Number of {target_type}s: {num_cards}")
                    cursor.execute(
                        "SELECT * FROM Card WHERE CardType = ? ORDER BY CardID ASC",
                        (target_type,)
                    )
                    cards = cursor.fetchall()
                    if cards:
                        print_as_table(cursor, cards)
                    else:
                        print(f"\nNo {target_type}s found")
                    pause_screen()

                elif choice == "type":
                    element_type = input(
                        "Enter Type (e.g., Fire, Water, Lightning) (or type 'back'): "
                    ).strip()
                    if element_type.lower() == "back":
                        continue
                    cursor.execute("""
                        SELECT DISTINCT Card.*
                        FROM Card
                        LEFT JOIN CreatureCard ON CreatureCard.CardID = Card.CardID
                        LEFT JOIN EnergyCard ON EnergyCard.CardID = Card.CardID
                        WHERE CreatureCard.ElementType = ?
                           OR EnergyCard.ElementType = ?
                        ORDER BY Card.CardID ASC
                    """, (element_type, element_type))
                    cards = cursor.fetchall()
                    print(f"\nTotal Cards of Element '{element_type}': {len(cards)}")
                    if cards:
                        print_as_table(cursor, cards)
                    else:
                        print("\nNo Cards of this Element found")
                    pause_screen()

                elif choice == "rarity":
                    rarity = input(
                        "Enter Rarity (e.g., Common, Rare, Ultra Rare) (or type 'back'): "
                    ).strip()
                    if rarity.lower() == "back":
                        continue
                    cursor.execute(
                        "SELECT * FROM Card WHERE Rarity LIKE ? ORDER BY CardID ASC",
                        (f"%{rarity}%",)
                    )
                    cards = cursor.fetchall()
                    print(f"\nTotal Cards of Rarity '{rarity}': {len(cards)}")
                    if cards:
                        print_as_table(cursor, cards)
                    else:
                        print("\nNo Cards of this Rarity found")
                    pause_screen()
                else:
                    print("Invalid option.")
                    pause_screen()

        elif category == "3":
            while True:
                clear_screen()
                print("-" * 60)
                print("             View All Cards")
                print("-" * 60)
                choice = input(
                    "Order by id, name, card number or rarity? (or type 'back'): "
                ).strip().lower()
                if choice == "back":
                    break

                if choice not in ("name", "id", "card number", "rarity"):
                    print("Invalid sort option.")
                    pause_screen()
                    continue

                order_clause = {
                    "name": "CardName ASC",
                    "id": "CardID ASC",
                    "card number": "CardNumber ASC",
                    "rarity": """CASE Card.Rarity
                        WHEN 'Special Illustration Rare' THEN 1
                        WHEN 'Illustration Rare' THEN 2
                        WHEN 'Hyper Rare' THEN 3
                        WHEN 'Ultra Rare' THEN 4
                        WHEN 'Ace Spec' THEN 5
                        WHEN 'Double Rare' THEN 6
                        WHEN 'Rare Holo' THEN 7
                        WHEN 'Rare' THEN 8
                        WHEN 'Uncommon' THEN 9
                        WHEN 'Common' THEN 10
                        ELSE 11 END ASC, CardName ASC"""
                }[choice]

                cursor.execute(f"""
                    SELECT CardID, CardName, CardType, CardNumber, Rarity, SetName
                    FROM Card
                    JOIN CardSet ON Card.SetID = CardSet.SetID
                    ORDER BY {order_clause}
                """)
                cards = cursor.fetchall()
                if cards:
                    print_as_table(cursor, cards)
                else:
                    print("No Card Found (gasp)")
                pause_screen()
        else:
            print("Invalid option.")
            pause_screen()


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
            return
        if category not in VALID_CARD_TYPES:
            print("Invalid option.")
            pause_screen()
            continue

        card_type = VALID_CARD_TYPES[category]
        while True:
            clear_screen()
            print("-" * 60)
            print(f"              Edit {card_type}")
            print("-" * 60)
            choice = input("Enter Card ID or Card Name (or type 'back'): ").strip()
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
            print("\nCard not found or card type does not match.")
            pause_screen()


def edit_card_details_checks(card, cursor, card_type):
    cardid = card[0]

    try:
        clear_screen()
        print("-" * 60)
        print("                  Edit Card Details")
        print("-" * 60)
        print_as_table(cursor, [card])
        print("\nPlease enter the card data you wish to change.")
        print("If you do not wish to change a field, just press Enter.")

        # Common Card fields
        while True:
            new_cardname = input(f"Update Card Name [{card[2]}]: ").strip()
            if not new_cardname:
                new_cardname = card[2]
                break
            cursor.execute(
                "SELECT CardID FROM Card WHERE CardName = ? AND CardID != ?",
                (new_cardname, cardid)
            )
            if cursor.fetchone():
                print("A card with that name already exists.")
            else:
                break

        while True:
            new_setid = input(f"Update Set ID [{card[1]}]: ").strip()
            if not new_setid:
                new_setid = card[1]
                break
            cursor.execute("SELECT SetID FROM CardSet WHERE SetID = ?", (new_setid,))
            if cursor.fetchone():
                break
            print("Invalid Set ID.")

        while True:
            new_cardnumber = input(f"Update Card Number [{card[4]}]: ").strip()
            if not new_cardnumber:
                new_cardnumber = card[4]
                break
            cursor.execute("""
                SELECT CardID
                FROM Card
                WHERE CardNumber = ?
                  AND SetID = ?
                  AND CardID != ?
            """, (new_cardnumber, new_setid, cardid))
            if cursor.fetchone():
                print("A card with that number already exists in this set.")
            else:
                break

        new_rarity = _ask_rarity(card[5])

        cursor.execute("""
            UPDATE Card
            SET SetID = ?, CardName = ?, CardNumber = ?, Rarity = ?
            WHERE CardID = ?
        """, (new_setid, new_cardname, new_cardnumber, new_rarity, cardid))

        if card_type == "Creature Card":
            cursor.execute("""
                SELECT EvolutionStage, HP, ElementType, RetreatCost, Weakness, Resistance
                FROM CreatureCard WHERE CardID = ?
            """, (cardid,))
            creature = cursor.fetchone()
            if creature is None:
                raise ValueError(f"CreatureCard data is missing for {cardid}.")

            new_evolution = input(f"Update Evolution Stage [{creature[0]}]: ").strip() or creature[0]
            while True:
                value = input(f"Update HP [{creature[1]}]: ").strip()
                if not value:
                    new_hp = creature[1]
                    break
                if value.isdigit() and int(value) > 0:
                    new_hp = int(value)
                    break
                print("HP must be a positive number.")

            new_element = input(f"Update Element Type [{creature[2]}]: ").strip() or creature[2]
            while True:
                value = input(f"Update Retreat Cost [{creature[3]}]: ").strip()
                if not value:
                    new_retreat = creature[3]
                    break
                if value.isdigit() and int(value) >= 0:
                    new_retreat = int(value)
                    break
                print("Retreat Cost must be a non-negative number.")

            new_weakness = input(f"Update Weakness [{creature[4]}]: ").strip() or creature[4]
            new_resistance = input(f"Update Resistance [{creature[5]}]: ").strip() or creature[5]

            cursor.execute("""
                UPDATE CreatureCard
                SET EvolutionStage = ?, HP = ?, ElementType = ?, RetreatCost = ?,
                    Weakness = ?, Resistance = ?
                WHERE CardID = ?
            """, (new_evolution, new_hp, new_element, new_retreat,
                  new_weakness, new_resistance, cardid))

        elif card_type == "Trainer Card":
            cursor.execute(
                "SELECT Subtype, Rules FROM TrainerCard WHERE CardID = ?", (cardid,)
            )
            trainer = cursor.fetchone()
            if trainer is None:
                raise ValueError(f"TrainerCard data is missing for {cardid}.")

            new_subtype = input(f"Update Subtype [{trainer[0]}]: ").strip() or trainer[0]
            new_rules = input(f"Update Rules [{trainer[1]}]: ").strip() or trainer[1]
            cursor.execute("""
                UPDATE TrainerCard
                SET Subtype = ?, Rules = ?
                WHERE CardID = ?
            """, (new_subtype, new_rules, cardid))

        elif card_type == "Energy Card":
            cursor.execute("""
                SELECT ElementType, EnergyType, SpecialEffects
                FROM EnergyCard WHERE CardID = ?
            """, (cardid,))
            energy = cursor.fetchone()
            if energy is None:
                raise ValueError(f"EnergyCard data is missing for {cardid}.")

            new_element = input(f"Update Element Type [{energy[0]}]: ").strip() or energy[0]
            new_energytype = input(f"Update Energy Type [{energy[1]}]: ").strip() or energy[1]
            new_effects = input(f"Update Special Effects [{energy[2]}]: ").strip() or energy[2]
            cursor.execute("""
                UPDATE EnergyCard
                SET ElementType = ?, EnergyType = ?, SpecialEffects = ?
                WHERE CardID = ?
            """, (new_element, new_energytype, new_effects, cardid))

        # Attacks and abilities are part of the same transaction.
        if card_type == "Creature Card":
            while True:
                attack_choice = input("""
Would you like to:
[1] Edit an existing attack
[2] Add a new attack
[3] Finish attacks

Select an option: """).strip()
                if attack_choice == "1":
                    edit_attack(cardid, commit=False)
                elif attack_choice == "2":
                    add_attack(cardid, commit=False)
                elif attack_choice == "3":
                    break
                else:
                    print("Invalid option.")

            while True:
                ability_choice = input("""
Would you like to:
[1] Edit an existing ability
[2] Add a new ability
[3] Finish abilities

Select an option: """).strip()
                if ability_choice == "1":
                    edit_ability(cardid, commit=False)
                elif ability_choice == "2":
                    add_ability(cardid, commit=False)
                elif ability_choice == "3":
                    break
                else:
                    print("Invalid option.")

        conn.commit()
        print("\nCard details updated successfully!")
        pause_screen()

    except (sqlite3.Error, ValueError) as error:
        conn.rollback()
        print(f"\nUpdate failed. No changes were saved.")
        print(f"Reason: {error}")
        pause_screen()


def edit_attack(card_id, commit=True):
    cursor.execute("""
        SELECT AttackID, AttackName, Damage, EnergyCost, Effect
        FROM AttackDetails WHERE CardID = ? ORDER BY AttackID
    """, (card_id,))
    attacks = cursor.fetchall()
    if not attacks:
        print("\nThis card has no attacks to edit.")
        pause_screen()
        return False

    print("\nExisting Attacks:")
    print_as_table(cursor, attacks)
    while True:
        attack_id = input("\nEnter Attack ID to edit (or type 'back'): ").strip()
        if attack_id.lower() == "back":
            return False
        cursor.execute("""
            SELECT AttackID, AttackName, Damage, EnergyCost, Effect
            FROM AttackDetails
            WHERE AttackID = ? AND CardID = ?
        """, (attack_id, card_id))
        attack = cursor.fetchone()
        if attack:
            break
        print("Invalid Attack ID.")

    new_name = input(f"Update Attack Name [{attack[1]}]: ").strip() or attack[1]
    new_damage = input(f"Update Damage [{attack[2]}]: ").strip() or attack[2]
    new_energy = input(f"Update Energy Cost [{attack[3]}]: ").strip() or attack[3]
    new_effect = input(f"Update Effect [{attack[4]}]: ").strip() or attack[4]

    cursor.execute("""
        UPDATE AttackDetails
        SET AttackName = ?, Damage = ?, EnergyCost = ?, Effect = ?
        WHERE AttackID = ? AND CardID = ?
    """, (new_name, new_damage, new_energy, new_effect, attack_id, card_id))

    if commit:
        conn.commit()
    print(f"\nAttack {attack_id} updated successfully!")
    pause_screen()
    return True


def edit_ability(card_id, commit=True):
    cursor.execute("""
        SELECT AbilityID, AbilityName, AbilityType, Description
        FROM CardAbility WHERE CardID = ? ORDER BY AbilityID
    """, (card_id,))
    abilities = cursor.fetchall()
    if not abilities:
        print("\nThis card has no abilities to edit.")
        pause_screen()
        return False

    print("\nExisting Abilities:")
    print_as_table(cursor, abilities)
    while True:
        ability_id = input("\nEnter Ability ID to edit (or type 'back'): ").strip()
        if ability_id.lower() == "back":
            return False
        cursor.execute("""
            SELECT AbilityID, AbilityName, AbilityType, Description
            FROM CardAbility
            WHERE AbilityID = ? AND CardID = ?
        """, (ability_id, card_id))
        ability = cursor.fetchone()
        if ability:
            break
        print("Invalid Ability ID.")

    new_name = input(f"Update Ability Name [{ability[1]}]: ").strip() or ability[1]
    new_type = input(f"Update Ability Type [{ability[2]}]: ").strip() or ability[2]
    new_description = input(f"Update Description [{ability[3]}]: ").strip() or ability[3]

    cursor.execute("""
        UPDATE CardAbility
        SET AbilityName = ?, AbilityType = ?, Description = ?
        WHERE AbilityID = ? AND CardID = ?
    """, (new_name, new_type, new_description, ability_id, card_id))

    if commit:
        conn.commit()
    print(f"\nAbility {ability_id} updated successfully!")
    pause_screen()
    return True


def add_attack(card_id, commit=True):
    attack_id = _get_next_child_id(card_id, "AttackDetails", "AttackID", "AT")
    attack_name = _ask_non_empty("Attack Name: ")
    damage = _ask_non_empty("Damage: ")
    energy_cost = _ask_non_empty("Energy Cost: ")
    effect = input("Effect: ").strip()

    cursor.execute("""
        INSERT INTO AttackDetails
        (AttackID, CardID, AttackName, Damage, EnergyCost, Effect)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (attack_id, card_id, attack_name, damage, energy_cost, effect))

    if commit:
        conn.commit()
    print(f"\nAttack {attack_id} added successfully!")
    return True


def add_ability(card_id, commit=True):
    ability_id = _get_next_child_id(card_id, "CardAbility", "AbilityID", "AB")
    ability_name = _ask_non_empty("Ability Name: ")
    ability_type = input("Ability Type: ").strip()
    description = input("Description: ").strip()

    cursor.execute("""
        INSERT INTO CardAbility
        (AbilityID, CardID, AbilityName, AbilityType, Description)
        VALUES (?, ?, ?, ?, ?)
    """, (ability_id, card_id, ability_name, ability_type, description))

    if commit:
        conn.commit()
    print(f"\nAbility {ability_id} added successfully!")
    return True


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
            return
        if category not in VALID_CARD_TYPES:
            print("Invalid option.")
            pause_screen()
            continue

        card_type = VALID_CARD_TYPES[category]
        card_id = _get_next_card_id()

        try:
            card_name = _ask_non_empty("Card Name: ")
            while True:
                cursor.execute("SELECT CardID FROM Card WHERE CardName = ?", (card_name,))
                if not cursor.fetchone():
                    break
                print("A card with that name already exists.")
                card_name = _ask_non_empty("Card Name: ")

            while True:
                set_id = _ask_non_empty("Set ID: ")
                cursor.execute("SELECT SetID FROM CardSet WHERE SetID = ?", (set_id,))
                if cursor.fetchone():
                    break
                print("Invalid Set ID.")

            while True:
                card_number = _ask_non_empty("Card Number: ")
                cursor.execute("""
                    SELECT CardID FROM Card
                    WHERE CardNumber = ? AND SetID = ?
                """, (card_number, set_id))
                if not cursor.fetchone():
                    break
                print("A card with that number already exists in this set.")

            rarity = _ask_rarity()

            cursor.execute("""
                INSERT INTO Card (CardID, SetID, CardName, CardType, CardNumber, Rarity)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (card_id, set_id, card_name, card_type, card_number, rarity))

            if category == "1":
                evolution = input("Evolution Stage: ").strip()
                while True:
                    hp = input("HP: ").strip()
                    if hp.isdigit() and int(hp) > 0:
                        hp = int(hp)
                        break
                    print("HP must be a positive number.")

                element = _ask_non_empty("Element Type: ")
                while True:
                    retreat_cost = input("Retreat Cost: ").strip()
                    if retreat_cost.isdigit() and int(retreat_cost) >= 0:
                        retreat_cost = int(retreat_cost)
                        break
                    print("Retreat Cost must be a non-negative number.")

                weakness = input("Weakness: ").strip()
                resistance = input("Resistance: ").strip()
                cursor.execute("""
                    INSERT INTO CreatureCard
                    (CardID, EvolutionStage, HP, ElementType, RetreatCost, Weakness, Resistance)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (card_id, evolution, hp, element, retreat_cost, weakness, resistance))

            elif category == "2":
                subtype = input("Subtype: ").strip()
                rules = input("Rules: ").strip()
                cursor.execute("""
                    INSERT INTO TrainerCard (CardID, Subtype, Rules)
                    VALUES (?, ?, ?)
                """, (card_id, subtype, rules))

            else:
                element = _ask_non_empty("Element Type: ")
                energy_type = _ask_non_empty("Energy Type: ")
                special_effects = input("Special Effects: ").strip()
                cursor.execute("""
                    INSERT INTO EnergyCard (CardID, ElementType, EnergyType, SpecialEffects)
                    VALUES (?, ?, ?, ?)
                """, (card_id, element, energy_type, special_effects))

            # Keep the card and its subtype in one transaction.
            conn.commit()
            print(f"\nCard {card_id} created successfully!")

        except (sqlite3.Error, ValueError) as error:
            conn.rollback()
            print("\nCard creation failed. No changes were saved.")
            print(f"Reason: {error}")
            pause_screen()
            continue

        if category == "1":
            while True:
                choice = input("\nWould you like to add an attack? (y/n): ").strip().lower()
                if choice == "n":
                    break
                if choice == "y":
                    while True:
                        try:
                            add_attack(card_id)
                        except sqlite3.Error as error:
                            conn.rollback()
                            print(f"Could not add attack: {error}")
                        more = input("\nWould you like to add another attack? (y/n): ").strip().lower()
                        if more == "n":
                            break
                        if more != "y":
                            print("Please enter y or n.")
                    break
                print("Please enter y or n.")

            while True:
                choice = input("\nWould you like to add an ability? (y/n): ").strip().lower()
                if choice == "n":
                    break
                if choice == "y":
                    while True:
                        try:
                            add_ability(card_id)
                        except sqlite3.Error as error:
                            conn.rollback()
                            print(f"Could not add ability: {error}")
                        more = input("\nWould you like to add another ability? (y/n): ").strip().lower()
                        if more == "n":
                            break
                        if more != "y":
                            print("Please enter y or n.")
                    break
                print("Please enter y or n.")

        pause_screen()
        return


def delete_card():
    print("\n------------------- Delete Card -------------------")
    card_id = input("Enter the Card ID you wish to delete (or type 'back'): ").strip()
    if card_id.lower() == "back":
        return

    cursor.execute(
        "SELECT CardName, CardType FROM Card WHERE CardID = ?", (card_id,)
    )
    card = cursor.fetchone()
    if not card:
        print(f"Error: No card found with ID '{card_id}'.")
        pause_screen()
        return

    card_name, card_type = card
    cursor.execute(
        "SELECT COALESCE(SUM(Quantity), 0) FROM PlayerCollection WHERE CardID = ?",
        (card_id,)
    )
    count_collection = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COALESCE(SUM(Quantity), 0) FROM CardInDeck WHERE CardID = ?",
        (card_id,)
    )
    count_decks = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM TradeCard WHERE CardID = ?", (card_id,))
    count_trades = cursor.fetchone()[0]

    print("\n[WARNING]")
    print(f"Card Name: '{card_name}' (Type: {card_type})")
    print(f"Linked in Player Inventories: {count_collection} copies")
    print(f"Attached to Player Decks: {count_decks} copies")
    print(f"Linked to Trade Offers: {count_trades} records")

    confirm = input("\nThis action is irreversible. Delete this card and its dependencies? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion aborted. No changes were made to the database.")
        pause_screen()
        return

    try:
        # Delete children before parent so this works even without ON DELETE CASCADE.
        for table in (
            "CardInDeck", "PlayerCollection", "TradeCard",
            "CardAbility", "AttackDetails", "CreatureCard",
            "TrainerCard", "EnergyCard"
        ):
            cursor.execute(f"DELETE FROM {table} WHERE CardID = ?", (card_id,))

        cursor.execute("DELETE FROM Card WHERE CardID = ?", (card_id,))
        if cursor.rowcount != 1:
            raise sqlite3.Error("Card could not be deleted.")

        conn.commit()
        print(f"\nSuccess! '{card_name}' (ID: {card_id}) and its references were removed.")

    except sqlite3.Error as error:
        conn.rollback()
        print("\n[DATABASE ERROR] Deletion failed. Transaction rolled back safely.")
        print(f"Reason: {error}")

    pause_screen()



# Manage decks: handles manage decks for the system.
def manage_decks():
    if user_position in ["Administrator", "Moderator"]:
        clear_screen()
        print("-" * 75)
        print("                       Manage Decks")
        print("-" * 75)
        print("  [1] View all cards in a Deck")
        print("  [2] View all decks containing a specific card")
        print("  [0] Back to Main Menu")
        print("")
        return input("\nSelect an option: ").strip()

    elif user_position == "Staff":
        return "0"

    return "0"


# View deck cards: handles viewing all cards in a deck.
def view_deck_cards():
    rarity_order = """
        CASE
            WHEN UPPER(Card.Rarity) LIKE '%SPECIAL ILLUSTRATION%' THEN 1
            WHEN UPPER(Card.Rarity) LIKE '%ILLUSTRATION RARE%' THEN 2
            WHEN UPPER(Card.Rarity) LIKE '%HYPER RARE%' THEN 3
            WHEN UPPER(Card.Rarity) LIKE '%ULTRA RARE%' THEN 4
            WHEN UPPER(Card.Rarity) LIKE '%ACE SPEC%' THEN 5
            WHEN UPPER(Card.Rarity) LIKE '%DOUBLE RARE%' THEN 6
            WHEN UPPER(Card.Rarity) LIKE '%RARE HOLO%' THEN 7
            WHEN UPPER(Card.Rarity) LIKE '%RARE%' THEN 8
            WHEN UPPER(Card.Rarity) LIKE '%UNCOMMON%' THEN 9
            WHEN UPPER(Card.Rarity) LIKE '%COMMON%' THEN 10
            ELSE 11
        END ASC
    """

    while True:
        clear_screen()
        print("-" * 60)
        print("                     View Cards in a Deck")
        print("-" * 60)

        category = input(
            "Search by Deck 'Name' or 'ID' (or type 'back'): "
        ).strip().lower()

        if category == "back":
            break

        if category not in ["id", "name"]:
            print("Invalid option. Enter 'id', 'name' or 'back'.")
            pause_screen()
            continue

        while True:
            if category == "id":
                deck_id = input("Enter Deck ID (or type 'back'): ").strip()

                if deck_id.lower() == "back":
                    break

                cursor.execute(
                    "SELECT DeckID, DeckName, PlayerID FROM Deck WHERE DeckID = ?",
                    (deck_id,)
                )
                deck = cursor.fetchone()

                if not deck:
                    print("\nDeck not found, try again.")
                    pause_screen()
                    continue

                where_clause = "Deck.DeckID = ?"
                search_value = deck_id

            else:
                deck_name = input(
                    "Enter Deck Name (or type 'back'): "
                ).strip()

                if deck_name.lower() == "back":
                    break

                cursor.execute(
                    "SELECT DeckID, DeckName, PlayerID FROM Deck WHERE DeckName = ?",
                    (deck_name,)
                )
                deck = cursor.fetchone()

                if not deck:
                    print("\nDeck not found, try again.")
                    pause_screen()
                    continue

                where_clause = "Deck.DeckID = ?"
                search_value = deck[0]

            # Get deck statistics.
            # LEFT JOIN allows an empty deck to still be found and displayed.
            cursor.execute(f"""
                SELECT
                    Deck.DeckID,
                    Deck.DeckName,
                    Player.Username,
                    COALESCE(SUM(CardInDeck.Quantity), 0) AS 'Total Cards In Deck',
                    COUNT(DISTINCT CardInDeck.CardID) AS 'Number of Unique Cards',
                    COALESCE(SUM(
                        CASE
                            WHEN Card.CardType = 'Creature Card'
                            THEN CardInDeck.Quantity
                            ELSE 0
                        END
                    ), 0) AS 'Creature Cards',
                    COALESCE(SUM(
                        CASE
                            WHEN Card.CardType = 'Trainer Card'
                            THEN CardInDeck.Quantity
                            ELSE 0
                        END
                    ), 0) AS 'Trainer Cards',
                    COALESCE(SUM(
                        CASE
                            WHEN Card.CardType = 'Energy Card'
                            THEN CardInDeck.Quantity
                            ELSE 0
                        END
                    ), 0) AS 'Energy Cards'
                FROM Deck
                JOIN Player ON Player.PlayerID = Deck.PlayerID
                LEFT JOIN CardInDeck ON CardInDeck.DeckID = Deck.DeckID
                LEFT JOIN Card ON Card.CardID = CardInDeck.CardID
                WHERE {where_clause}
                GROUP BY Deck.DeckID, Deck.DeckName, Player.Username
            """, (search_value,))

            deck_stats = cursor.fetchone()

            if deck_stats:
                print("\nDeck Information:")
                print_as_table(cursor, [deck_stats])

            # Get cards in the deck.
            cursor.execute(f"""
                SELECT
                    Card.CardID,
                    Card.CardName,
                    Card.CardType,
                    Card.CardNumber,
                    Card.Rarity,
                    CardInDeck.Quantity
                FROM Card
                JOIN CardInDeck ON CardInDeck.CardID = Card.CardID
                WHERE CardInDeck.DeckID = ?
                ORDER BY {rarity_order}, Card.CardName ASC
            """, (search_value,))

            cards = cursor.fetchall()

            if cards:
                print("\nCards in Deck:")
                print_as_table(cursor, cards)
            else:
                print("\nThis deck contains no cards.")

            pause_screen()
            break


# View all decks containing a specific card.
def view_all_decks_containing_specific_card():
    while True:
        clear_screen()
        print("-" * 60)
        print("             View All Decks Containing A Specific Card")
        print("-" * 60)

        category = input(
            "Search for Card by 'Name' or 'ID' (or type 'back'): "
        ).strip().lower()

        if category == "back":
            break

        if category not in ["id", "name"]:
            print("Invalid option. Enter 'id', 'name' or 'back'.")
            pause_screen()
            continue

        while True:
            if category == "id":
                card_id = input(
                    "Enter Card ID (or type 'back'): "
                ).strip()

                if card_id.lower() == "back":
                    break

                cursor.execute(
                    "SELECT CardID, CardName FROM Card WHERE CardID = ?",
                    (card_id,)
                )
                card = cursor.fetchone()

                if not card:
                    print("\nCard not found.")
                    pause_screen()
                    continue

                search_value = card_id
                where_clause = "CardInDeck.CardID = ?"

            else:
                card_name = input(
                    "Enter Card Name (or type 'back'): "
                ).strip()

                if card_name.lower() == "back":
                    break

                # Use fetchall because multiple cards with the same name
                # are possible in different sets.
                cursor.execute(
                    "SELECT CardID, CardName FROM Card WHERE CardName = ?",
                    (card_name,)
                )
                matching_cards = cursor.fetchall()

                if not matching_cards:
                    print("\nCard not found.")
                    pause_screen()
                    continue

                if len(matching_cards) > 1:
                    print("\nMultiple cards have that name:")
                    print_as_table(cursor, matching_cards)

                    selected_id = input(
                        "Enter the Card ID you want to search for (or type 'back'): "
                    ).strip()

                    if selected_id.lower() == "back":
                        break

                    valid_ids = [card[0] for card in matching_cards]

                    if selected_id not in valid_ids:
                        print("Invalid Card ID.")
                        pause_screen()
                        continue

                    search_value = selected_id
                    where_clause = "CardInDeck.CardID = ?"
                else:
                    search_value = matching_cards[0][0]
                    where_clause = "CardInDeck.CardID = ?"

            cursor.execute(f"""
                SELECT
                    Deck.DeckID,
                    Deck.DeckName,
                    Player.Username,
                    CardInDeck.Quantity
                FROM CardInDeck
                JOIN Deck ON CardInDeck.DeckID = Deck.DeckID
                JOIN Player ON Player.PlayerID = Deck.PlayerID
                WHERE {where_clause}
                ORDER BY Deck.DeckName ASC
            """, (search_value,))

            decks = cursor.fetchall()

            if decks:
                print("\nDecks containing this card:")
                print_as_table(cursor, decks)
            else:
                print("\nNo decks contain this card.")

            pause_screen()
            break


def manage_staff():
    if user_position == "Administrator":
        clear_screen()
        print("-" * 75)
        print("                     Manage Staff Members")
        print("-" * 75)
        print("  [1] View Staff Details             [4] Delete Staff Member")
        print("  [2] Edit Staff Details             [0] Back to Main Menu")
        print("  [3] Create New Staff Member")
        print("")

        return input("\nSelect an option: ").strip()

    # Staff and Moderators do not have access to staff management.
    return "0"



def view_staff_details():
    while True:
        clear_screen()
        print("-" * 90)
        print("                         View Staff Details")
        print("-" * 90)
        print("  [1] View all Staff Details")
        print("  [2] Search for Staff Members by Role")
        print("  [3] Search for Staff Member by ID or Username")
        print("  [0] Back to Main Menu")
        print("")

        choice = input("Select an option: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            cursor.execute("""
                SELECT *
                FROM Staff
                ORDER BY Position ASC, StaffID ASC
            """)

            staff = cursor.fetchall()

            if staff:
                print_as_table(cursor, staff)
            else:
                print("\nNo staff members found.")

            pause_screen()

        elif choice == "2":
            while True:
                role = input(
                    "Enter Staff Role "
                    "(Administrator/Moderator/Staff, or type 'back'): "
                ).strip()

                if role.lower() == "back":
                    break

                # Make role matching case-insensitive for user input.
                role_lookup = {
                    "administrator": "Administrator",
                    "moderator": "Moderator",
                    "staff": "Staff"
                }

                role = role_lookup.get(role.lower())

                if role is None:
                    print(
                        "\nInvalid role. Please enter "
                        "Administrator, Moderator or Staff."
                    )
                    pause_screen()
                    continue

                cursor.execute("""
                    SELECT *
                    FROM Staff
                    WHERE Position = ?
                    ORDER BY FirstName ASC, LastName ASC, StaffID ASC
                """, (role,))

                staff = cursor.fetchall()

                if staff:
                    print_as_table(cursor, staff)
                    pause_screen()
                    break

                print("\nNo staff members found with that role.")
                pause_screen()

        elif choice == "3":
            while True:
                search = input(
                    "Search by 'ID' or 'Username' "
                    "(or type 'back'): "
                ).strip().lower()

                if search == "back":
                    break
                if search == "id":
                    while True:
                        staff_id = input(
                            "Enter Staff ID (or type 'back'): "
                        ).strip().upper()

                        if staff_id.lower() == "back":
                            break

                        cursor.execute("""
                            SELECT *
                            FROM Staff
                            WHERE StaffID = ?
                        """, (staff_id,))

                        staff = cursor.fetchone()

                        if staff:
                            # print_as_table expects rows, so wrap
                            # the single tuple in a list.
                            print_as_table(cursor, [staff])
                            pause_screen()
                            break

                        print(
                            "\nNo staff member found with that ID. "
                            "Please try again."
                        )
                        pause_screen()

                elif search == "username":
                    while True:
                        username = input(
                            "Enter Staff Username (or type 'back'): "
                        ).strip()

                        if username.lower() == "back":
                            break

                        cursor.execute("""
                            SELECT *
                            FROM Staff
                            WHERE Username = ?
                        """, (username,))

                        staff = cursor.fetchone()

                        if staff:
                            print_as_table(cursor, [staff])
                            pause_screen()
                            break

                        print(
                            "\nNo staff member found with that username. "
                            "Please try again."
                        )
                        pause_screen()

                else:
                    print(
                        "\nInvalid option. Please enter "
                        "'ID', 'Username' or 'back'."
                    )
                    pause_screen()

        else:
            print("\nInvalid option. Please select 0, 1, 2 or 3.")
            pause_screen()



def edit_staff_details():
    while True:
        clear_screen()
        print("-" * 60)
        print("                  Edit Staff Details")
        print("-" * 60)

        search = input(
            "(type 'back' to go back)\n"
            "Find staff member to edit by ID or Username: "
        ).strip().lower()

        if search == "back":
            break

        if search == "id":
            while True:
                staff_id = input(
                    "Enter Staff ID (or type 'back'): "
                ).strip().upper()

                if staff_id.lower() == "back":
                    break

                cursor.execute("""
                    SELECT *
                    FROM Staff
                    WHERE StaffID = ?
                """, (staff_id,))

                staff = cursor.fetchone()

                if staff:
                    edit_staff_details_checks(staff, cursor)
                    break

                print(
                    "\nNo staff member found with that ID. "
                    "Please try again."
                )
                pause_screen()

        elif search == "username":
            while True:
                username = input(
                    "Enter Staff Username (or type 'back'): "
                ).strip()

                if username.lower() == "back":
                    break

                cursor.execute("""
                    SELECT *
                    FROM Staff
                    WHERE Username = ?
                """, (username,))

                staff = cursor.fetchone()

                if staff:
                    edit_staff_details_checks(staff, cursor)
                    break

                print(
                    "\nNo staff member found with that username. "
                    "Please try again."
                )
                pause_screen()

        else:
            print(
                "\nInvalid search option. "
                "Please enter 'ID', 'Username' or 'back'."
            )
            pause_screen()


def edit_staff_details_checks(staff, cursor):
    # Display the existing staff record.
    print_as_table(cursor, [staff])

    staff_id = staff[0]

    print("\nPlease enter the staff data you wish to change.")
    print("If you do not wish to change something, just press Enter.")
    print("")

    while True:
        new_firstname = input(
            f"Update First Name [{staff[1]}]: "
        ).strip()

        if new_firstname == "":
            new_firstname = staff[1]
            break

        if not new_firstname.replace(" ", "").isalpha():
            print("First name can only contain letters.")
            continue

        break

    while True:
        new_lastname = input(
            f"Update Last Name [{staff[2]}]: "
        ).strip()

        if new_lastname == "":
            new_lastname = staff[2]
            break

        if not new_lastname.replace(" ", "").isalpha():
            print("Last name can only contain letters.")
            continue

        break

    while True:
        new_username = input(
            f"Update Username [{staff[3]}]: "
        ).strip()

        if new_username == "":
            new_username = staff[3]
            break

        cursor.execute("""
            SELECT StaffID
            FROM Staff
            WHERE Username = ?
              AND StaffID != ?
        """, (new_username, staff_id))

        if cursor.fetchone():
            print("This username already exists.")
        else:
            break

    while True:
        new_password = input(
            "Update Password (press Enter to keep current): "
        ).strip()

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
            print(
                "Password must contain at least one symbol "
                "(e.g., !, @, #, $)."
            )
            continue

        break

    while True:
        new_email = input(
            f"Update Email [{staff[5]}]: "
        ).strip()

        if new_email == "":
            new_email = staff[5]
            break

        if "@" not in new_email:
            print("Please enter a valid email address.")
            continue

        at_position = new_email.find("@")
        dot_position = new_email.rfind(".")

        if (
            at_position > 0
            and dot_position > at_position + 1
            and dot_position < len(new_email) - 1
        ):
            break

        print("Please enter a valid email address.")
    while True:
        current_phone = staff[6]

        new_phone = input(
            f"Update Phone Number [{current_phone or 'None'}]: "
        ).strip()

        # Pressing Enter keeps the existing phone number.
        if new_phone == "":
            new_phone = current_phone
            break

        # Allow the same common phone formatting as before.
        cleaned_number = (
            new_phone
            .replace("+", "")
            .replace("-", "")
            .replace(" ", "")
            .replace("(", "")
            .replace(")", "")
        )

        if 3 <= len(cleaned_number) <= 17 and cleaned_number.isdigit():
            break

        print("Please enter a valid phone number.")

    while True:
        new_position = input(
            f"Update Position "
            f"(Administrator/Moderator/Staff) [{staff[7]}]: "
        ).strip()

        if new_position == "":
            new_position = staff[7]
            break

        position_lookup = {
            "administrator": "Administrator",
            "moderator": "Moderator",
            "staff": "Staff"
        }

        new_position = position_lookup.get(new_position.lower())

        if new_position:
            break

        print(
            "Invalid position. Please enter "
            "Administrator, Moderator or Staff."
        )

    print("\nNew Staff Details:")
    print(f"First Name:  {new_firstname}")
    print(f"Last Name:   {new_lastname}")
    print(f"Username:    {new_username}")
    print(f"Email:       {new_email}")
    print(f"Phone:       {new_phone}")
    print(f"Position:    {new_position}")

    while True:
        confirm = input(
            "\nSave these changes? (yes/no): "
        ).strip().lower()

        if confirm == "yes":
            break

        if confirm == "no":
            print("\nChanges cancelled.")
            pause_screen()
            return

        print("Please enter 'yes' or 'no'.")

    try:
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
            staff_id
        ))

        conn.commit()

        print("\nStaff member updated successfully.")

    except sqlite3.Error as error:
        conn.rollback()
        print(f"\nUnable to update staff member: {error}")

    pause_screen()


def create_new_staff_member():
    clear_screen()
    print("-" * 60)
    print("                  Add New Staff Member")
    print("-" * 60)

    cursor.execute("""
        SELECT StaffID
        FROM Staff
        WHERE StaffID LIKE 'S%'
        ORDER BY CAST(SUBSTR(StaffID, 2) AS INTEGER) DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    if result is None:
        next_number = 1
    else:
        try:
            next_number = int(result[0][1:]) + 1
        except (ValueError, TypeError):
            next_number = 1

    staff_id = f"S{next_number:03d}"

    print(f"Staff ID: {staff_id}")
    while True:
        firstname = input("Enter First Name: ").strip()

        if firstname == "":
            print("First name cannot be blank.")
            continue

        if not firstname.replace(" ", "").isalpha():
            print("First name can only contain letters.")
            continue

        break

    while True:
        lastname = input("Enter Last Name: ").strip()

        if lastname == "":
            print("Last name cannot be blank.")
            continue

        if not lastname.replace(" ", "").isalpha():
            print("Last name can only contain letters.")
            continue

        break
    while True:
        username = input("Enter Username: ").strip()

        if username == "":
            print("Username cannot be blank.")
            continue

        cursor.execute("""
            SELECT StaffID
            FROM Staff
            WHERE Username = ?
        """, (username,))

        if cursor.fetchone():
            print("This username already exists.")
        else:
            break
    while True:
        password = input("Enter Password: ").strip()

        if password == "":
            print("Password cannot be blank.")
            continue

        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            continue

        if not any(char.isupper() for char in password):
            print("Password must contain at least one uppercase letter.")
            continue

        if not any(char.islower() for char in password):
            print("Password must contain at least one lowercase letter.")
            continue

        if not any(not char.isalnum() for char in password):
            print(
                "Password must contain at least one symbol "
                "(e.g., !, @, #, $)."
            )
            continue

        break

    while True:
        number = input("Enter Phone Number: ").strip()

        if number == "":
            print("Phone number cannot be blank.")
            continue

        cleaned_number = (
            number
            .replace("+", "")
            .replace("-", "")
            .replace(" ", "")
            .replace("(", "")
            .replace(")", "")
        )

        if 3 <= len(cleaned_number) <= 17 and cleaned_number.isdigit():
            break

        print("Please enter a valid phone number.")

    while True:
        email = input("Enter Email: ").strip()

        if email == "":
            print("Email cannot be blank.")
            continue

        if "@" not in email:
            print("Please enter a valid email address.")
            continue

        at_position = email.find("@")
        dot_position = email.rfind(".")

        if (
            at_position > 0
            and dot_position > at_position + 1
            and dot_position < len(email) - 1
        ):
            break

        print("Please enter a valid email address.")

    while True:
        position = input(
            "Enter Position (Staff/Moderator/Administrator): "
        ).strip()

        position_lookup = {
            "staff": "Staff",
            "moderator": "Moderator",
            "administrator": "Administrator"
        }

        position = position_lookup.get(position.lower())

        if position:
            break

        print(
            "Invalid position. Please enter "
            "Staff, Moderator or Administrator."
        )

    try:
        cursor.execute("""
            INSERT INTO Staff
            (
                StaffID,
                FirstName,
                LastName,
                Username,
                Password,
                Email,
                PhoneNumber,
                Position
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            staff_id,
            firstname,
            lastname,
            username,
            password,
            email,
            number,
            position
        ))

        conn.commit()

        print(
            f"\nNew staff member '{username}' "
            f"added successfully."
        )

    except sqlite3.Error as error:
        conn.rollback()
        print(f"\nUnable to create staff member: {error}")

    pause_screen()



def delete_staff_member():
    while True:
        clear_screen()
        print("-" * 60)
        print("                  Delete Staff Member")
        print("-" * 60)

        search = input(
            "(type 'back' to go back)\n"
            "Find Staff Member to Delete by ID or Username: "
        ).strip().lower()

        if search == "back":
            break
        if search == "id":
            while True:
                staff_id = input(
                    "Enter Staff ID (or type 'back'): "
                ).strip().upper()

                if staff_id.lower() == "back":
                    break

                cursor.execute("""
                    SELECT *
                    FROM Staff
                    WHERE StaffID = ?
                """, (staff_id,))

                staff = cursor.fetchone()

                if not staff:
                    print(
                        "\nNo staff member found with that ID. "
                        "Please try again."
                    )
                    pause_screen()
                    continue

                print("\nStaff member found:")
                print_as_table(cursor, [staff])

                while True:
                    confirm = input(
                        "\nAre you sure you want to delete this "
                        "staff member? (yes/no): "
                    ).strip().lower()

                    if confirm == "no":
                        print("\nDeletion cancelled.")
                        pause_screen()
                        break

                    if confirm != "yes":
                        print("Please enter 'yes' or 'no'.")
                        continue

                    try:
                        # Remove related tournament records first.
                        cursor.execute("""
                            DELETE FROM TournamentStaff
                            WHERE StaffID = ?
                        """, (staff_id,))

                        # Then remove the staff member.
                        cursor.execute("""
                            DELETE FROM Staff
                            WHERE StaffID = ?
                        """, (staff_id,))

                        conn.commit()

                        print("\nStaff member deleted successfully.")

                    except sqlite3.Error as error:
                        conn.rollback()
                        print(
                            f"\nUnable to delete staff member: {error}"
                        )

                    pause_screen()
                    break

                # Return to ID/Username selection.
                break
        elif search == "username":
            while True:
                username = input(
                    "Enter Staff Username (or type 'back'): "
                ).strip()

                if username.lower() == "back":
                    break

                cursor.execute("""
                    SELECT *
                    FROM Staff
                    WHERE Username = ?
                """, (username,))

                staff = cursor.fetchone()

                if not staff:
                    print(
                        "\nNo staff member found with that username. "
                        "Please try again."
                    )
                    pause_screen()
                    continue

                staff_id = staff[0]

                print("\nStaff member found:")
                print_as_table(cursor, [staff])

                while True:
                    confirm = input(
                        "\nAre you sure you want to delete this "
                        "staff member? (yes/no): "
                    ).strip().lower()

                    if confirm == "no":
                        print("\nDeletion cancelled.")
                        pause_screen()
                        break

                    if confirm != "yes":
                        print("Please enter 'yes' or 'no'.")
                        continue

                    try:
                        # Use StaffID rather than username so the
                        # correct record is always deleted.
                        cursor.execute("""
                            DELETE FROM TournamentStaff
                            WHERE StaffID = ?
                        """, (staff_id,))

                        cursor.execute("""
                            DELETE FROM Staff
                            WHERE StaffID = ?
                        """, (staff_id,))

                        conn.commit()

                        print("\nStaff member deleted successfully.")

                    except sqlite3.Error as error:
                        conn.rollback()
                        print(
                            f"\nUnable to delete staff member: {error}"
                        )

                    pause_screen()
                    break

                break

        else:
            print(
                "\nInvalid search option. "
                "Please enter 'ID', 'Username' or 'back'."
            )
            pause_screen()




def generate_analytical_reports():
    while True:
        clear_screen()
        print("-" * 90)
        print("                     Generate Analytical Reports")
        print("-" * 90)
        print("  [1] Display the players with the largest card collections.")
        print("  [2] Display the most commonly owned card.")
        print("  [3] Display cards ordered by rarity.")
        print("  [4] Calculate the maximum and minimum HP.")
        print("  [5] Display total players/cards/decks/tournaments/registrations/matches.")
        print("  [0] Back to main menu")
        print("")

        choice = input("Select an option: ").strip()
        if choice == "0":
            break
        elif choice == "1":
            clear_screen()
            print("-" * 90)
            print("                 Players With The Largest Collections")
            print("-" * 90)

            try:
                cursor.execute("""
                    SELECT
                        Player.PlayerID,
                        Player.Username,
                        SUM(PlayerCollection.Quantity) AS "Number of Cards"
                    FROM Player
                    JOIN PlayerCollection
                        ON PlayerCollection.PlayerID = Player.PlayerID
                    GROUP BY Player.PlayerID, Player.Username
                    ORDER BY SUM(PlayerCollection.Quantity) DESC
                    LIMIT 10
                """)

                players = cursor.fetchall()

                if players:
                    print_as_table(cursor, players)
                else:
                    print("\nNo players with card collections were found.")

            except sqlite3.Error as error:
                print(f"\nUnable to generate report: {error}")

            pause_screen()
            print("-" * 90)
            print("                    Most Commonly Owned Cards")
            print("-" * 90)

            try:
                cursor.execute("""
                    SELECT
                        Card.CardID,
                        Card.CardName,
                        Card.CardType,
                        Card.CardNumber,
                        Card.Rarity,
                        SUM(PlayerCollection.Quantity) AS "Total Owned"
                    FROM Card
                    JOIN PlayerCollection
                        ON PlayerCollection.CardID = Card.CardID
                    GROUP BY
                        Card.CardID,
                        Card.CardName,
                        Card.CardType,
                        Card.CardNumber,
                        Card.Rarity
                    ORDER BY SUM(PlayerCollection.Quantity) DESC,
                             Card.CardName ASC
                    LIMIT 10
                """)

                cards = cursor.fetchall()

                if cards:
                    print_as_table(cursor, cards)
                else:
                    print("\nNo owned cards found.")

            except sqlite3.Error as error:
                print(f"\nUnable to generate report: {error}")
            print("")
            print("-" * 90)
            print("                 Most Commonly Owned Creature Cards")
            print("-" * 90)

            try:
                cursor.execute("""
                    SELECT
                        Card.CardID,
                        Card.CardName,
                        Card.CardNumber,
                        Card.Rarity,
                        SUM(PlayerCollection.Quantity) AS "Total Owned"
                    FROM Card
                    JOIN PlayerCollection
                        ON PlayerCollection.CardID = Card.CardID
                    WHERE Card.CardType = 'Creature Card'
                    GROUP BY
                        Card.CardID,
                        Card.CardName,
                        Card.CardNumber,
                        Card.Rarity
                    ORDER BY SUM(PlayerCollection.Quantity) DESC,
                             Card.CardName ASC
                    LIMIT 10
                """)

                cards = cursor.fetchall()

                if cards:
                    print_as_table(cursor, cards)
                else:
                    print("\nNo owned Creature Cards found.")

            except sqlite3.Error as error:
                print(f"\nUnable to generate report: {error}")
            print("")
            print("-" * 90)
            print("                  Most Commonly Owned Trainer Cards")
            print("-" * 90)

            try:
                cursor.execute("""
                    SELECT
                        Card.CardID,
                        Card.CardName,
                        Card.CardNumber,
                        Card.Rarity,
                        SUM(PlayerCollection.Quantity) AS "Total Owned"
                    FROM Card
                    JOIN PlayerCollection
                        ON PlayerCollection.CardID = Card.CardID
                    WHERE Card.CardType = 'Trainer Card'
                    GROUP BY
                        Card.CardID,
                        Card.CardName,
                        Card.CardNumber,
                        Card.Rarity
                    ORDER BY SUM(PlayerCollection.Quantity) DESC,
                             Card.CardName ASC
                    LIMIT 10
                """)

                cards = cursor.fetchall()

                if cards:
                    print_as_table(cursor, cards)
                else:
                    print("\nNo owned Trainer Cards found.")

            except sqlite3.Error as error:
                print(f"\nUnable to generate report: {error}")
            print("")
            print("-" * 90)
            print("                   Most Commonly Owned Energy Cards")
            print("-" * 90)

            try:
                cursor.execute("""
                    SELECT
                        Card.CardID,
                        Card.CardName,
                        Card.CardNumber,
                        Card.Rarity,
                        SUM(PlayerCollection.Quantity) AS "Total Owned"
                    FROM Card
                    JOIN PlayerCollection
                        ON PlayerCollection.CardID = Card.CardID
                    WHERE Card.CardType = 'Energy Card'
                    GROUP BY
                        Card.CardID,
                        Card.CardName,
                        Card.CardNumber,
                        Card.Rarity
                    ORDER BY SUM(PlayerCollection.Quantity) DESC,
                             Card.CardName ASC
                    LIMIT 10
                """)

                cards = cursor.fetchall()

                if cards:
                    print_as_table(cursor, cards)
                else:
                    print("\nNo owned Energy Cards found.")

            except sqlite3.Error as error:
                print(f"\nUnable to generate report: {error}")

            pause_screen()
        elif choice == "3":
            clear_screen()
            print("-" * 90)
            print("                       Cards Ordered By Rarity")
            print("-" * 90)

            try:
                cursor.execute("""
                    SELECT *
                    FROM Card
                    ORDER BY
                        CASE
                            WHEN UPPER(Rarity) LIKE '%SPECIAL ILLUSTRATION%' THEN 1
                            WHEN UPPER(Rarity) LIKE '%ILLUSTRATION RARE%' THEN 2
                            WHEN UPPER(Rarity) LIKE '%HYPER RARE%' THEN 3
                            WHEN UPPER(Rarity) LIKE '%ULTRA RARE%' THEN 4
                            WHEN UPPER(Rarity) LIKE '%ACE SPEC%' THEN 5
                            WHEN UPPER(Rarity) LIKE '%DOUBLE RARE%' THEN 6
                            WHEN UPPER(Rarity) LIKE '%RARE HOLO%' THEN 7
                            WHEN UPPER(Rarity) LIKE '%RARE%' THEN 8
                            WHEN UPPER(Rarity) LIKE '%UNCOMMON%' THEN 9
                            WHEN UPPER(Rarity) LIKE '%COMMON%' THEN 10
                            ELSE 11
                        END ASC,
                        CardName ASC
                """)

                cards = cursor.fetchall()

                if cards:
                    print_as_table(cursor, cards)
                else:
                    print("\nNo cards found.")

            except sqlite3.Error as error:
                print(f"\nUnable to generate report: {error}")

            pause_screen()
        elif choice == "4":
            clear_screen()
            print("-" * 90)
            print("                    Maximum and Minimum HP")
            print("-" * 90)

            try:
                # Highest HP
                cursor.execute("""
                    SELECT
                        Card.CardID,
                        Card.CardName,
                        Card.CardNumber,
                        Card.Rarity,
                        CreatureCard.HP
                    FROM Card
                    JOIN CreatureCard
                        ON Card.CardID = CreatureCard.CardID
                    ORDER BY CreatureCard.HP DESC
                    LIMIT 1
                """)

                highesthp = cursor.fetchone()

                # Lowest HP
                cursor.execute("""
                    SELECT
                        Card.CardID,
                        Card.CardName,
                        Card.CardNumber,
                        Card.Rarity,
                        CreatureCard.HP
                    FROM Card
                    JOIN CreatureCard
                        ON Card.CardID = CreatureCard.CardID
                    ORDER BY CreatureCard.HP ASC
                    LIMIT 1
                """)

                lowesthp = cursor.fetchone()

                if highesthp and lowesthp:
                    print("Card with the Highest HP:")
                    print_as_table(cursor, [highesthp])

                    print("\nCard with the Lowest HP:")
                    print_as_table(cursor, [lowesthp])

                else:
                    print("\nNo Creature Cards with HP were found.")

            except sqlite3.Error as error:
                print(f"\nUnable to generate HP report: {error}")

            pause_screen()
        elif choice == "5":
            clear_screen()
            print("-" * 60)
            print("                     System Statistics")
            print("-" * 60)

            try:
                cursor.execute("SELECT COUNT(*) FROM Player")
                players = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM Card")
                cards = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM Deck")
                decks = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM Tournament")
                tournaments = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM RegistrationList")
                registrations = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM Matches
                    WHERE MatchStatus = 'Finished'
                """)
                matches = cursor.fetchone()[0]
                stat_template = "  {:<35} : {}"

                print("")
                print(stat_template.format(
                    "Total Players", players
                ))
                print(stat_template.format(
                    "Total Cards", cards
                ))
                print(stat_template.format(
                    "Total Decks", decks
                ))
                print(stat_template.format(
                    "Total Tournaments", tournaments
                ))
                print(stat_template.format(
                    "Total Tournament Registrations", registrations
                ))
                print(stat_template.format(
                    "Total Matches Played", matches
                ))

                print("-" * 60)

            except sqlite3.Error as error:
                print(f"\nUnable to generate statistics: {error}")
            pause_screen()
        else:
            print("\nInvalid option selected.")
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
                        register_remove_players()
                    elif manage_tournaments_option == "3":
                        view_venues()
                    elif manage_tournaments_option == "4":
                        if user_position in ['Moderator', 'Administrator']:
                            edit_tournament_details()
                        else: 
                            continue
                    elif manage_tournaments_option == "5":
                        if user_position in ['Moderator', 'Administrator']:
                            create_new_tournament()
                        else: 
                            continue
                    elif manage_tournaments_option == "6":
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
