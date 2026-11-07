# This file's purpose is to start Flask and to handle web requests.
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    error_message = None
    connection = sqlite3.connect("coursepilot.db")
    connection.execute("PRAGMA foreign_keys = ON")
    if request.method == "POST":
        course_code = request.form["course_code"].strip()
        course_name = request.form["course_name"].strip()
        semester_id = None
        try:
            semester_id = int(request.form["semester_id"])
        except ValueError:
            error_message = "Please select a valid semester."

        if semester_id is not None:
            cursor = connection.execute(
                "SELECT semester_id FROM semesters WHERE semester_id = ?",
                (semester_id,)
            )
            semester = cursor.fetchone()
            if semester is None:
                error_message = "The selected semester does not exist."

        print("Course Code:", course_code)
        print("Course Name:", course_name)
        print("Semester ID:", semester_id)

        if not course_code or not course_name:
            error_message = "Course code and course name are required."
        if error_message is None:
            print("Course information is valid.")

            connection.execute(
                """
                INSERT INTO courses (semester_id, course_code, course_name)
                VALUES (?, ?, ?)
                """,
                (semester_id, course_code, course_name)
            )
            connection.commit()

    app_name = "CoursePilot"

    cursor = connection.execute("""
        SELECT courses.course_code, semesters.name
        FROM courses
        JOIN semesters
           ON courses.semester_id = semesters.semester_id;
    """)

    rows = cursor.fetchall()

    semester_cursor = connection.execute(
        "SELECT semester_id, name FROM semesters"
    )
    semesters = semester_cursor.fetchall()

    connection.close()

    courses = rows
    return render_template(
        "index.html",
        name=app_name,
        courses=courses,
        semesters=semesters,
        error_message=error_message
    )

