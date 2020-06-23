import random
from classes.map import Map

class Player:

    def __init__(self, isBot = False):
        self.isBot = isBot
        self.map = Map()
        self.deny_shoots = []
        self.target_ships = []
        self.kills = 0

    def getMaps(self):
        return self.map.maps()

    def getXY(self, cmd=False):
        if self.isBot:
            return self.getBotShoot()
        return self.map.getXY(cmd)

    def makeShoot(self, x, y, enemyPlayer):
        if not self.map.isShoot(x, y):
            return 2

        isGoal = enemyPlayer.isGoal(x, y)
        self.map.saveShoot(x, y, isGoal)
        enemyPlayer.map.saveEnemyShoot(x, y)

        if isGoal:
            self.__setDeny(x, y)
            self.target_ships.append((x, y))
            self.kills += 1
            return 1

        return 0

    def isGoal(self, x, y):
        if self.map.isShip(x, y):
            return True
        return False

    def getBotShoot(self):
        while len(self.target_ships) > 0:
            xg, yg = self.target_ships[0]

            for i in range(4):
                x, y = self.__randDirect(xg, yg, i)
                if self.isRange(x, y):
                    return x, y
            self.target_ships.pop(0)

        return self.getRandomShoot()

    def getRandomShoot(self):
        while True:
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            if self.isRange(x, y):
                return x, y

    def __randDirect(self, x, y, dir):
        randDirect = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        return randDirect[dir]

    def __setDeny(self, x, y):
        self.deny_shoots.append(((x + 1), (y + 1)))
        self.deny_shoots.append(((x + 1), (y - 1)))
        self.deny_shoots.append(((x - 1), (y + 1)))
        self.deny_shoots.append(((x - 1), (y - 1)))

    def isRange(self, x, y):
        if self.map.isShoot(x, y) and self.map.isMap(x, y) and (x, y) not in self.deny_shoots:
            return True
        return False

    def isWinner(self):
        if self.kills >= 20:
            return True
        return False