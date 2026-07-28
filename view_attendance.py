import tkinter as tk
from tkinter import ttk
import sqlite3
import os

# -----------------------------------
# Database Path
# -----------------------------------
DB_PATH = os.path.join("database", "attendance.db")


# -----------------------------------
# Connect Database
# -----------------------------------
def connect_db():
    return sqlite3.connect(DB_PATH)

# -----------------------------------
# Dashboard Statistics
# -----------------------------------

def total_students():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")

    total = cursor.fetchone()[0]

    conn.close()

    return total


def today_attendance():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM attendance

        WHERE date = DATE('now')

    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# -----------------------------------
# Load Attendance Records
# -----------------------------------
def load_data():

    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            attendance.student_id,
            students.name,
            students.department,
            attendance.date,
            attendance.time,
            attendance.status
        FROM attendance
        INNER JOIN students
        ON attendance.student_id = students.student_id
        ORDER BY attendance.date DESC,
                 attendance.time DESC
    """)

    records = cursor.fetchall()

    conn.close()

    for index, row in enumerate(records):

        if index % 2 == 0:
            tree.insert("", tk.END, values=row, tags=("even",))
        else:
            tree.insert("", tk.END, values=row, tags=("odd",))

# -----------------------------------
# Search Attendance
# -----------------------------------
def search_data():

    keyword = search_var.get().strip()

    # If search box is empty, load everything
    if keyword == "":
        load_data()
        return

    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            attendance.student_id,
            students.name,
            students.department,
            attendance.date,
            attendance.time,
            attendance.status
        FROM attendance
        INNER JOIN students
        ON attendance.student_id = students.student_id
        WHERE
            attendance.student_id LIKE ?
            OR students.name LIKE ?
        ORDER BY
            attendance.date DESC,
            attendance.time DESC
    """, (f"%{keyword}%", f"%{keyword}%"))

    records = cursor.fetchall()

    conn.close()

    for index, row in enumerate(records):
        if index % 2 == 0:
            tree.insert("", tk.END, values=row, tags=("even",))
        else:
            tree.insert("", tk.END, values=row, tags=("odd",))

# -----------------------------------
# Refresh Table
# -----------------------------------
def refresh_data():

    search_var.set("")
    date_var.set("")

    load_data()

