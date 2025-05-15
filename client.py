import socket
import tkinter as tk
from tkinter import messagebox

# Verbindung zum Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '127.0.0.1'
s.connect((ip, 50000))

# --- GUI Setup ---
root = tk.Tk()
root.title("Hangman Client")

# Spielstand (Wort, Versuche etc.)
status_label = tk.Label(root, text="", justify="left", font=("Arial", 12), anchor="w", height=6, width=50)
status_label.pack(padx=10, pady=(10, 5))

# Rückmeldung nach Eingabe (z. B. "Falsch!")
feedback_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
feedback_label.pack(padx=10, pady=(0, 10))

# Eingabe
entry = tk.Entry(root, font=("Arial", 14), width=5)
entry.pack(padx=10, pady=5)

def sende_buchstabe():
    buchstabe = entry.get().strip().lower()
    if len(buchstabe) != 1 or not buchstabe.isalpha():
        messagebox.showwarning("Ungültig", "Bitte gib genau einen Buchstaben ein.")
        return

    s.send(buchstabe.encode())
    entry.delete(0, tk.END)

    rueckmeldung = s.recv(1024).decode()
    feedback_label.config(text=rueckmeldung)

    # Nächster Spielstand
    neuer_status = s.recv(1024).decode()
    status_label.config(text=neuer_status)

    if "erraten:" in rueckmeldung or "verloren" in rueckmeldung:
        s.close()
        entry.config(state="disabled")
        send_button.config(state="disabled")
        feedback_label.config(fg="green" if "erraten" in rueckmeldung else "red")

send_button = tk.Button(root, text="Buchstaben senden", command=sende_buchstabe)
send_button.pack(padx=10, pady=10)

def empfange_status():
    try:
        erster_status = s.recv(1024).decode()
        status_label.config(text=erster_status)
    except Exception as e:
        status_label.config(text="Fehler bei Verbindung: " + str(e))

root.after(100, empfange_status)
root.mainloop()
