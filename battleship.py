import threading
from classes.game import Game
from classes.server import Server

SERVER_HOST = "localhost"

def startServer():
    isBotGame = True
    server = Server(isBotGame)
    server.run()

if SERVER_HOST == "localhost":
    threading.Thread(target=startServer).start()

game = Game(SERVER_HOST)
game.run()




