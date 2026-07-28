# ============================================================
# Face Recognition Attendance System
# Professional Dashboard (Redesigned UI)
# ============================================================

import sys
import subprocess
import customtkinter as ctk
from tkinter import messagebox

# ============================================================
# Appearance
# ============================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ============================================================
# Colors
# ============================================================

BACKGROUND      = "#EEF2FA"
HEADER_TOP      = "#2A4FB8"
HEADER_BOTTOM   = "#1F3C88"
CARD_BG         = "#FFFFFF"
CARD_BORDER     = "#E1E7F3"
TEXT_DARK       = "#1F2A44"
TEXT_MUTED      = "#6B7686"
STATUS_BAR_BG   = "#FFFFFF"

GREEN   = "#2E8B57"
GREEN_H = "#246B45"
BLUE    = "#1976D2"
BLUE_H  = "#135BA5"
ORANGE  = "#F57C00"
ORANGE_H= "#D96C00"
PURPLE  = "#8E44AD"
PURPLE_H= "#6C3483"
TEAL    = "#16A085"
TEAL_H  = "#117A65"
RED     = "#D32F2F"
RED_H   = "#B71C1C"

# ============================================================
# Universal Script Runner
# ============================================================

def set_status(text, color=TEXT_DARK, dot_color="#8BC34A"):
    status_label.configure(text=text, text_color=color)
    status_dot.configure(text_color=dot_color)


def run_script(script, title):

    try:
        set_status(f"Status  •  {title}...", TEXT_DARK, "#F5A623")
        app.update_idletasks()

        subprocess.run(
            [sys.executable, script],
            check=True
        )

        set_status(f"Status  •  {title} Completed", "#1F3C88", "#2E8B57")

    except FileNotFoundError:

        messagebox.showerror(
            "Error",
            f"{script} not found!"
        )
        set_status("Status  •  File not found", RED, RED)

    except subprocess.CalledProcessError:

        messagebox.showerror(
            "Error",
            f"{title} exited with an error!"
        )
        set_status("Status  •  Error", RED, RED)

# ============================================================
# Button Functions
# ============================================================

def register_student():
    run_script("register.py", "Registration")


def train_model():
    run_script("train_model.py", "Training")


def start_attendance():
    run_script("recognize.py", "Attendance")


def view_attendance():
    try:
        subprocess.Popen(
            [sys.executable, "view_attendance.py"]
        )
        set_status("Status  •  View Attendance Opened", "#1F3C88", "#2E8B57")

    except FileNotFoundError:
        messagebox.showerror(
            "Error",
            "view_attendance.py not found!"
        )
        set_status("Status  •  File not found", RED, RED)


def export_attendance():

    try:

        subprocess.run(
            [sys.executable, "export_excel.py"],
            check=True
        )

        messagebox.showinfo(
            "Success",
            "Attendance exported successfully!"
        )

        set_status("Status  •  Export Completed", "#1F3C88", "#2E8B57")

    except FileNotFoundError:

        messagebox.showerror(
            "Error",
            "export_excel.py not found!"
        )
        set_status("Status  •  File not found", RED, RED)

    except subprocess.CalledProcessError:

        messagebox.showerror(
            "Error",
            "Export Failed!"
        )
        set_status("Status  •  Error", RED, RED)


def exit_app():

    answer = messagebox.askyesno(
        "Exit",
        "Do you want to exit?"
    )

    if answer:
        app.destroy()

# ============================================================
# Main Window
# ============================================================

app = ctk.CTk()

app.title("Face Recognition Attendance System")
app.geometry("900x680")
app.resizable(False, False)
app.configure(fg_color=BACKGROUND)

# ============================================================
# Header
# ============================================================

header = ctk.CTkFrame(
    app,
    height=110,
    fg_color=HEADER_BOTTOM,
    corner_radius=0
)
header.pack(fill="x")
header.pack_propagate(False)

# Accent strip along the top for a little polish
accent_strip = ctk.CTkFrame(header, height=4, fg_color=ORANGE, corner_radius=0)
accent_strip.pack(fill="x", side="top")

header_content = ctk.CTkFrame(header, fg_color="transparent")
header_content.pack(expand=True, fill="both")

# Logo badge (circular chip behind the emoji)
logo_badge = ctk.CTkFrame(
    header_content,
    width=48,
    height=48,
    corner_radius=24,
    fg_color=HEADER_TOP
)
logo_badge.pack(pady=(10, 2))
logo_badge.pack_propagate(False)

logo = ctk.CTkLabel(
    logo_badge,
    text="🎓",
    font=("Segoe UI Emoji", 20)
)
logo.place(relx=0.5, rely=0.5, anchor="center")

title = ctk.CTkLabel(
    header_content,
    text="FACE RECOGNITION ATTENDANCE SYSTEM",
    font=("Segoe UI", 21, "bold"),
    text_color="white"
)
title.pack()

