import sqlite3

db = sqlite3.connect('database/database.sqlite')
db.row_factory = sqlite3.Row

with open('database/schema.sql') as f:
    db.executescript(f.read())

