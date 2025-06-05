import socket
import threading
import tkinter as tk
from tkinter import messagebox

# Verbindung zum Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '127.0.0.1'
s.connect((ip, 50000))

# --- GUI Setup ---
root = tk.Tk()
root.title("Hangman Client")
root.geometry("450x500")  # Fenstergröße etwas größer

# --- Text-Widget für Status + Strichmännchen ---
status_text = tk.Text(root, font=("Courier New", 14), height=14, width=50, bg="white")
status_text.pack(padx=10, pady=(10, 5))
status_text.config(state=tk.DISABLED)

# Rückmeldung (z. B. "Richtig!") – kurz und schlicht
feedback_label = tk.Label(root, text="", font=("Arial", 12), fg="black")
feedback_label.pack(padx=10, pady=(0, 10))

# Eingabe
entry = tk.Entry(root, font=("Arial", 14), width=5)
entry.pack(padx=10, pady=(0, 5))

def sende_buchstabe():
    buchstabe = entry.get().strip().lower()
    if len(buchstabe) != 1 or not buchstabe.isalpha():
        messagebox.showwarning("Ungültig", "Bitte gib genau einen Buchstaben ein.")
        return

    try:
        s.send(buchstabe.encode())
    except:
        feedback_label.config(text="Verbindung zum Server verloren.")
        return

    entry.delete(0, tk.END)

# Button zum Senden
send_button = tk.Button(root, text="Buchstaben senden", command=sende_buchstabe)
send_button.pack(padx=10, pady=(5, 10))

# Funktion zur Darstellung des Strichmännchens
def zeichne_strichmaennchen(versuche):
    hangman = [
        "  _______     ",
        " |/      |    ",
        " |      {kopf}   ",
        " |      {koerper}   ",
        " |      {linker_arm}{rumpf}{rechter_arm}  ",
        " |      {linkes_bein} {rechtes_bein}   ",
        " |             ",
        "_|___          "
    ]

    kopf = " "
    koerper = " "
    linker_arm = " "
    rechter_arm = " "
    rumpf = " "
    linkes_bein = " "
    rechtes_bein = " "

    fehler = 6 - versuche

    if fehler >= 1:
        kopf = "O"
    if fehler >= 2:
        koerper = "|"
    if fehler >= 3:
        linker_arm = "/"
    if fehler >= 4:
        rechter_arm = "\\"
    if fehler >= 5:
        linkes_bein = "/"
    if fehler >= 6:
        rechtes_bein = "\\"

    return "\n".join(hangman).format(
        kopf=kopf,
        koerper=koerper,
        linker_arm=linker_arm,
        rechter_arm=rechter_arm,
        rumpf=rumpf,
        linkes_bein=linkes_bein,
        rechtes_bein=rechtes_bein,
    )

def update_status(text):
    status_text.config(state=tk.NORMAL)
    status_text.delete("1.0", tk.END)
    status_text.insert(tk.END, text)
    status_text.config(state=tk.DISABLED)

# --- Empfangsthread ---
def empfangen():
    while True:
        try:
            nachricht = s.recv(2048).decode()
            if not nachricht:
                break

            teile = nachricht.strip().split("\n", 1)
            if len(teile) == 2:
                feedback, status = teile

                versuche = 6
                for line in status.split("\n"):
                    if line.startswith("Versuche:"):
                        try:
                            versuche = int(line.split(":")[1].strip())
                        except:
                            pass

                strichmaennchen = zeichne_strichmaennchen(versuche)

                update_status(strichmaennchen + "\n\n" + status.strip())
                feedback_label.config(text=feedback.strip())
            else:
                update_status(nachricht.strip())
                feedback_label.config(text="")

        except:
            break

    s.close()
    entry.config(state="disabled")
    send_button.config(state="disabled")
    feedback_label.config(text="Verbindung getrennt.")

# Empfang läuft im Hintergrund
threading.Thread(target=empfangen, daemon=True).start()

# Start GUI
root.mainloop()
