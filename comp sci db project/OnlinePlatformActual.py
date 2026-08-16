import sqlite3
import sys
import os
from datetime import date

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


def print_as_table(cursor, row):
    if row is None:
        print("No data found.")
        return
    
    headers = []
    for i in cursor.description:
        headers.append(i[0])

    row_strings = []
    for i in row:
        row_strings.append(str(i))

    col_widths = []
    for h,r in zip(headers, row_strings):
        col_widths.append(max(len(h), len(r)) + 4)

    format_template = ""
    for i in col_widths:
        format_template += f"{{:<{i}}}"

    print("")
    print("=" * sum(col_widths))
    print(format_template.format(*headers))
    print("-" * sum(col_widths))
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
                    print_as_table(cursor, player)
                    playerid = player[0]
                    print("Please enter the player data you wish to change. If you do not wish to change anything in the specific column, just click enter.")
                    new_username = input("Update username: ").strip()
                    new_dob = input("Update Date of Birth (YYYY-MM-DD): ").strip()
                    new_number = input("Update Phone Number: ").strip()
                    new_email = input("Update Email: ").strip()
                    
                    # Convert blank string entries into clean database NULL values if skipped or empty
                    db_number = new_number if new_number != "" else None
                    db_old_number = player[4] if player[4] is not None else None

                    cursor.execute(
                        """
                        UPDATE Player 
                        SET Username = ?, DateOfBirth = ?, PhoneNumber = ?, Email = ? 
                        WHERE PlayerID = ?
                        """, 
                        (
                            new_username if new_username else player[1], 
                            new_dob if new_dob else player[3], 
                            db_number if new_number else db_old_number, 
                            new_email if new_email else player[5],  
                            playerid
                        )
                    )
                    conn.commit()
                    print("Player details updated successfully.")
                    pause_screen()
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
                    print_as_table(cursor, player)
                    playerid = player[0]
                    print("Please enter the player data you wish to change. If you do not wish to change anything in the specific column, just click enter.")
                    new_username = input("Update username: ").strip()
                    new_dob = input("Update Date of Birth (YYYY-MM-DD): ").strip()
                    new_number = input("Update Phone Number: ").strip()
                    # Convert blank string entries into clean database NULL values if skipped or empty
                    db_number = new_number if new_number != "" else None
                    db_old_number = player[4] if player[4] is not None else None

                    cursor.execute(
                        """
                        UPDATE Player 
                        SET Username = ?, DateOfBirth = ?, PhoneNumber = ?, Email = ? 
                        WHERE PlayerID = ?
                        """, 
                        (
                            new_username if new_username else player[1], 
                            new_dob if new_dob else player[3], 
                            db_number if new_number else db_old_number, 
                            new_email if new_email else player[5],  
                            playerid
                        )
                    )
                    conn.commit()
                    print("Player details updated successfully.")
                    pause_screen()
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
                    print_as_table(cursor, player)
                    playerid = player[0]
                    print("Please enter the player data you wish to change. If you do not wish to change anything in the specific column, just click enter.")
                    new_username = input("Update username: ").strip()
                    new_dob = input("Update Date of Birth (YYYY-MM-DD): ").strip()
                    new_number = input("Update Phone Number: ").strip()
                    new_email = input("Update Email: ").strip()
                    
                    db_number = new_number if new_number != "" else None
                    db_old_number = player[4] if player[4] is not None else None

                    cursor.execute(
                        """
                        UPDATE Player 
                        SET Username = ?, DateOfBirth = ?, PhoneNumber = ?, Email = ? 
                        WHERE PlayerID = ?
                        """, 
                        (
                            new_username if new_username else player[1], 
                            new_dob if new_dob else player[3], 
                            db_number if new_number else db_old_number, 
                            new_email if new_email else player[5],  
                            playerid
                        )
                    )
                    conn.commit()
                    print("Player details updated successfully.")
                    pause_screen()
                    break
                else:
                    print("No player found with that username. Please try again.")
                    pause_screen()
        else:
            print("Invalid search option. Please enter 'ID' or 'Username'.")
            pause_screen()
        clear_screen()


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

    print(f"Generated Player ID: {player_id}")
    print(f"Registration Date  : {date_joined}\n")

    username = input("Enter Username: ").strip()
    dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
    number = input("Enter Phone Number (Press Enter to skip): ").strip()
    email = input("Enter Email: ").strip()

    db_number = number if number != "" else None

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
                        cursor.execute("DELETE FROM Player WHERE PlayerID = ?", (id_input,))
                        conn.commit()
                        print(f"Player '{player[1]}' deleted successfully.")
                        pause_screen()
                        break
                    else:
                        print("Deletion cancelled.")
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
                    confirm = input(f"Are you sure you want to delete player '{player[1]}'? (yes/no): ").lower().strip()
                    if confirm == "yes":
                        cursor.execute("DELETE FROM Player WHERE Username = ?", (username,))
                        conn.commit()
                        print(f"Player '{player[1]}' deleted successfully.")
                        pause_screen()
                        break
                    else:
                        print("Deletion cancelled.")
                        pause_screen()
                        break
                else:
                    print("No player found with that username. Please try again.")
                    pause_screen()

        else:
            print("Invalid search option. Please enter 'ID' or 'Username'.")
            pause_screen()
        clear_screen()


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
            else:
                print("Invalid option selected, please try again.")
                pause_screen()


main()
