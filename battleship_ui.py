import pygame, random, sys

sf = 0



def startDisplay():
    global sf
    pygame.init()
    sf = pygame.display.set_mode([800, 500])
    drawMessage("Добро пожаловать в морской бой!!!")
    pygame.display.update()
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    # pygame.display.flip()
    #
    # pygame.quit()
# 0 - море
# 1 - корабль
# 2 - ранен
# 3 - промах

def drawCell(px, py, type):
    if type == 0:
        pygame.draw.rect(sf, (0x00, 0xb4, 0xd8), (px, py, 25, 25))  # море
    if type == 1:
        pygame.draw.rect(sf, (0x77, 0x49, 0x36), (px, py, 25, 25))  # корабль
    if type == 2:
        pygame.draw.rect(sf, (0xbc, 0x39, 0x08), (px, py, 25, 25))#ранен
        # pygame.draw.line(sf, (0x00, 0xb4, 0xd8), [px + 1, py], [px + 2, py + 3], 3)
        # pygame.draw.line(sf, (0x00, 0xb4, 0xd8), [px + 2, px + 3], [px + 5, py + 2], 2)
        # pygame.draw.line(sf, (0x00, 0xb4, 0xd8), [px + 5, py + 3], [px + 5, py + 9], 2)
        # pygame.draw.line(sf, (0x00, 0xb4, 0xd8), [px + 5, py + 9], [px + 10, py + 9], 3)
        # pygame.draw.line(sf, (0x00, 0xb4, 0xd8), [px + 10, py + 9], [px + 10, py + 13], 3)
        # pygame.draw.line(sf, (0x00, 0xb4, 0xd8), [px + 10, py + 13], [px + 10, py + 17], 2)
        # pygame.draw.line(sf, (0x00, 0xb4, 0xd8), [px + 10, py + 17], [px + 13, py + 17], 2)
        # pygame.draw.line(sf, (0x00, 0xb4, 0xd8), [px + 13, py + 17], [px + 13, py + 20], 3)
        # pygame.draw.line(sf, (0x00, 0xb4, 0xd8), [px + 13, py + 20], [px + 18, py + 20], 3)
        # pygame.draw.line(sf, (0x00, 0xb4, 0xd8), [px + 18, py + 20], [px + 22, py + 20], 2)
        # pygame.draw.line(sf, (0x00, 0xb4, 0xd8), [px + 22, py + 20], [px + 22, py + 24], 3)
    if type == 3:
        pygame.draw.rect(sf, (0x00, 0xb4, 0xd8), (px, py, 25, 25))
        pygame.draw.rect(sf, (0x94, 0x1b, 0x0c), (px + 7, py + 7, 11, 11))  # промах
    return

def drawMap(mx, my, map):

    # text
    font = pygame.font.Font(None, 23)
    text = font.render("         A    B    C   D    E    F   G    H    I     J", 1, (0xff, 0xff, 0xff))
    place = text.get_rect(center=(mx + 108, my - 7))
    sf.blit(text, place)

    for x in range(10):

        font = pygame.font.Font(None, 23)
        text = font.render(str(x), 1, (0xff, 0xff, 0xff))
        place = text.get_rect(center=(mx - 10, my + x * 25 + 15))
        sf.blit(text, place)

        for y in range(10):
            px, py = mx + x * 25, my + y * 25
            #type = random.randint(0, 3)
            index = y * 10 + x
            type = int(map[index])
            drawCell(px, py, type)
            pygame.draw.rect(sf, (0, 0, 0), (px, py, 25, 25), 1)

        font = pygame.font.Font(None, 23)
        text = font.render(str(x), 1, (0xff, 0xff, 0xff))
        place = text.get_rect(center=(mx + 260, my + x * 25 + 15))
        sf.blit(text, place)

    font = pygame.font.Font(None, 23)
    text = font.render("         A    B    C   D    E    F   G    H    I     J", 1, (0xff, 0xff, 0xff))
    place = text.get_rect(center=(mx + 108, my + 260))
    sf.blit(text, place)

def drawMessage(text):
    pygame.draw.rect(sf, (0xc5, 0xc5, 0xc5), (80, 390, 620, 70))
    font = pygame.font.Font(None, 45)
    text = font.render(text, 1, (0x27, 0x5d, 0x85))
    place = text.get_rect(center=(390, 420))
    sf.blit(text, place)

def drawGame(mapStr):
    map1 = mapStr[:100]
    map2 = mapStr[-100:]

    drawMap(80, 70, map1)
    drawMap(450, 70, map2)
    pygame.display.update()







