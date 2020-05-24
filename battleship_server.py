import battleship_map as bsm, socket, time

players_ip = []
wm = 0

HOST = ""
PORT = 33333

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

while True:
    print("Слушаю порт: ", PORT)
    server.listen(2)
    sock, addr = server.accept()
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print("ПоЛуЧеНо оТ: ", addr, data.decode())
        ip = addr[0]
        if ip not in players_ip and len(players_ip) > 2:
            sock.send("Лобби переполнено! \n")
            break
        if ip not in players_ip:
            players_ip.append(ip)
        if players_ip[0] == ip:
            player = 1
        else:
            player = 2

        gamer = "Вы игрок номер " + str(player) + "\n"

        ds = data.decode()

        if ds == "map":
            map1 = bsm.getFriendShips(player)
            map2 = bsm.getEnemyShips(player)
            q = sock.send((gamer + map1 + map2).encode())
            print(q)
        if len(ds) == 2:
            if player != wm and wm > 0:
                sock.send("Не ваш ход".encode())
                continue

            L = "ABCDEFGHIJ"
            try:
                x = int(L.index(ds[0:1])) + 1
                y = int(ds[1:2]) + 1
            except:
                sock.send("Ошибка ввода!".encode())
                continue
            goal = bsm.makeShoot(player, x, y)
            if goal == 1:
                wm = player
                sock.send("Вы попали, стреляйте снова!!!".encode())
            else:
                wm = bsm.enemyPlayer(player)
                sock.send("Вы не попали, переход хода :(".encode())

    sock.close()

