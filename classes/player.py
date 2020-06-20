import random
from classes.map import Map

class Player:

    def __init__(self, isBot = False):
        self.isBot = isBot
        self.map = Map()

        self.deny_shoots = []
        self.target_ships = []
        self.count = 0
        self.lastGoal = False
        self.kills = 0

    def getMaps(self):
        return self.map.maps()

    def makeShoot(self, isGoal, x = 0, y = 0):
        if self.isBot:
            x, y = self.getBotShoot()
        if not self.map.isShoot(x, y, isGoal):
            return 2
        if isGoal:
            self.__setDeny(x, y)
            self.target_ships.append((x, y))
            self.lastGoal = True
            self.lastX, self.lastY = x, y
            self.kills += 1
            return 1
        self.lastGoal = False
        return 0

    def isGoal(self, x, y):
        if self.map.isShip(x, y):
            return True
        return False

    def getBotShoot(self):
        if len(self.target_ships) > 0:
            xg, yg = self.target_ships[0]
            if self.count == 0:
                self.count = 4

        if self.count > 0:
            if self.lastGoal == True and self.count < 4:
                xf, yf = xg + (xg - self.lastX), yg + (yg - self.lastY)
                count = 0
                if self.__isRange(xf, yf):
                    return xf, yf
            while count > 0:
                x, y = self.__randDirect(xg, yg, count - 1)
                count -= 1
                if count == 0:
                    self.target_ships.pop(0)
                if self.__isRange(x, y):
                    return x, y

        return self.getShootRandom()

    def getShootRandom(self):
        while True:
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            if self.__isRange(x, y):
                return x, y

    def __randDirect(self, x, y, dir):
        randDirect = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        return randDirect[dir]

    def __setDeny(self, x, y):
        self.deny_shoots.append(((x + 1), (y + 1)))
        self.deny_shoots.append(((x + 1), (y - 1)))
        self.deny_shoots.append(((x - 1), (y + 1)))
        self.deny_shoots.append(((x - 1), (y - 1)))

    def __isRange(self, x, y):
        if self.map.isShoot(x, y) and self.map.isMap(x, y) and (x, y) not in self.botDeny:
            return True
        return False

    def isWinner(self):
        if self.kills >= 20:
            return True
        return False