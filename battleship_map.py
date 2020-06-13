import random

N = 10
debug = 0

server_ships = []
server_ships.insert(1, [])
server_ships.insert(2, [])

server_shoots = []
server_shoots.insert(0, [])
server_shoots.insert(1, [])
server_shoots.insert(2, [])

def genShips(N, debug = False):
    ships = []
    deny = []
    
    # Однопалубные корабли х 4
    while len(ships) < 4:
        x = random.randint(1, N)
        y = random.randint(1, N)
        if (x, y) in deny:
            continue
        ships.append((x, y))
        denyExtend(deny, x, y)

    # Двухпалубные корабли х 3
    while len(ships) < 10:
        x = random.randint(1, N)
        y = random.randint(1, N)
        if (x, y) in deny:
            continue
        ships.append((x, y))
        for i in range(4):
            dir = random.randint(0, 3)
            x1, y1 = randDirect(x, y, dir)
            if x1 < 11 and x1 > 0 and y1 < 11 and y1 > 0 and (x1, y1) not in deny:
                ships.append((x1, y1))
                break
        denyExtend(deny,x, y)
        denyExtend(deny, x1, y1)

    # Трехпалубные корабли
    while len(ships) < 16:
        x = random.randint(1, N)
        y = random.randint(1, N)
        if (x, y) in deny:
            continue

        for i in range(4):
            dir = random.randint(0, 3)
            x1, y1 = randDirect(x, y, dir)
            if x1 < 11 and x1 > 0 and y1 < 11 and y1 > 0 and (x1, y1) not in deny:
                x2, y2 = randDirect(x1, y1, dir)
                if x2 < 11 and x2 > 0 and y2 < 11 and y2 > 0 and (x2, y2) not in deny:
                    ships.append((x, y))
                    ships.append((x1, y1))
                    ships.append((x2, y2))
                    denyExtend(deny, x, y)
                    denyExtend(deny, x1, y1)
                    denyExtend(deny, x2, y2)

    # Четырехпалубный х 1
    while len(ships) < 20:
        x = random.randint(1, N)
        y = random.randint(1, N)
        if (x, y) in deny:
            continue

        for i in range(4):
            dir = random.randint(0, 3)
            x1, y1 = randDirect(x, y, dir)
            if x1 < 11 and x1 > 0 and y1 < 11 and y1 > 0 and (x1, y1) not in deny:
                x2, y2 = randDirect(x1, y1, dir)
                if x2 < 11 and x2 > 0 and y2 < 11 and y2 > 0 and (x2, y2) not in deny:
                    x3, y3 = randDirect(x2, y2, dir)
                    if x3 < 11 and x3 > 0 and y3 < 11 and y3 > 0 and (x3, y3) not in deny:
                        ships.append((x, y))
                        ships.append((x1, y1))
                        ships.append((x2, y2))
                        ships.append((x3, y3))
                        denyExtend(deny, x, y)
                        denyExtend(deny, x1, y1)
                        denyExtend(deny, x2, y2)
                        denyExtend(deny, x3, y3)


    if debug == True:
        printShips(ships, deny, N)
    return ships

def printShips(ships, N):
    for y in range(1, N + 1):
        for x in range(1, N + 1):
            if (x, y) in ships:
                print("[#]", end = "")
            else:
                print("[ ]", end = "")
        print()

def mapShips(player):
    shipStr = ""
    shipStr += " " * 3 + "A  B  C  D  E  F  G  H  I  J \n"
    for y in range(1, N + 1):
        shipStr += str(y - 1) + (" " if y < 11 else "")
        for x in range(1, N + 1):
            if (x, y) in server_ships[player]:
                if (x, y) in server_shoots[enemyPlayer(player)]:
                    shipStr += "\033[44m\033[31m{}\033[0m".format("[#]")
                else:
                    shipStr += "\033[44m\033[30m{}\033[0m".format("[#]")
            else:

                if (x, y) in server_shoots[enemyPlayer(player)]:
                    shipStr += "\033[44m\033[31m{}\033[0m".format(" + ")
                else:
                    shipStr += "\033[44m\033[34m{}\033[0m".format("[ ]")

        shipStr += "\033[0m" + "\n"
    return shipStr

def mapShoots(player):
    shootStr = ""
    shootStr += " " * 3 + "A  B  C  D  E  F  G  H  I  J \n"
    for y in range(1, N + 1):
        shootStr += str(y - 1) + (" " if y < 11 else "")
        for x in range(1, N + 1):
            if (x, y) in server_shoots[player]:
                if (x, y) in server_ships[enemyPlayer(player)]:
                    shootStr += "\033[44m\033[31m{}\033[0m".format("[*]")
                else:
                    shootStr += "\033[44m\033[31m{}\033[0m".format(" * ")
            else:
                shootStr += "\033[44m\033[34m{}\033[0m".format("[ ]")
        shootStr += "\033[0m" + "\n"
    return shootStr

def makeShoot(player, x, y):
    if (x, y) in server_shoots[player]:
        return 2
    server_shoots[player].append((x, y))
    if (x, y) in server_ships[enemyPlayer(player)]:
        return 1
    return 0

def denyExtend(deny, x, y):
    deny.extend(((x, y), (x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)))
    return

def randDirect(x, y, dir):
    randDirect = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
    return randDirect[dir]

def getFriendShips(player):
    if len(server_ships[player]) == 0:
        ships = genShips(N, debug)
        server_ships.insert(player, ships)
    return mapShips(player)

def enemyPlayer(player):
    return 1 if player == 2 else 2

def getEnemyShips(player):
    return mapShoots(player)


def mapStr(player, isVisibleShips = True):
    shipStr = ""
    for y in range(1, N + 1):
        for x in range(1, N + 1):
            if (x, y) in server_ships[player]:
                if (x, y) in server_shoots[enemyPlayer(player)]:
                    shipStr += "2" # попадание
                else:
                    if isVisibleShips == False:
                        shipStr += "0" # скрываем корабли противника
                    else:
                        shipStr += "1" # корабль
            else:

                if (x, y) in server_shoots[enemyPlayer(player)]:
                    shipStr += "3" # мимо
                else:
                    shipStr += "0" # море

    return shipStr