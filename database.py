import sqlite3
import os

# Database Path
DB_PATH = os.path.join("database", "attendance.db")


# ----------------------------
# Connect to Database
# ----------------------------
def connect_db():
    return sqlite3.connect(DB_PATH)


# ----------------------------
# Create Tables
# ----------------------------
def create_database():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        year TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        date TEXT,
        time TEXT,
        status TEXT,
        FOREIGN KEY(student_id)
        REFERENCES students(student_id)
    )
    """)

    conn.commit()
    conn.close()


# ----------------------------
# Add Student
# ----------------------------
def add_student(student_id, name, department, year):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (student_id, name, department, year)
    VALUES (?, ?, ?, ?)
    """, (student_id, name, department, year))

    conn.commit()
    conn.close()

# ----------------------------
# Check if Student Exists
# ----------------------------
def student_exists(student_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    conn.close()

    return student is not None 

# ----------------------------
# Get Student Details
# ----------------------------
def get_student(student_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT student_id, name, department, year
    FROM students
    WHERE student_id = ?
    """, (student_id,))

    student = cursor.fetchone()

    conn.close()

    return student

# Run only when database.py is executed directly
if __name__ == "__main__":
    create_database()
    print("Database Ready!") 

# ----------------------------
# Check Today's Attendance
# ----------------------------
def attendance_exists(student_id, date):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM attendance
    WHERE student_id = ? AND date = ?
    """, (student_id, date))

    record = cursor.fetchone()

    conn.close()

    return record is not None


# ----------------------------
# Mark Attendance
# ----------------------------
def mark_attendance(student_id, date, time, status="Present"):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO attendance
    (student_id, date, time, status)
    VALUES (?, ?, ?, ?)
    """, (student_id, date, time, status))

    conn.commit()
    conn.close()