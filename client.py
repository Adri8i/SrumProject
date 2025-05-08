import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '127.0.0.1'
s.connect((ip, 50000))

try:
    while True:
        # Nachricht an Server senden
        msg = input("Du (Client): ")
        s.send(msg.encode())

        # Antwort vom Server empfangen
        data = s.recv(1024)
        if not data:
            print("Verbindung beendet.")
            break
        print("Server:", data.decode())
finally:
    s.close()
