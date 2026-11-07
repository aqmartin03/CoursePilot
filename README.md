# CoursePilot

**Navigate your coursework with confidence.**

## Project Overview

CoursePilot is a web application designed to help college students organize their courses, manage assignments, and prioritize their academic workload.

The goal is to create a free, practical assignment planner that helps students determine which assignments deserve their attention first.

CoursePilot is being developed as part of my CSE 199R project at Brigham Young University–Idaho.

## Purpose

I wanted to create a tool that I could use to organize my own coursework without relying on a paid productivity application.

I also wanted to strengthen my software development skills by building a full-stack web application using Python, Flask, SQL, HTML, and CSS.

This project gives me hands-on experience with relational databases, backend development, user input validation, and eventually algorithm design.

## Current Features

- Display courses and their associated semesters.
- Add new courses through a web form.
- Store course information in a SQLite database.
- Dynamically populate semester options from the database.
- Validate course codes, names, and semester IDs.
- Display error messages for invalid submissions.

## Technologies Used

- **Python:** Backend programming and application logic.
- **Flask:** Web framework for handling requests and rendering pages.
- **SQLite:** Relational database for storing application information.
- **HTML:** Structure of the web interface.
- **Jinja:** Dynamically displays information from Flask in HTML.
- **CSS:** Planned interface styling.
- **Git/GitHub:** Version control and project documentation.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CoursePilot.git
cd CoursePilot
```

Replace `YOUR_USERNAME` with the repository owner's GitHub username.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Initialize the database

```bash
python init_db.py
```

This creates the SQLite database and its tables.

### 5. Run the application

```bash
python -m flask --app app run --debug
```

Open `http://127.0.0.1:5000` in your browser.

**Note:** CoursePilot is currently under development. The database starts without semester records, and semesters must currently be added manually through SQLite before courses can be created through the website.

## Planned Features

- Create and manage semesters.
- Add, edit, delete, and complete assignments.
- Automatically prioritize assignments based on deadlines, estimated effort, and importance.
- Display assignment recommendations on a dashboard.
- Automatically archive courses after their semesters end, with warnings for unfinished assignments.
- Improve the user interface and mobile responsiveness.

## Long-Term Goals

- Integrate with the Canvas LMS API to import courses and assignments.
- Synchronize assignment deadlines with Canvas.
- Support individual user accounts.
- Provide optional study scheduling recommendations.

## Project Status

**In Development — Sprint 1**

Current focus: Building the Flask application, SQLite database, and course management functionality.

## Author

Developed as a CSE 199R discovery project at Brigham Young University–Idaho.