    • Edit player details. 
    • Add/delete player accounts. 
    • Display all tournaments a player has entered. 
    • Show all decks owned by a player. 
    • Count the number of decks a player owns. 
    • Calculate the total number of cards owned by a player. 
    • Display the player's most valuable deck (if you store card values). 


SELECT * FROM Player WHERE Username = ? 


sql_command = """
UPDATE player 
SET name = ?, age = ?, position = ? 
WHERE player_id = ?;
"""

# 4. Combine the command with the inputs in a tuple
# The order must exactly match the '?' placeholders in the SQL string
user_data = (new_name, new_age, new_position, target_id)

try:
    # 5. Execute and commit the changes
    cursor.execute(sql_command, user_data)
    conn.commit()
    print(f"Player {target_id} successfully updated!")
    
except sqlite3.Error as error:
    print("Failed to update data:", error)
    conn.rollback()

finally:
    # 6. Clean up connections
    cursor.close()
    conn.close()

1. Staff Menu (Player & Event Management)Staff deal with the daily users and tournament coordination.
Manage Players: Search players, view player details, see their decks, or check entered tournaments.
Manage Tournaments: Register/remove players, view upcoming tournaments, or count registrants.
Manage Matches: Log match results, create matches, or view a player's match history.
Log Out

2. Moderator Menu (Game Integrity & Content)Moderators ensure the card data itself is accurate and clean.
All Staff Options (Access to the Staff menu items).
Manage Cards: Search cards, add new cards, or edit existing card details (HP, Element, Rarity).
Manage Decks: View cards in a deck, or check which decks contain a specific card.
Log Out

3. Admin Menu (Full System & Analytics)
Admins handle high-level data deletion, staff accounts, and business reports.
All Moderator & Staff Options (Access to everything).
Destructive Actions: Delete player accounts, delete cards, or delete tournaments.
System Reports: View top statistics (Largest card collections, rarest cards, most common cards, system totals).
Manage Staff: Add, edit, or delete staff user accounts.
Log Out

