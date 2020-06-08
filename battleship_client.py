import socket

HOST = ""
PORT = 33333

while True:
    cmd = input("Введите команду: ")

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    conn.send(cmd.encode())
    conn.settimeout(0.2)

    try:
        while True:
            data = conn.recv(1024)
            print(data.decode(), end='')
    except socket.timeout:
        print()

    conn.close()
