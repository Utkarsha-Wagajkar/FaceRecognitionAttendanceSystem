import sqlite3
import os

DB_PATH = os.path.join("database", "attendance.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM students")
students = cursor.fetchall()

print("\nRegistered Students")
print("-" * 50)

for student in students:
    print(student)

conn.close()