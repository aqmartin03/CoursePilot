CREATE TABLE semesters (
    semester_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    CHECK (end_date > start_date)
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    semester_id INTEGER NOT NULL,
    course_code TEXT NOT NULL,
    course_name TEXT NOT NULL,
    is_archived INTEGER NOT NULL DEFAULT 0,
    CHECK (is_archived IN (0, 1)),
    FOREIGN KEY (semester_id)
        REFERENCES semesters(semester_id)
);

CREATE TABLE assignments (
    assignment_id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    due_date TEXT NOT NULL,
    estimated_hours REAL NOT NULL,
    importance INTEGER NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0,
    CHECK (completed IN (0, 1)),
    CHECK (importance BETWEEN 1 AND 5),
    CHECK (estimated_hours > 0),
    FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
);