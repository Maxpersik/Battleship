import pygame
from classes.client import Client
from classes.view import View

class Game:
    FPS = 30

    HOST = "localhost"
    PORT = 33333

    def __init__(self):
        self.__clock = pygame.time.Clock()
        self.client = Client(self.HOST, self.PORT)
        self.view = View()

    def run(self):

        self.client.sendServer("map")
        mapStr = self.client.sendServer("mapstr")
        self.view.drawGame(mapStr)
        mapRefresh = False
        answer = False

        running = True
        while running:
            # Держим цикл на правильной скорости
            self.__clock.tick(self.FPS)
            # Ввод процесса (события)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        cmd = self.view.getMapCoord(event.pos[0], event.pos[1])
                        if cmd:
                            answer = self.client.sendServer(cmd)
                            mapRefresh = True

            # Обновление
            if mapRefresh:
                self.view.clear()
                self.view.playSound(answer)
                mapStr = self.client.sendServer("mapstr")
                self.view.drawGame(mapStr)
                mapRefresh = False
            self.view.drawMessage(answer)
            self.view.drawMouse()
            # Рендеринг

            # После отрисовки всего, переворачиваем экран
            pygame.display.flip()

        pygame.quit()