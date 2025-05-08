import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 50000))
s.listen(1)

print("Warte auf Verbindung...")
conn, addr = s.accept()
print(f"Verbunden mit {addr}")

try:
    while True:
        # Nachricht vom Client empfangen
        data = conn.recv(1024)
        if not data:
            print("Verbindung beendet.")
            break
        print("Client:", data.decode())

        # Antwort senden
        msg = input("Du (Server): ")
        conn.send(msg.encode())
finally:
    conn.close()
    s.close()
