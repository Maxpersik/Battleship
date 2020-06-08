import socket, battleship_ui as bsu

HOST = "192.168.1.5"
PORT = 33333

bsu.startDisplay()

while True:
    cmd = input("Введите команду: ")

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    conn.send(cmd.encode())
    conn.settimeout(0.2)

    try:
        while True:
            data = conn.recv(1024)
            if cmd == "mapstr":
                bsu.drawGame(data.decode())
            print(data.decode(), end='')
    except socket.timeout:
        print()

    conn.close()
