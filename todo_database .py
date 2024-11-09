import tkinter as tk
from tkinter import messagebox
from win10toast import ToastNotifier
import sqlite3
import datetime

# Create or connect to the SQLite database
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Create a tasks table if it doesn't already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        priority TEXT,
        completed BOOLEAN NOT NULL CHECK (completed IN (0,1))
    )
''')
conn.commit()

# Initialize the notifier
notifier = ToastNotifier()

# Function to add a task
def add_task():
    title = title_entry.get()
    description = description_entry.get("1.0", "end-1c")
    due_date = due_date_entry.get()
    priority = priority_var.get()

    if title == "":
        messagebox.showwarning("Input Error", "Task title cannot be empty!")
        return

    cursor.execute("INSERT INTO tasks (title, description, due_date, priority, completed) VALUES (?, ?, ?, ?, ?)",
                   (title, description, due_date, priority, False))
    conn.commit()
    notifier.show_toast("Task Added", f"{title} added successfully!", duration=5)
    display_tasks()
    clear_entries()

# Function to clear input fields
def clear_entries():
    title_entry.delete(0, tk.END)
    description_entry.delete("1.0", tk.END)
    due_date_entry.delete(0, tk.END)
    priority_var.set("Low")

# Function to display tasks
def display_tasks():
    tasks_list.delete(0, tk.END)
    cursor.execute("SELECT * FROM tasks WHERE completed=0")
    tasks = cursor.fetchall()
    for task in tasks:
        tasks_list.insert(tk.END, f"{task[1]} - {task[3]} (Due: {task[2]})")

# GUI setup
root = tk.Tk()
root.title("To-Do List")

# Task Entry Section
title_label = tk.Label(root, text="Task Title")
title_label.grid(row=0, column=0)
title_entry = tk.Entry(root, width=30)
title_entry.grid(row=0, column=1)

description_label = tk.Label(root, text="Description")
description_label.grid(row=1, column=0)
description_entry = tk.Text(root, height=3, width=30)
description_entry.grid(row=1, column=1)

due_date_label = tk.Label(root, text="Due Date")
due_date_label.grid(row=2, column=0)
due_date_entry = tk.Entry(root, width=30)
due_date_entry.grid(row=2, column=1)

priority_label = tk.Label(root, text="Priority")
priority_label.grid(row=3, column=0)
priority_var = tk.StringVar(value="Low")
priority_menu = tk.OptionMenu(root, priority_var, "Low", "Medium", "High")
priority_menu.grid(row=3, column=1)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.grid(row=4, column=1, pady=10)

# Task Display Section
tasks_list = tk.Listbox(root, width=50, height=15)
tasks_list.grid(row=5, column=0, columnspan=2, pady=10)

display_tasks()  # Load tasks on startup
root.mainloop()




# Function to check for upcoming tasks and notify
def check_reminders():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("SELECT title, due_date FROM tasks WHERE due_date >= ?", (current_time,))
    tasks = cursor.fetchall()
    for task in tasks:
        notifier.show_toast("Task Reminder", f"{task[0]} is due soon!", duration=10)

# Schedule this function to run every hour (or as needed) in the app
