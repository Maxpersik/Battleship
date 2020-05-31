import battleship_map as bsm, random

botPlayer = 1
bot_shoots = []
def getShootBot(goal):
    while True:
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        if (x, y) not in bsm.server_shoots[botPlayer]:
            return x, y