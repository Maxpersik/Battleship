import random

class Map:
    N = 10

    def __init__(self, debug = False):
        self.debug = debug
        self.ships = []
        self.shoots = []
        self.deny = []
        self.enemy_ships = []
        self.enemy_shoots = []

        self.genShips()

    def genShips(self):
        # Однопалубные корабли х 4
        while len(self.ships) < 4:
            x = random.randint(1, self.N)
            y = random.randint(1, self.N)
            if (x, y) in self.deny:
                continue
            self.ships.append((x, y))
            self.__denyExtend(x, y)

        # Двухпалубные корабли х 3
        while len(self.ships) < 10:
            x = random.randint(1, self.N)
            y = random.randint(1, self.N)
            if (x, y) in self.deny:
                continue
            self.ships.append((x, y))
            for i in range(4):
                dir = random.randint(0, 3)
                x1, y1 = self.__randDirect(x, y, dir)
                if x1 < 11 and x1 > 0 and y1 < 11 and y1 > 0 and (x1, y1) not in self.deny:
                    self.ships.append((x1, y1))
                    break
            self.__denyExtend(x, y)
            self.__denyExtend(x1, y1)

        # Трехпалубные корабли
        while len(self.ships) < 16:
            x = random.randint(1, self.N)
            y = random.randint(1, self.N)
            if (x, y) in self.deny:
                continue

            for i in range(4):
                dir = random.randint(0, 3)
                x1, y1 = self.__randDirect(x, y, dir)
                if x1 < 11 and x1 > 0 and y1 < 11 and y1 > 0 and (x1, y1) not in self.deny:
                    x2, y2 = self.__randDirect(x1, y1, dir)
                    if x2 < 11 and x2 > 0 and y2 < 11 and y2 > 0 and (x2, y2) not in self.deny:
                        self.ships.append((x, y))
                        self.ships.append((x1, y1))
                        self.ships.append((x2, y2))
                        self.__denyExtend(x, y)
                        self.__denyExtend(x1, y1)
                        self.__denyExtend(x2, y2)

        # Четырехпалубный х 1
        while len(self.ships) < 20:
            x = random.randint(1, self.N)
            y = random.randint(1, self.N)
            if (x, y) in self.deny:
                continue

            for i in range(4):
                dir = random.randint(0, 3)
                x1, y1 = self.__randDirect(x, y, dir)
                if x1 < 11 and x1 > 0 and y1 < 11 and y1 > 0 and (x1, y1) not in self.deny:
                    x2, y2 = self.__randDirect(x1, y1, dir)
                    if x2 < 11 and x2 > 0 and y2 < 11 and y2 > 0 and (x2, y2) not in self.deny:
                        x3, y3 = self.__randDirect(x2, y2, dir)
                        if x3 < 11 and x3 > 0 and y3 < 11 and y3 > 0 and (x3, y3) not in self.deny:
                            self.ships.append((x, y))
                            self.ships.append((x1, y1))
                            self.ships.append((x2, y2))
                            self.ships.append((x3, y3))
                            self.__denyExtend(x, y)
                            self.__denyExtend(x1, y1)
                            self.__denyExtend(x2, y2)
                            self.__denyExtend(x3, y3)

        if self.debug == True:
            self.printShips()
        return

    def printShips(self):
        for y in range(1, self.N + 1):
            for x in range(1, self.N + 1):
                if (x, y) in self.ships:
                    print("[#]", end="")
                else:
                    print("[ ]", end="")
            print()

    def __denyExtend(self, x, y):
        self.deny.extend(((x, y), (x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)))
        return

    def __randDirect(self, x, y, dir):
        randDirect = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        return randDirect[dir]

    def maps(self):
        shipStr = ""
        for y in range(1, self.N + 1):
            for x in range(1, self.N + 1):
                if (x, y) in self.ships:
                    if (x, y) in self.enemy_shoots:
                        shipStr += "2"  # попадание
                    else:
                        shipStr += "1"  # корабль
                else:
                    if (x, y) in self.enemy_shoots:
                        shipStr += "3"  # мимо
                    else:
                        shipStr += "0"  # море

        for y in range(1, self.N + 1):
            for x in range(1, self.N + 1):
                if (x, y) in self.shoots:
                    if (x, y) in self.enemy_ships:
                        shipStr += "2"  # попадание
                    else:
                        shipStr += "3"  # мимо
                else:
                    shipStr += "0"  # море

        return shipStr

    def isShip(self, x, y):
        if (x, y) in self.enemy_shoots:
            return False
        self.enemy_shoots.append((x, y))
        if (x, y) in self.ships:
            return True
        return False

    def isShoot(self, x, y, isGoal):
        if (x, y) in self.shoots:
            return False
        self.shoots.append((x, y))
        if isGoal:
            self.enemy_ships.append((x, y))
        return True

    def isMap(self, x, y):
        if x < self.N + 1 and x > 0 and y < self.N + 1 and y > 0:
            return True

