import sqlite3

connection = sqlite3.connect("coursepilot.db")

with open("schema.sql", "r") as file:
    schema = file.read()

connection.executescript(schema)

connection.close()

print("CoursePilot database initialized successfully!")