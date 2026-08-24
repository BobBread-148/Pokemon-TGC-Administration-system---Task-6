from ast import Try
import sqlite3
import sys
import os
import datetime
from datetime import date

sqlite3.register_adapter(datetime.date, lambda val: val.isoformat())
sqlite3.register_adapter(datetime.datetime, lambda val: val.isoformat())


conn = sqlite3.connect("PokemonOnlineTCG_Database.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")










#matches id, player1 id, player 1 username, player 2 id, player 2 user, winner, matchstatus, round
cursor.execute("""
--matches id, player1 id, player 1 username, player 2 id, player 2 user, winner, matchstatus, round
SELECT m.MatchesID, m.Player1, p1.Username, m.Player2, p2.Username, m.Winner, p3.username m.MatchStatus, m.Round
FROM Matches 
JOIN RegistrationList ON Matches.TournamentID = RegistrationList.TournamentID
JOIN Player ON Player.PlayerID = RegistrationList.PlayerID
WHERE Matches.TournamentID = 'T001';
""") 