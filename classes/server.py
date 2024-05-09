import socket, sys, config, pickle
from classes.player import Player

class Server:

    def __init__(self):
        self.players_ip = []
        self.botCount = config.game["bots"]

        self.players = [0, 0]
        self.players[0] = Player(True if self.botCount > 0 else False)
        self.players[1] = Player(True if self.botCount > 1 else False)

        self.gameOver = False
        self.winStatus = 0
        self.runPlayer = 0

        self.HOST = config.conn["host"]
        self.PORT = config.conn["port"]

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.HOST, self.PORT))

        if self.botCount > 0:
            self.players_ip.append("0.0.0.0")

        print("Слушаю порт: ", self.PORT)

        if config.game["autosave"] == 1:
            self.autoLoad()

        running = True
        while running:
            server.listen(2)
            sock, addr = server.accept()
            while True:
                data = sock.recv(1024)
                if not data:
                    break

                print("ПоЛуЧеНо оТ: ", addr, data)

                if not self.__checkPlayer(addr):
                    break

                cmd = data.decode()
                if cmd == "quit" and self.player == 0:
                    running = False
                    break

                res = self.__applyCmd(cmd)
                sock.send(str(res).encode())

                if config.game["autosave"] == 1:
                    self.autoSave()

        sock.close()
        sys.exit()

    def __checkPlayer(self, addr):
        ip = addr[0]
        if ip not in self.players_ip and len(self.players_ip) > 2:
            return False
        if ip not in self.players_ip:
            self.players_ip.append(ip)
        self.player = self.players_ip.index(ip)
        self.enemyPlayer = 0 if self.player == 1 else 1
        return True

    def __checkRunner(self):
        if self.runPlayer != self.player:
            return False
        return True

    def __applyCmd(self, cmd):
        if cmd == "maps":
            return self.__getMaps()

        if cmd == "ping":
            return self.__getPingCode()

        if len(cmd) == 2:
            return self.__getShootCode(cmd)

        return config.codes["CODE_ERROR"]

    def __getMaps(self):
        return self.players[self.player].getMaps()

    def __getPingCode(self):
        if self.gameOver:
            return self.winStatus

        if self.botCount < 2 and self.__checkRunner():
            return config.codes["CODE_RUN"]

        if self.__checkRunner():
            if self.players[self.player].isBot:
                x, y = self.players[self.player].getXY()

                # shoot bot
                goal = self.players[self.player].makeShoot(x, y, self.players[self.enemyPlayer])

                if goal == 0:
                    self.runPlayer = self.enemyPlayer
            return self.__getCode(goal, False)

        if self.players[self.enemyPlayer].isBot:
            x, y = self.players[self.enemyPlayer].getXY()

            # shoot bot
            goal = self.players[self.enemyPlayer].makeShoot(x, y, self.players[self.player])

            if goal == 0:
                self.runPlayer = self.player

            if self.players[self.enemyPlayer].isWinner():
                self.gameOver = True
                self.winPlayer = self.enemyPlayer
                self.winStatus = config.codes["CODE_LOSE"]

            return self.__getCode(goal, True)
        return config.codes["CODE_RUN"]

    def __getShootCode(self, cmd):
        if self.gameOver:
            return self.winStatus

        if not self.__checkRunner():
            return config.codes["CODE_ENEMY_RUN"]

        try:
            x, y = self.players[self.player].getXY(cmd)
        except:
            return config.codes["CODE_ERROR"]

        # shoot
        goal = self.players[self.player].makeShoot(x, y, self.players[self.enemyPlayer])

        if goal == 0:
            self.runPlayer = self.enemyPlayer

        if self.players[self.player].isWinner():
            self.gameOver = True
            self.winPlayer = self.player
            self.winStatus = config.codes["CODE_WIN"]

        return self.__getCode(goal, False)

    def __getCode(self, goal, isEnemyPlayer):
        codes = ["CODE_SPLASH", "CODE_HIT", "CODE_REPEAT", "CODE_ENEMY_SPLASH", "CODE_ENEMY_HIT", "CODE_ENEMY_REPEAT"]
        index = goal + 3 if isEnemyPlayer else goal
        return codes[index]

    def autoSave(self):
        with open("autosave/game.dat", "wb") as file:
            pickle.dump(
                [self.players[0].map.getData(), self.players[1].map.getData(),
                 [self.gameOver, self.winStatus, self.runPlayer],
                 [self.players[0].kills, self.players[1].kills]],
            file)

    def autoLoad(self):
        try:
            with open("autosave/game.dat", "rb") as file:
                unpickled = pickle.load(file)
                if unpickled[2][0] == True: # Game over
                    return
                self.players[0].map.setData(unpickled[0])
                self.players[1].map.setData(unpickled[1])
                self.gameOver = unpickled[2][0]
                self.winStatus = unpickled[2][1]
                self.runPlayer = unpickled[2][2]
                self.players[0].kills = unpickled[3][0]
                self.players[1].kills = unpickled[3][1]
        except:
            print("No data file")
