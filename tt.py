import sqlite3

conn = sqlite3.connect("database/attendance.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM attendance WHERE student_id='103'")

conn.commit()
conn.close()

print("Deleted Successfully")