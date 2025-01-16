import sqlite3 as sql

conn = sql.connect("server.db")
cur = conn.cursor()