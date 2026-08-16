from re import match
import sqlite3
import sys

from concurrent.interpreters import create

conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")



def login():
    global user_position, user_firstname
    print("""
----------------------Pokemon TGC Administrator System---------------------- 
""")
    for i in range(3):
        staff_user = input("Enter Username:")
        staff_password = input("Enter Password:")

        cursor.execute("SELECT FirstName, Position FROM Staff WHERE Username = ? AND Password = ?", (staff_user, staff_password))
        user = cursor.fetchone()
        if user:
            user_position = user[1]
            user_firstname = user[0]
            print("Login successful!")
            print(f"Welcome {user_firstname}!  Role: {user_position}")
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



def manage_players():
    if user_position == "Staff":
        print("""
    - View all Player data (1)
    - Search for a specific player (2)
    - Edit Player Details (3)
    - Add new Player (4)""")
        player_option = input(" ")
        return player_option
    elif user_position == "Moderator" or user_position == "Administrator":
        print("""
    - View all Player data (1)
    - Search for a specific player (2)
    - Edit Player Details (3)
    - Add new Player (4)""")
        player_option = input(" ")
        return player_option

    • Provide details of a particular player. 
    • Search for players by username or email. 
    • Edit player details. 
    • Add/delete player accounts. 
    • Display all tournaments a player has entered. 
    • Show all decks owned by a player. 
    • Count the number of decks a player owns. 
    • Calculate the total number of cards owned by a player. 
    • Display the player's most valuable deck (if you store card values). 

def manage_tournaments():
    if user_position == "Staff":
        print("""
    - View tournament details (1)
    - Edit tournament details (2)
    - Manage tournament registeration (3)""")
        tournament_option = input(" ")
        return tournament_option
    elif user_position == "Moderator" or user_position == "Administrator":
        print("""
    - View tournament details (1)
    - Edit tournament details (2)
    - Manage tournament registeration (3)
    - Create a new tournament (4)
    - Cancel a tournament (5)""")
        tournament_option = input(" ")
        return tournament_option

    • Display details of a tournament. 
    • Register/remove players from tournaments. 

    • Count the number of players registered for each tournament. 

    • Display all upcoming tournaments. 
    • Display tournaments ordered by date. 
    • Add/edit/delete tournaments. 

def manage_matches():
    if user_position == "Staff":
        print("""
    - View match details
    - view all matches in a tournament
    - View all matches player by a Player
        """)

    tournament match details
        create edit delete match
        view details of a specific match
        view all matches ina tournament
        view winners of all matches ina  tournament

    • Create/edit/delete matches. 
    • Display details of a specific match
    • Display all matches in a tournament. 
    • Display all matches played by a selected player. 
    • Display the winner of each match. 
    • Count the total number of matches in a tournament. 

def main():
    login()
    if not login:
        conn.close()
        sys.exit()
    menu_option = main_menu()
    if menu_option == "0":
        print("Logging out...")
        conn.close()
        sys.exit()
    elif menu_option == "1":
        pass


main()