import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import threading

def run_script(cmd):
    subprocess.Popen(cmd)

def enroll():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Enter name")
        return

    threading.Thread(
        target=run_script,
        args=([sys.executable, "capture_enroll.py", "--name", name],),
        daemon=True
    ).start()

def encode():
    threading.Thread(
        target=run_script,
        args=([sys.executable, "encode_faces.py"],),
        daemon=True
    ).start()
    messagebox.showinfo("Success", "Encoding started")

def recognize():
    threading.Thread(
        target=run_script,
        args=([sys.executable, "recognize_attendance.py"],),
        daemon=True
    ).start()

def view():
    threading.Thread(
        target=run_script,
        args=([sys.executable, "app.py"],),
        daemon=True
    ).start()

# GUI
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("420x330")

tk.Label(root, text="Face Recognition Attendance",
         font=("Arial", 14, "bold")).pack(pady=15)

tk.Label(root, text="Enter Name").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

tk.Button(root, text="Enroll Face", width=25, command=enroll).pack(pady=5)
tk.Button(root, text="Train / Encode Faces", width=25, command=encode).pack(pady=5)
tk.Button(root, text="Start Attendance", width=25, command=recognize).pack(pady=5)
tk.Button(root, text="View Attendance", width=25, command=view).pack(pady=5)

root.mainloop()


