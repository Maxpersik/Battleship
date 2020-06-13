import battleship_map as bsm, socket, sys, battleship_bot as bsb

players_ip = []
wm = 0
kills = [0, 0, 0]

gameOver = False
botGame = True
winPlayer = 0


map1 = bsm.getFriendShips(1)
map2 = bsm.getEnemyShips(2)

HOST = ""
PORT = 33333

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

if botGame == True:
    players_ip.append("0.0.0.0")

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

        if ds == "mapstr":
            map1 = bsm.mapStr(player, 1)
            map2 = bsm.mapStr(bsm.enemyPlayer(player), 0)
            q = sock.send((map1 + map2).encode())

        if len(ds) == 2:
            answer = ""
            if gameOver == True:
                if player == winPlayer:
                    answer = "4"
                else:
                    answer = "3"
                sock.send(answer.encode())
                continue
            if player != wm and wm > 0:
                sock.send("Не ваш ход".encode())
                continue

            L = "ABCDEFGHIJ"
            try:
                x = int(L.index(ds[0:1])) + 1
                y = int(ds[1:2]) + 1
            except:
                continue

            goal = bsm.makeShoot(player, x, y)

            if goal == 1:
                kills[player] += 1
                wm = player
                if kills[player] >= 20:
                    gameOver = True
                    winPlayer = player
            if goal == 0:
                wm = bsm.enemyPlayer(player)

            answer = str(goal)
            sock.send(answer.encode())

            if goal == 2:
                continue
            #print(bsb.botPlayer)
            if botGame == True and wm == bsb.botPlayer:
                goal = False
                while True:
                    x, y = bsb.getShootBot(goal, x, y)
                    goal = bsm.makeShoot(bsb.botPlayer, x, y)
                    print(x, y)
                    if goal == True:
                        kills[bsb.botPlayer] += 1
                        if kills[bsb.botPlayer] >= 20:
                            gameOver = True
                            winPlayer = bsb.botPlayer
                            break
                    else:
                        wm = bsm.enemyPlayer(bsb.botPlayer)
                        break

    sock.close()

