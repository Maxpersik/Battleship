import pygame, config
from classes.client import Client
from classes.view import View

class Game:
    FPS = config.game["fps"]

    def __init__(self, server_host, server_port):
        self.__clock = pygame.time.Clock()
        self.client = Client(server_host, server_port)
        self.view = View()

    def run(self):
        mapStr = self.client.sendServer("maps")
        self.view.drawGame(mapStr)
        mapRefresh = False
        answer = "CODE_START"
        count = 0

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
                            self.view.playSound(answer)
                            mapRefresh = True
                            count = 0

            # Проверить ход соперника
            count += 1
            if count == self.FPS * 3:
                answer = self.client.sendServer("ping")
                self.view.playSound(answer)
                mapRefresh = True
                count = 0

            # Обновление
            if mapRefresh:
                self.view.clear()
                mapStr = self.client.sendServer("maps")
                self.view.drawGame(mapStr)
                mapRefresh = False

            self.view.drawMessage(answer)
            self.view.drawMouse()
            # Рендеринг

            # После отрисовки всего, переворачиваем экран
            pygame.display.flip()

        pygame.quit()
        self.client.sendServer("quit")
