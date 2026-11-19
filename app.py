# This file's purpose is to start Flask and to handle web requests.
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_courses(connection):
    cursor = connection.execute("""
        SELECT courses.course_id,
               courses.course_code,
               semesters.name
        FROM courses
        JOIN semesters
            ON courses.semester_id = semesters.semester_id;
    """)
    return cursor.fetchall()

def get_semesters(connection):
    cursor = connection.execute(
        "SELECT semester_id, name FROM semesters"
    )
    return cursor.fetchall()

def get_assignments(connection):
    cursor = connection.execute("""
        SELECT assignments.title,
               assignments.due_date,
               courses.course_code,
               assignments.estimated_hours,
               assignments.importance,
               assignments.completed,
               assignments.assignment_id
        FROM assignments
        JOIN courses
            ON assignments.course_id = courses.course_id
        ORDER BY assignments.due_date;
    """)
    return cursor.fetchall()

@app.route("/api/assignments", methods=["GET", "POST"])
def api_assignments():
    connection = sqlite3.connect("coursepilot.db")
    connection.execute("PRAGMA foreign_keys = ON")

    if request.method == "POST":
        data = request.get_json()
        title = data.get("title", "").strip()
        due_date = data.get("due_date", "").strip()
        course_id = data.get("course_id")
        estimated_hours = data.get("estimated_hours")
        importance = data.get("importance")

        if not title or not due_date:
            connection.close()
            return jsonify({"error": "Title and due date are required."}), 400

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            connection.close()
            return jsonify({
                "error": "Due date must be a valid date."
            }), 400

        try:
            course_id = int(course_id)
            estimated_hours = float(estimated_hours)
            importance = int(importance)
            if estimated_hours <= 0:
                connection.close()
                return jsonify({
                    "error": "Estimated hours must be greater than zero."
                }), 400

            if importance < 1 or importance > 5:
                connection.close()
                return jsonify({
                    "error": "Importance must be between 1 and 5."
                }), 400
        except (TypeError, ValueError):
            connection.close()
            return jsonify({
                "error": "Assignment values are invalid."
            }), 400

        cursor = connection.execute(
            "SELECT course_id FROM courses WHERE course_id = ?",
            (course_id,)
        )
        if cursor.fetchone() is None:
            connection.close()
            return jsonify({
                "error": "The selected course does not exist."
            }), 400

        connection.execute(
            """
            INSERT INTO assignments (course_id, title, due_date, estimated_hours, importance)
            VALUES (?, ?, ?, ?, ?)
            """,
            (course_id, title, due_date, estimated_hours, importance)
        )
        connection.commit()
        connection.close()
        return jsonify({"message": "Assignment created."}), 201
    
    assignments = get_assignments(connection)
    connection.close()

    return jsonify([
        {
            "title": assignment[0],
            "due_date": assignment[1],
            "course_code": assignment[2],
            "estimated_hours": assignment[3],
            "importance": assignment[4],
            "completed": bool(assignment[5]),
            "assignment_id": assignment[6]
        }
        for assignment in assignments
    ])

@app.route("/", methods=["GET", "POST"])
def home():
    course_error = None
    semester_error = None
    assignment_error = None
    connection = sqlite3.connect("coursepilot.db")
    connection.execute("PRAGMA foreign_keys = ON")
    if request.method == "POST":
        action = request.form.get("action")
        # Add course section
        if action == "add_course":

            course_code = request.form["course_code"].strip()
            course_name = request.form["course_name"].strip()
            semester_id = None
            try:
                semester_id = int(request.form["semester_id"])
            except ValueError:
                course_error = "Please select a valid semester."

            if semester_id is not None:
                cursor = connection.execute(
                    "SELECT semester_id FROM semesters WHERE semester_id = ?",
                    (semester_id,)
                )
                semester = cursor.fetchone()
                if semester is None:
                    course_error = "The selected semester does not exist."

            print("Course Code:", course_code)
            print("Course Name:", course_name)
            print("Semester ID:", semester_id)

            if not course_code or not course_name:
                course_error = "Course code and course name are required."
            if course_error is None:
                print("Course information is valid.")

                connection.execute(
                    """
                    INSERT INTO courses (semester_id, course_code, course_name)
                    VALUES (?, ?, ?)
                    """,
                    (semester_id, course_code, course_name)
                )
                connection.commit()
        # Add semester section
        elif action == "add_semester":
            semester_name = request.form["semester_name"].strip()
            start_date = request.form["start_date"].strip()
            end_date = request.form["end_date"].strip()
            print(f"Semester Name: {semester_name}")
            print(f"Start Date: {start_date}")
            print(f"End Date: {end_date}")
            if not semester_name:
                semester_error = "Semester name is required."
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                end = datetime.strptime(end_date, "%Y-%m-%d").date()
                if end <= start:
                    semester_error = "End date must be after start date."
            except ValueError:
                semester_error = "Please enter valid dates."

            if semester_error is None:
                connection.execute(
                    """
                    INSERT INTO semesters (name, start_date, end_date)
                    VALUES (?, ?, ?)
                    """,
                    (semester_name, start_date, end_date)
                )
                connection.commit()
            # Add assignment section
        elif action == "add_assignment":
            title = request.form["assignment_title"].strip()
            due_date = request.form["assignment_due_date"].strip()
            course_id = request.form["assignment_course_id"]
            estimated_hours = request.form["estimated_hours"]
            importance = request.form["importance"]
            if not title:
                assignment_error = "Assignment title is required."
            try:
                course_id = int(course_id)
                estimated_hours = float(estimated_hours)
                importance = int(importance)
                if estimated_hours <= 0:
                    assignment_error = "Estimated hours must be greater than zero."
                if importance < 1 or importance > 5:
                    assignment_error = "Importance must be between 1 and 5."
            except ValueError:
                assignment_error = "Please enter valid assignment information."
            if assignment_error is None:
                connection.execute(
                    """
                    INSERT INTO assignments (course_id, title, due_date, estimated_hours, importance)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (course_id, title, due_date, estimated_hours, importance)
                )
                connection.commit()

        elif action == "toggle_assignment":
            assignment_id = request.form["assignment_id"]
            connection.execute(
                """
                UPDATE assignments
                SET completed = CASE completed
                    WHEN 0 THEN 1
                    ELSE 0
                END
                WHERE assignment_id = ?
                """,
                (assignment_id,)
            )
            connection.commit()
    app_name = "CoursePilot"
    
    courses = get_courses(connection)
    semesters = get_semesters(connection)
    assignments = get_assignments(connection)

    connection.close()

    return render_template(
        "index.html",
        name=app_name,
        courses=courses,
        semesters=semesters,
        assignments=assignments,
        course_error=course_error,
        semester_error=semester_error,
        assignment_error=assignment_error
    )