import sqlite3
import sys

conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

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

    print("=" * sum(col_widths))
    print(format_template.format(*headers))
    print("-" * sum(col_widths))
    print(format_template.format(*row_strings))
    print("=" * sum(col_widths))


def login():
    global user_position, user_firstname
    print("----------------------Pokemon TGC Administrator System---------------------- ")
    for i in range(3):
        staff_user = input("Enter Username:")
        staff_password = input("Enter Password:")

        cursor.execute("SELECT FirstName, Position FROM Staff WHERE Username = ? AND Password = ?", (staff_user, staff_password))
        user = cursor.fetchone()
        if user:
            user_position = user[1]
            user_firstname = user[0]
            print("Login successful!")
            print(f"Welcome {user_firstname}.  Role: {user_position}")
            return True
        else:
            print("Invalid username or password. Please try again.")
    print("Too many failed attempts. Access denied.")
    return False

def main_menu():
    global menu_option
    if user_position == "Administrator":
        print("""
    What would you like to do:
    - Manage Players (1)
    - Manage Tournaments (2)
    - Manage Matches (3)
    - Manage Cards (4)
    - Manage Decks (5)
    - Manage Staff (6)
    - Analytical Reports (7)
    - Log out (0)""")
        menu_option = input(" ")

    elif user_position == "Moderator":
        print("""
    What would you like to do:
    - Manage Players (1)
    - Manage Tournaments (2)
    - Manage Matches (3)
    - Manage Cards (4)
    - Manage Decks (5)
    - Log out (0)""")
        menu_option = input(" ")

    elif user_position == "Staff":
        print("""
    What would you like to do:
    - Manage Players (1)
    - Manage Tournaments (2)
    - Manage Matches (3)
    - Log out (0)""")
        menu_option = input(" ")

    return menu_option

def log_out():
    conn.commit()
    conn.close()
    sys.exit("Logging out... Goodbye!")

def manage_players():
    if user_position == "Administrator" or user_position == "Moderator":
        print("""
    - View account details (1)
    - Edit account details (3)
    - View Player stats (2)
    - Add new Player (4)
    - Delete Player (5)""")
        option = input(" ")
        return option

def view_account_details():
    while True:
        search = input("Would you like to search for player by ID, Username or Email? \n(or type 'back' to return to the manage players menu)").lower().strip()

        if search == "id":
            id_input = input("Enter Player ID:")
            cursor.execute("SELECT * FROM Player WHERE PlayerID = ?", (id_input,))
            player = cursor.fetchone()
            print_as_table(cursor, player)


        elif search == "username":
            username = input("Enter Player Username:")
            cursor.execute("SELECT * FROM Player WHERE Username = ?", (username,))
            player = cursor.fetchone()
            print_as_table(cursor, player)

        elif search == "email":
            email = input("Enter Player Email:")
            cursor.execute("SELECT * FROM Player WHERE Email = ?", (email,))
            player = cursor.fetchone()
            print_as_table(cursor, player)

        elif search == "back":
            break

        else:
            print("Invalid search option. Please enter 'ID', 'Username', or 'Email'.")

    
def main():
    if login():
        while True:
            menu_option = main_menu()
            if menu_option == "0":
                log_out()
            elif menu_option == "1":
                while True: 
                    manage_players_option = manage_players()
                    if manage_players_option == "1":
                        view_account_details()
                    else:
                        break


main()