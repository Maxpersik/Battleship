import battleship_map as bsm, socket, sys, battleship_bot as bsb

players_ip = []
wm = 0
kills = [0, 0, 0]

gameOver = False
botGame = True

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
        if gameOver == True:
            sock.send("Игра закончена!!!".encode())
            print("Игра закончена")
            sys.exit()
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
                win = ""
                kills[player] += 1
                wm = player
                if kills[player] >= 20:
                    gameOver = True
                    win = "\nCongratulations!!!!!!! You are winner!!"
                sock.send(("Вы попали, стреляйте снова!!!" + win).encode())
            else:
                wm = bsm.enemyPlayer(player)
                sock.send("Вы не попали, переход хода :(".encode())
            #print(bsb.botPlayer)
            if botGame == True and wm == bsb.botPlayer:
                while True:
                    x, y = bsb.getShootBot(goal)
                    goal = bsm.makeShoot(bsb.botPlayer, x, y)
                    if goal == False:
                        wm = bsm.enemyPlayer(bsb.botPlayer)
                        break


                


    sock.close()

