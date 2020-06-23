import socket
from classes.player import Player

class Server:

    HOST = "localhost"
    PORT = 33333

    def __init__(self, isBotGame = True):
        self.players_ip = []
        self.isBotGame = isBotGame

        self.players = [0, 0]
        self.players[0] = Player(isBotGame)
        self.players[1] = Player(False)

        self.gameOver = False
        self.winStatus = 0
        self.runPlayer = 1

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.HOST, self.PORT))

        if self.isBotGame == True:
            self.players_ip.append("0.0.0.0")

        print("Слушаю порт: ", self.PORT)

        running = True
        while running:
            server.listen(2)
            sock, addr = server.accept()
            while True:
                data = sock.recv(1024)
                if not data:
                    break

                print("ПоЛуЧеНо оТ: ", addr, data.decode())
                if not self.__checkPlayer(addr):
                    break

                cmd = data.decode()
                res = self.__applyCmd(cmd)
                sock.send(str(res).encode())

            sock.close()

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

        return -1

    def __getMaps(self):
        return self.players[self.player].getMaps()

    def __getPingCode(self):
        if self.gameOver:
            return self.winStatus

        if self.__checkRunner():
            return 5

        if self.players[self.enemyPlayer].isBot:
            x, y = self.players[self.enemyPlayer].getXY()

            # shoot bot
            code = self.players[self.enemyPlayer].makeShoot(x, y, self.players[self.player])

            if code == 0:
                self.runPlayer = self.player

            if self.players[self.enemyPlayer].isWinner():
                self.gameOver = True
                self.winPlayer = self.enemyPlayer
                self.winStatus = 3

            return code + 10
        return 5

    def __getShootCode(self, cmd):
        if self.gameOver:
            return self.winStatus

        if not self.__checkRunner():
            return 15

        try:
            x, y = self.players[self.player].getXY(cmd)
        except:
            return -1

        # shoot
        code = self.players[self.player].makeShoot(x, y, self.players[self.enemyPlayer])

        if code == 0:
            self.runPlayer = self.enemyPlayer

        if self.players[self.player].isWinner():
            self.gameOver = True
            self.winPlayer = self.player
            self.winStatus = 4

        return code
