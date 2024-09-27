import sqlite3
connection = sqlite3.connect('inquiri.db')
def criaBanco():
    with open('schema.sql') as f:
       connection.executescript(f.read())


criaBanco()