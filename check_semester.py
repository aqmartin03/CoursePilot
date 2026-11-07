import sqlite3

semester_id = 1

connection = sqlite3.connect("coursepilot.db")

cursor = connection.execute(
    "SELECT semester_id FROM semesters WHERE semester_id = ?",
    (semester_id,)
)

semester = cursor.fetchone()

connection.close()

if semester is None:
    print("Semester does not exist!")
else:
    print("Semester exists!")