import socket
import random

# Server vorbereiten
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 50000))
s.listen(1)

print("Warte auf Verbindung...")
conn, addr = s.accept()
print(f"Verbunden mit {addr}")

# Spielvariablen
woerter = ["python", "spiel", "programm", "schule", "computer"]
wort = random.choice(woerter)
erraten = ["_"] * len(wort)
versuche = 6
benutzte_buchstaben = []

conn.send("Willkommen bei Hangman!".encode())

try:
    while versuche > 0 and "_" in erraten:
        # Spielstand senden
        status = f"\nWort: {' '.join(erraten)}\nBenutzte Buchstaben: {', '.join(benutzte_buchstaben)}\nVerbleibende Versuche: {versuche}\n>> Rate einen Buchstaben:"
        conn.send(status.encode())

        # Eingabe vom Client
        buchstabe = conn.recv(1024).decode().lower()
        if not buchstabe:
            break

        if len(buchstabe) != 1 or not buchstabe.isalpha():
            antwort = "Bitte gib nur einen Buchstaben ein."
        elif buchstabe in benutzte_buchstaben:
            antwort = "Diesen Buchstaben hast du schon probiert."
        else:
            benutzte_buchstaben.append(buchstabe)
            if buchstabe in wort:
                for i in range(len(wort)):
                    if wort[i] == buchstabe:
                        erraten[i] = buchstabe
                antwort = "Richtig!"
            else:
                versuche -= 1
                antwort = "Falsch!"

        # Rückmeldung senden
        conn.send(antwort.encode())

    # Spielende
    if "_" not in erraten:
        conn.send(f"\nGlückwunsch! Du hast das Wort erraten: {wort}".encode())
    else:
        conn.send(f"\nLeider verloren. Das Wort war: {wort}".encode())

finally:
    conn.close()
    s.close()