# -----------------------------------
# Filter Attendance By Date
# -----------------------------------
def filter_by_date():

    selected_date = date_var.get().strip()

    # If date box is empty
    if selected_date == "":
        load_data()
        return

    # Clear old rows
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            attendance.student_id,
            students.name,
            students.department,
            attendance.date,
            attendance.time,
            attendance.status
        FROM attendance
        INNER JOIN students
        ON attendance.student_id = students.student_id
        WHERE attendance.date = ?
        ORDER BY attendance.time DESC
    """, (selected_date,))

    records = cursor.fetchall()

    conn.close()

    # Display records
    for index, row in enumerate(records):
        if index % 2 == 0:
            tree.insert("", tk.END, values=row, tags=("even",))
        else:
            tree.insert("", tk.END, values=row, tags=("odd",))

# -----------------------------------
# Main Window
# -----------------------------------
root = tk.Tk()

root.title("Attendance Records")

root.geometry("1000x600")

root.configure(bg="#F4F6F9")

root.resizable(False, False)


# -----------------------------------
# Heading
# -----------------------------------
heading = tk.Label(
    root,
    text="Attendance Records",
    font=("Arial", 20, "bold"),
    bg="#F4F6F9",
    fg="#003366"
)

heading.pack(pady=15)
# -----------------------------------
# Statistics
# -----------------------------------

stats_frame = tk.Frame(
    root,
    bg="#F4F6F9"
)

stats_frame.pack(pady=5)

students_label = tk.Label(
    stats_frame,
    text=f"👤 Total Students : {total_students()}",
    font=("Arial",12,"bold"),
    bg="#F4F6F9",
    fg="#1976D2"
)

students_label.grid(
    row=0,
    column=0,
    padx=30
)

attendance_label = tk.Label(
    stats_frame,
    text=f"📅 Today's Attendance : {today_attendance()}",
    font=("Arial",12,"bold"),
    bg="#F4F6F9",
    fg="#2E8B57"
)

attendance_label.grid(
    row=0,
    column=1,
    padx=30
)


# -----------------------------------
# Search Frame
# -----------------------------------
search_frame = tk.Frame(
    root,
    bg="#F4F6F9"
)

search_frame.pack(pady=5)

search_label = tk.Label(
    search_frame,
    text="Search (ID / Name):",
    font=("Arial", 12, "bold"),
    bg="#F4F6F9"
)

search_label.grid(
    row=0,
    column=0,
    padx=8
)

search_var = tk.StringVar()

search_entry = tk.Entry(
    search_frame,
    textvariable=search_var,
    width=30,
    font=("Arial", 12)
)

search_entry.grid(
    row=0,
    column=1,
    padx=8
)

search_button = tk.Button(
    search_frame,
    text="Search",
    bg="#2196F3",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12,
    command=search_data
)

search_button.grid(
    row=0,
    column=2,
    padx=8
)

refresh_button = tk.Button(
    search_frame,
    text="Refresh",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12,
    command=refresh_data
)

refresh_button.grid(
    row=0,
    column=3,
    padx=8
)

# -----------------------------------
# Date Filter
# -----------------------------------

date_label = tk.Label(
    search_frame,
    text="Date (YYYY-MM-DD):",
    font=("Arial", 12, "bold"),
    bg="#F4F6F9"
)

date_label.grid(
    row=1,
    column=0,
    padx=8,
    pady=10
)

date_var = tk.StringVar()

date_entry = tk.Entry(
    search_frame,
    textvariable=date_var,
    width=30,
    font=("Arial", 12)
)

date_entry.grid(
    row=1,
    column=1,
    padx=8,
    pady=10
)

filter_button = tk.Button(
    search_frame,
    text="Filter Date",
    bg="#9C27B0",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12,
    command=filter_by_date
)

filter_button.grid(
    row=1,
    column=2,
    padx=8,
    pady=10
)

# -----------------------------------
# Table Frame
# -----------------------------------
table_frame = tk.Frame(root, bg="#F4F6F9")

table_frame.pack(pady=20)

# -----------------------------------
# Scrollbar
# -----------------------------------
scrollbar = ttk.Scrollbar(table_frame)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# -----------------------------------
# Treeview
# -----------------------------------
columns = (
    "Student ID",
    "Name",
    "Department",
    "Date",
    "Time",
    "Status"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=18,
    yscrollcommand=scrollbar.set
)

scrollbar.config(command=tree.yview)

# -----------------------------------
# Headings
# -----------------------------------
for column in columns:

    tree.heading(column, text=column)

    tree.column(
        column,
        anchor="center",
        width=150
    )

tree.tag_configure(
    "even",
    background="#F8FAFC"
)

tree.tag_configure(
    "odd",
    background="white"
)
tree.pack(side=tk.LEFT)

# -----------------------------------
# Professional Table Style
# -----------------------------------

style = ttk.Style()

style.theme_use("clam")

# Table Heading
style.configure(
    "Treeview.Heading",
    background="#1F3C88",
    foreground="white",
    font=("Segoe UI", 11, "bold"),
    relief="flat"
)

style.map(
    "Treeview.Heading",
    background=[("active", "#2952A3")]
)

# Table Body
style.configure(
    "Treeview",
    background="white",
    foreground="black",
    rowheight=30,
    font=("Segoe UI", 10),
    fieldbackground="white",
    borderwidth=0
)

style.map(
    "Treeview",
    background=[("selected", "#CCE5FF")],
    foreground=[("selected", "black")]
)

# -----------------------------------
# Back To Dashboard
# -----------------------------------

def back_to_dashboard():
    root.destroy()


# -----------------------------------
# Bottom Buttons
# -----------------------------------

bottom_frame = tk.Frame(
    root,
    bg="#F4F6F9"
)

bottom_frame.pack(pady=15)

back_button = tk.Button(
    bottom_frame,
    text="🏠 Back to Dashboard",
    bg="#1976D2",
    fg="white",
    font=("Arial", 11, "bold"),
    width=18,
    cursor="hand2",
    command=back_to_dashboard
)

back_button.grid(
    row=0,
    column=0,
    padx=12
)

close_button = tk.Button(
    bottom_frame,
    text="🚪 Close",
    bg="#F44336",
    fg="white",
    font=("Arial", 11, "bold"),
    width=18,
    cursor="hand2",
    command=root.destroy
)

close_button.grid(
    row=0,
    column=1,
    padx=12
)

# -----------------------------------
# Load Data
# -----------------------------------
load_data()

# -----------------------------------
# Start Application
# -----------------------------------
root.mainloop()