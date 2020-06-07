import battleship_map as bsm, random

botPlayer = 1
count = 0
xg, yg = 0, 0
botDeny = []
botTarget = []

def getShootBot(goal, x, y):
    global count, xg, yg, botTarget

    if goal == True:
        setDeny(x, y)
        botTarget.append((x, y))

    if len(botTarget) > 0:
        xg, yg = botTarget[0]
        if count == 0:
            count = 4

    if count > 0:
        if goal == True and count < 4:
            xf, yf = xg + (xg - x), yg + (yg - y)
            count = 0
            if isRange(xf, yf):
                return xf, yf
        while count > 0:
            x, y = randDirect(xg, yg, count - 1)
            count -= 1
            if count == 0:
                botTarget.pop(0)
                print(botTarget)
            if isRange(x, y):
                return x, y


    return getShootRandom()

def getShootRandom():
    while True:
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        if isRange(x, y):
            return x, y

def isRange(x, y):
    if (x, y) not in bsm.server_shoots[botPlayer] and (x < 11 and x > 0 and y < 11 and y > 0) and (x, y) not in botDeny:
        return True
    return False

def randDirect(x, y, dir):
    randDirect = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
    return randDirect[dir]

def setDeny(x, y):
    botDeny.append(((x + 1), (y + 1)))
    botDeny.append(((x + 1), (y - 1)))
    botDeny.append(((x - 1), (y + 1)))
    botDeny.append(((x - 1), (y - 1)))