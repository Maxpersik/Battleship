import pygame, battleship_ui as bsu, socket
import random

WIDTH = 800
HEIGHT = 500
FPS = 30

HOST = "localhost"
PORT = 33333

MESSAGE_HIT = "Вы попали, стреляйте снова!!!"
MESSAGE_SPLASH = "Вы не попали, переход хода :("
MESSAGE_START = "Добро пожаловать в морской бой!!!"
MESSAGE_LOSE = "Вы проиграли ноликам и единичкам!!!"
MESSAGE_WIN = "Победа!!!"
MESSAGE_REPEAT = "Вы сюда уже стреляли"

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
bsu.drawMessage(sf, MESSAGE_START)
sendServer("map")
mapStr = sendServer("mapstr")
bsu.drawGame(sf, mapStr)
mapRefresh = False
goal = True

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
                    print(answer)
                    mapRefresh = True

    # Обновление

    # Рендеринг

    if mapRefresh:
        sf.fill(BLACK)
        if answer == "1":
            bsu.drawMessage(sf, MESSAGE_HIT)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("sounds/hit.wav"))
        if answer == "0":
            bsu.drawMessage(sf, MESSAGE_SPLASH)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("sounds/splash.wav"))
        if answer == "2":
            bsu.drawMessage(sf, MESSAGE_REPEAT)
        if answer == "3":
            bsu.drawMessage(sf, MESSAGE_LOSE)
        if answer == "4":
            bsu.drawMessage(sf, MESSAGE_WIN)

        mapStr = sendServer("mapstr")
        print(answer)
        bsu.drawGame(sf, mapStr)
        mapRefresh = False

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()