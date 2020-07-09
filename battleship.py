import threading, sys
from classes.game import Game
from classes.server import Server

def startServer(isBotGame=True):
    server = Server(isBotGame)
    server.run()

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            startServer(False)
        if sys.argv[1] == "client":
            game = Game(sys.argv[2])
            game.run()
    else:
        threading.Thread(target=startServer).start()

        game = Game()
        game.run()

if __name__ == "__main__":
    main()



