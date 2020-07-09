import pygame, config

class View:
    WIDTH = 800
    HEIGHT = 500
    MAP1_X = 80
    MAP2_X = 470
    MAP_Y = 70
    MAP_WIDTH = 250
    MAP_HEIGHT = 250

    BLACK = (0, 0, 0)

    # 0 - море
    # 1 - корабль
    # 2 - ранен
    # 3 - промах

    CURSOR_AIM_SIZE = (24, 24)
    CURSOR_AIM_HOTSPOT = (12, 12)
    CURSOR_AIM_ANDMASK = ( \
        0, 60, 0, 0, 60, 0, 0, 60, \
        0, 0, 255, 0, 1, 255, 128, 3, \
        189, 192, 7, 60, 224, 14, 60, 112, \
        28, 60, 56, 24, 0, 24, 255, 129, \
        255, 255, 129, 255, \
        255, 129, 255, 255, \
        129, 255, 24, 0, 24, 28, 60, 56, \
        14, 60, 112, 7, 60, 224, 3, 189, \
        192, 1, 255, 128, 0, 255, 0, 0, \
        60, 0, 0, 60, 0, 0, 60, 0, \
        )
    CURSOR_AIM_XORMASK = CURSOR_AIM_ANDMASK

    CURSOR_NORMAL_SIZE = (24, 24)
    CURSOR_NORMAL_HOTSPOT = (12, 12)
    CURSOR_NORMAL_ANDMASK = ( \
        0, 240, 0, 0, 144, 0, 0, 144, \
        0, 0, 144, 0, 0, 144, 0, 0, \
        144, 0, 0, 144, 0, 0, 159, 224, \
        0, 147, 56, 56, 147, 60, 108, 147, \
        52, 70, 147, 52, \
        99, 128, 52, 33, \
        128, 4, 49, 128, 4, 24, 0, 4, \
        12, 0, 4, 6, 0, 4, 2, 0, \
        4, 3, 0, 12, 1, 0, 56, 1, \
        0, 32, 1, 255, 224, 0, 0, 0, \
        )
    CURSOR_NORMAL_XORMASK = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(config.sounds["CODE_SEA"])
        pygame.mixer.music.play(loops=-1)
        self.__sf = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Battleship: StartGame")
        self.__font = pygame.font.SysFont("Arial", 15)

    def __drawCell(self, px, py, type):
        if type == 0:
            pygame.draw.rect(self.__sf, (0x00, 0xb4, 0xd8), (px, py, 25, 25))  # море
        if type == 1:
            self.__drawImage("ship", px, py)
        if type == 2:
            self.__drawImage("fire", px, py)
        if type == 3:
            self.__drawImage("splash", px, py)
        return

    def __drawImage(self, name, x, y):
        surf = pygame.image.load("images/" + name + ".bmp")
        rect = surf.get_rect(topleft=(x, y))
        self.__sf.blit(surf, rect)

    def drawMap(self, mx, my, map):
        text = self.__font.render("        A    B    C   D    E    F   G    H    I     J", 1, (0xff, 0xff, 0xff))
        place = text.get_rect(center=(mx + 108, my - 7))
        self.__sf.blit(text, place)

        for x in range(10):
            text = self.__font.render(str(x), 1, (0xff, 0xff, 0xff))
            place = text.get_rect(center=(mx - 10, my + x * 25 + 15))
            self.__sf.blit(text, place)

            for y in range(10):
                px, py = mx + x * 25, my + y * 25
                index = y * 10 + x
                type = int(map[index])
                self.__drawCell(px, py, type)
                pygame.draw.rect(self.__sf, (0, 0, 0), (px, py, 25, 25), 1)

            text = self.__font.render(str(x), 1, (0xff, 0xff, 0xff))
            place = text.get_rect(center=(mx + 260, my + x * 25 + 15))
            self.__sf.blit(text, place)

        text = self.__font.render("        A    B    C   D    E    F   G    H    I     J", 1, (0xff, 0xff, 0xff))
        place = text.get_rect(center=(mx + 108, my + 260))
        self.__sf.blit(text, place)

    def drawMessage(self, code="CODE_START"):
        message = config.messages[code]

        pygame.draw.rect(self.__sf, (0xc5, 0xc5, 0xc5), (80, 390, 620, 70))
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(message, 1, (0x27, 0x5d, 0x85))
        rect = text.get_rect(center=(390, 422))
        self.__sf.blit(text, rect)

    def drawGame(self, mapStr):
        self.drawMap(self.MAP1_X, self.MAP_Y, mapStr[:100])
        self.drawMap(self.MAP2_X, self.MAP_Y, mapStr[-100:])

    def getMapCoord(self, mouse_x, mouse_y):
        L = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

        if self.__isRangeMap(mouse_x, mouse_y):
            x = (mouse_x - self.MAP2_X) // 25
            y = (mouse_y - self.MAP_Y) // 25
            coord = L[x] + str(y)

            return coord
        return False

    def drawMouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.__isRangeMap(mouse_x, mouse_y):
            pygame.mouse.set_cursor(self.CURSOR_AIM_SIZE, self.CURSOR_AIM_HOTSPOT, self.CURSOR_AIM_ANDMASK,
                                    self.CURSOR_AIM_XORMASK)
        else:
            pygame.mouse.set_cursor(self.CURSOR_NORMAL_SIZE, self.CURSOR_NORMAL_HOTSPOT, self.CURSOR_NORMAL_ANDMASK,
                                    self.CURSOR_NORMAL_XORMASK)
        return

    def __isRangeMap(self, mouse_x, mouse_y):
        if mouse_x > self.MAP2_X and mouse_x < (self.MAP2_X + self.MAP_WIDTH) and mouse_y > self.MAP_Y and mouse_y < (self.MAP_Y + self.MAP_HEIGHT):
            return True
        return False

    def playSound(self, code):
        try:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(config.sounds[code]))
        except:
            pass
        return

    def clear(self):
        self.__sf.fill(self.BLACK)