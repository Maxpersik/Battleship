import socket
from classes.player import Player

class Server:

    HOST = "localhost"
    PORT = 33333

    def __init__(self, isBotGame = True):
        self.players_ip = []
        self.isBotGame = isBotGame

        self.players = [0, 0]
        self.players[0] = Player(False)
        self.players[1] = Player(False)

        self.gameOver = False
        self.winPlayer = 0
        self.runPlayer = 0

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.HOST, self.PORT))

        if self.isBotGame == True:
            self.players_ip.append("0.0.0.0")

        running = True
        while running:
            print("Слушаю порт: ", self.PORT)
            server.listen(2)
            sock, addr = server.accept()
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                # print("ПоЛуЧеНо оТ: ", addr, data.decode())
                player = self.__checkClient(addr)
                if not player:
                    break

                cmd = data.decode()
                res = self.__applyCmd(cmd, player)
                sock.send(str(res).encode())

            sock.close()


    def __getXY(self, cmd):
        L = "ABCDEFGHIJ"
        x = int(L.index(cmd[0:1])) + 1
        y = int(cmd[1:2]) + 1
        return x, y

    def __checkClient(self, addr):
        ip = addr[0]
        if ip not in self.players_ip and len(self.players_ip) > 2:
            return False
        if ip not in self.players_ip:
            self.players_ip.append(ip)
        return self.players_ip.index(ip)

    def __applyCmd(self, cmd, player):
        if cmd == "maps":
            return self.players[player].getMaps()

        if len(cmd) == 2:
            try:
                x, y = self.__getXY(cmd)
            except:
                return -1

            return self.__getCode(x, y, player)
        return -1

    def __getCode(self, x, y, player):
        enemyPlayer = self.__enemyPlayer(player)

        if self.players[player].isWinner():
            self.gameOver = True
            self.winPlayer = player
            return 4
        if self.players[enemyPlayer].isWinner():
            self.gameOver = True
            self.winPlayer = enemyPlayer
            return 3

        isGoal = self.players[enemyPlayer].isGoal(x, y)
        code = self.players[player].makeShoot(isGoal, x, y)
        if isGoal:
            self.runPlayer = player
        else:
            self.runPlayer = enemyPlayer
        return code

    def __enemyPlayer(self, player):
        return not player

    # def enemyPlayer(self):
    #     return 1 if self.player == 2 else 2