subtitle = ctk.CTkLabel(
    header_content,
    text="Smart  •  Fast  •  Reliable Attendance Tracking",
    font=("Segoe UI", 12),
    text_color="#B9C8ED"
)
subtitle.pack(pady=(2, 6))

# ============================================================
# Welcome
# ============================================================

welcome_wrap = ctk.CTkFrame(app, fg_color="transparent")
welcome_wrap.pack(pady=(12, 4))

welcome = ctk.CTkLabel(
    welcome_wrap,
    text="Welcome back 👋",
    font=("Segoe UI", 19, "bold"),
    text_color=TEXT_DARK
)
welcome.pack()

instruction = ctk.CTkLabel(
    welcome_wrap,
    text="Choose an operation below to get started",
    font=("Segoe UI", 12),
    text_color=TEXT_MUTED
)
instruction.pack(pady=(2, 0))

# ============================================================
# Dashboard Card (with a soft "shadow" behind it)
# ============================================================

card_shadow = ctk.CTkFrame(
    app,
    width=740,
    height=350,
    corner_radius=20,
    fg_color="#D9E0F0"
)
card_shadow.pack(pady=(12, 0))
card_shadow.pack_propagate(False)

dashboard = ctk.CTkFrame(
    card_shadow,
    corner_radius=18,
    fg_color=CARD_BG,
    border_width=1,
    border_color=CARD_BORDER
)
dashboard.place(relx=0.5, rely=0.48, anchor="center", relwidth=0.98, relheight=0.95)

# Grid config: 2 columns x 3 rows of tiles
dashboard.grid_columnconfigure((0, 1), weight=1, uniform="col")
dashboard.grid_rowconfigure((0, 1, 2), weight=1, uniform="row")

# ============================================================
# Helper Function — icon tile button
# ============================================================

def create_tile(parent, row, col, icon, text, command, color, hover_color):
    tile = ctk.CTkFrame(
        parent,
        corner_radius=16,
        fg_color="#F7F9FD",
        border_width=1,
        border_color="#E7ECF6"
    )
    tile.grid(row=row, column=col, padx=16, pady=8, sticky="nsew")

    icon_chip = ctk.CTkLabel(
        tile,
        text=icon,
        font=("Segoe UI Emoji", 20),
        width=42,
        height=42,
        corner_radius=21,
        fg_color=color,
        text_color="white"
    )
    icon_chip.pack(pady=(14, 6))

    label = ctk.CTkLabel(
        tile,
        text=text,
        font=("Segoe UI", 13, "bold"),
        text_color=TEXT_DARK
    )
    label.pack(pady=(0, 12))

    # Whole tile is clickable — hover highlights it so it still reads as interactive
    widgets = (tile, icon_chip, label)

    def on_enter(e):
        tile.configure(fg_color="#EDF1FB", border_color=color)

    def on_leave(e):
        tile.configure(fg_color="#F7F9FD", border_color="#E7ECF6")

    for widget in widgets:
        widget.bind("<Button-1>", lambda e: command())
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.configure(cursor="hand2")

    return tile

# ============================================================
# Dashboard Tiles
# ============================================================

create_tile(dashboard, 0, 0, "👤", "Register Student", register_student, GREEN, GREEN_H)
create_tile(dashboard, 0, 1, "🧠", "Train Model", train_model, BLUE, BLUE_H)
create_tile(dashboard, 1, 0, "📷", "Start Attendance", start_attendance, ORANGE, ORANGE_H)
create_tile(dashboard, 1, 1, "📋", "View Attendance", view_attendance, PURPLE, PURPLE_H)
create_tile(dashboard, 2, 0, "📁", "Export Attendance", export_attendance, TEAL, TEAL_H)
create_tile(dashboard, 2, 1, "🚪", "Exit", exit_app, RED, RED_H)

# ============================================================
# Status Bar
# ============================================================

status_bar = ctk.CTkFrame(
    app,
    fg_color=STATUS_BAR_BG,
    corner_radius=12,
    border_width=1,
    border_color=CARD_BORDER,
    height=36
)
status_bar.pack(fill="x", padx=30, pady=(14, 0))
status_bar.pack_propagate(False)

status_dot = ctk.CTkLabel(
    status_bar,
    text="●",
    font=("Segoe UI", 14),
    text_color="#8BC34A"
)
status_dot.pack(side="left", padx=(16, 6))

status_label = ctk.CTkLabel(
    status_bar,
    text="Status  •  Ready",
    font=("Segoe UI", 13),
    text_color=TEXT_DARK
)
status_label.pack(side="left")

# keep old variable name available in case other code references `status`
status = status_label

# ============================================================
# Footer
# ============================================================

footer = ctk.CTkLabel(
    app,
    text="Face Recognition Attendance System  •  Version 1.0",
    font=("Segoe UI", 11),
    text_color=TEXT_MUTED
)
footer.pack(pady=(6, 10))

# ============================================================
# Run Application
# ============================================================

app.mainloop()