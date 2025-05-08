import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '127.0.0.1'
s.connect((ip, 50000))

try:
    while True:
        # Serverstatus empfangen
        data = s.recv(1024)
        if not data:
            break
        message = data.decode()
        print("\nServer:", message)

        if "erraten:" in message or "verloren" in message:
            break

        # Eingabe senden
        buchstabe = input(">> Dein Buchstabe: ")
        s.send(buchstabe.encode())

        # Rückmeldung vom Server
        rueckmeldung = s.recv(1024)
        print("Server:", rueckmeldung.decode())

finally:
    s.close()
