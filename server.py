import socket
import threading
import random
import csv

# --- Spielstatus (global) ---
with open('C:\\hangman_woerter.csv', 'r') as f:
    reader = csv.reader(f)
    woerter = [row[0] for row in reader]

wort = random.choice(woerter)
erraten = ["_"] * len(wort)
versuche = 6
benutzte = []
clients = []
lock = threading.Lock()  # für sicheren Zugriff

def status_text():
    return f"\nWort: {' '.join(erraten)}\nBenutzte: {', '.join(benutzte)}\nVersuche: {versuche}\n"

def sende_an_alle(nachricht):
    for c in clients:
        try:
            c.send(nachricht.encode())
        except:
            clients.remove(c)

def client_thread(conn, addr):
    global versuche

    print(f"Verbunden mit {addr}")
    conn.send("Willkommen bei HANGMAN!\n".encode())
    conn.send(status_text().encode())

    while True:
        try:
            daten = conn.recv(1024)
            if not daten:
                break

            buchstabe = daten.decode().strip().lower()

            antwort = ""
            with lock:
                if len(buchstabe) != 1 or not buchstabe.isalpha():
                    antwort = "Bitte nur einen Buchstaben.\n"
                elif buchstabe in benutzte:
                    antwort = f"'{buchstabe}' wurde schon benutzt.\n"
                else:
                    benutzte.append(buchstabe)
                    if buchstabe in wort:
                        for i in range(len(wort)):
                            if wort[i] == buchstabe:
                                erraten[i] = buchstabe
                        antwort = f"Richtig: {buchstabe}"
                    else:
                        versuche -= 1
                        antwort = f"Falsch: {buchstabe}"

                # An alle senden
                sende_an_alle(antwort + "\n" + status_text())

                if "_" not in erraten:
                    sende_an_alle(f"Gewonnen! Das Wort war: {wort}\n")
                    break
                if versuche == 0:
                    sende_an_alle(f"Verloren! Das Wort war: {wort}\n")
                    break

        except:
            break

    print(f"Spieler {addr} hat verlassen.")
    clients.remove(conn)
    conn.close()

# --- Server starten ---
server = socket.socket()
server.bind(('', 50000))
server.listen()

print("Server läuft. Warten auf Verbindungen...")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=client_thread, args=(conn, addr), daemon=True).start()