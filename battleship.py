import threading, sys, config
from classes.game import Game
from classes.server import Server

# Запуск сервера
def startServer():
    server = Server()
    server.run()

# Начало игры
def startGame():
    if config.conn["server"]:
        threading.Thread(target=startServer).start()

    host = config.conn["host"]
    port = config.conn["port"]

    game = Game(host, port)
    game.run()

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        config.game["bots"] = 0

    if len(sys.argv) > 2 and sys.argv[1] == "client":
        config.conn["server"] = False
        config.conn["host"] = sys.argv[2]

    startGame()

if __name__ == "__main__":
    main()



