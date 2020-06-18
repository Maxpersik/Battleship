import pygame, battleship_ui as bsu, socket
import random

WIDTH = 800
HEIGHT = 500
FPS = 30

HOST = "localhost"
PORT = 33333


def sendServer(cmd):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    conn.send(cmd.encode())
    conn.settimeout(0.2)

    answer = ""

    try:
        while True:
            data = conn.recv(1024)
            answer += data.decode()
            #print(data.decode(), end='')
    except socket.timeout:
        pass

    conn.close()
    return answer


# Задаем цвета
BLACK = (0, 0, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/sea.mp3")
pygame.mixer.music.play(loops = -1)
sf = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battleship: StartGame")
clock = pygame.time.Clock()
sendServer("map")
mapStr = sendServer("mapstr")
bsu.drawGame(sf, mapStr)
mapRefresh = False
goal = True
answer = False

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                cmd = bsu.getMapCoord(event.pos[0], event.pos[1])
                if cmd:
                    answer = sendServer(cmd)
                    mapRefresh = True

    # Обновление
    if mapRefresh:
        sf.fill(BLACK)
        bsu.playSound(answer)
        mapStr = sendServer("mapstr")
        bsu.drawGame(sf, mapStr)
        mapRefresh = False
    bsu.drawMessage(sf, answer)
    bsu.drawMouse(sf)
    # Рендеринг




    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()