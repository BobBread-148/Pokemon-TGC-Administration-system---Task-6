import sqlite3
import sys

conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")



def login():
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

def main():
    login()
    if not login:
        conn.close()
        sys.exit()

main()