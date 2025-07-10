import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib
import json
import os
from datetime import datetime

DATA_FILE = "notes_data.json"

# ----------------- Utility Functions -----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"password": "", "notes": []}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ----------------- Login Screen -----------------
def show_login_screen():
    login_frame = tk.Frame(root, bg="#f0f0f0")
    login_frame.pack(pady=100)

    tk.Label(login_frame, text="🔐 Enter Master Password", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    password_entry = tk.Entry(login_frame, show="*", width=25, font=("Arial", 12))
    password_entry.pack(pady=5)

    def login():
        entered = password_entry.get()
        if not data["password"]:
            # Set new password
            data["password"] = hash_password(entered)
            save_data()
            messagebox.showinfo("Success", "Password set successfully!")
            login_frame.destroy()
            show_notes_screen()
        elif hash_password(entered) == data["password"]:
            login_frame.destroy()
            show_notes_screen()
        else:
            messagebox.showerror("Error", "Incorrect password!")

    tk.Button(login_frame, text="Login", command=login, bg="#4caf50", fg="white", width=15).pack(pady=10)

# ----------------- Notes Screen -----------------
def show_notes_screen():
    notes_frame = tk.Frame(root, bg="#ffffff")
    notes_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(notes_frame, text="📓 Your Notes", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)

    notes_listbox = tk.Listbox(notes_frame, font=("Arial", 12), width=50, height=10)
    notes_listbox.pack(pady=10)

    for note in data["notes"]:
        notes_listbox.insert(tk.END, f"{note['title']} ({note['date']})")

    def add_note():
        note_window = tk.Toplevel(root)
        note_window.title("Add New Note")
        note_window.geometry("350x300")
        note_window.grab_set()  # Make modal

        # Title input
        tk.Label(note_window, text="Enter Title:", font=("Arial", 12)).pack(pady=(10, 0))
        title_entry = tk.Entry(note_window, font=("Arial", 12), width=35)
        title_entry.pack(pady=(0, 10))

        # Content input
        tk.Label(note_window, text="Enter Content:", font=("Arial", 12)).pack()
        content_text = tk.Text(note_window, height=8, width=35)
        content_text.pack(pady=5)

        def save_note():
            title = title_entry.get().strip()
            content = content_text.get("1.0", tk.END).strip()

            if not title:
                messagebox.showwarning("Missing Title", "Title is required!")
                return
            if not content:
                messagebox.showwarning("Missing Content", "Content is required!")
                return

            new_note = {
                "title": title,
                "content": content,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            data["notes"].append(new_note)
            save_data()
            notes_listbox.insert(tk.END, f"{title} ({new_note['date']})")
            note_window.destroy()

        tk.Button(note_window, text="Save Note", command=save_note, bg="#4caf50", fg="white").pack(pady=10)



    def view_note():
        selected = notes_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a note.")
            return
        index = selected[0]
        note = data["notes"][index]
        messagebox.showinfo(note["title"], note["content"])


    def delete_note():
        selected = notes_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a note to delete.")
            return
        index = selected[0]
        note = data["notes"][index]
        confirm = messagebox.askyesno("Delete Note", f"Are you sure you want to delete '{note['title']}'?")
        if confirm:
            notes_listbox.delete(index)
            data["notes"].pop(index)
            save_data()



    btn_frame = tk.Frame(notes_frame, bg="#ffffff")
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="➕ Add Note", command=add_note, bg="#2196f3", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="👁 View", command=view_note, bg="#4caf50", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="🗑 Delete", command=delete_note, bg="#f44336", fg="white", width=12).grid(row=0, column=2, padx=5)

# ----------------- Main App Setup -----------------
root = tk.Tk()
root.title("Personal Notes Locker")
root.geometry("400x500")
root.configure(bg="#f0f0f0")

data = load_data()
show_login_screen()

root.mainloop()