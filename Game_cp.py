# Pygame шаблон - скелет для нового проекта Pygame
import pygame
from random import randint

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

# ОКНО
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption('Kitty Go!')
pygame.display.set_icon(pygame.image.load('images/icon.png'))


font1 = pygame.font.SysFont('impact', 30)
font2 = pygame.font.Font(None, 80)


# ИЗОБРАЖЕНИЯ
imgBG = pygame.image.load('images/background.png')
imgBird = pygame.image.load('images/bird.png')
imgPT = pygame.image.load('images/pipe_top.png')
imgPB = pygame.image.load('images/pipe_bottom.png')

# МУЗЫКА
pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

sndFall = pygame.mixer.Sound('sounds/fall.wav')
sndFall.set_volume(0.5)

sndGameOver = pygame.mixer.Sound('sounds/game_over.wav')
sndGameOver.set_volume(0.7)


# ПЕРЕМЕННЫЕ
py = HEIGHT // 2  # перемещение по y
sy = 0  # направление движения вверх или вниз (скорость движения)
ay = 0  # ускорение (меняется от нажатия кнопки мыши)
player = pygame.Rect(WIDTH // 3, py, 34, 24)
frame = 0


frame = 0

state = 'start'
timer = 10

pipes = []  # трубы
bges = []
pipesScores = []

pipeSpeed = 3
pipeGateSize = 250
pipeGatePos = HEIGHT // 2   # ширина прохода

bges.append(pygame.Rect(0, 0, 288, 600))

lives = 3
scores = 0

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



# Цикл игры
play = True
while play:
    # Держим цикл на правильной скорости
    # clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            play = False

    # УПРАВЛЕНИЕ КЛАВИШАМИ
    press = pygame.mouse.get_pressed()  # состояние всех кнопок мыши
    keys = pygame.key.get_pressed()  # состояние кнопок клавиатуры
    click = press[0] or keys[pygame.K_SPACE]  # когда нажата клавиша, то меняется ускорение

    if timer > 0:
        timer -= 1

    frame = (frame + 0.2) % 4


    # ДВИЖЕНИЕ ТРУБ
    for i in range(len(bges) - 1, -1, -1):
        bg = bges[i]
        bg.x -= pipeSpeed // 2

        if bg.right < 0:
            bges.remove(bg)

        if bges[len(bges)-1].right <= WIDTH:
            bges.append(pygame.Rect(bges[len(bges)-1].right, 0, 288, 600))

    for i in range(len(pipes) - 1, -1, -1):
        pipe = pipes[i]
        pipe.x -= pipeSpeed

        if pipe.right < 0:
            pipes.remove(pipe)
            if pipe in pipesScores:
                pipesScores.remove(pipe)


    # СОСТОЯНИЯ ИГРЫ
    if state == 'start':

        if click and timer == 0 and len(pipes) == 0:
            state = 'play'

        py += (HEIGHT // 2 - py) * 0.1
        player.y = py

    # СОСТОЯНИЕ PLAY
    elif state == 'play':
        # когда нажата клавиша, то меняется ускорение
        if click:
            ay = -2
        else:
            ay = 0

        # МЕХАНИКА ПАДЕНИЯ
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        # ДОБАВЛЕНИЕ ТРУБ
        if len(pipes) == 0 or pipes[len(pipes) - 1].x < WIDTH - 200:
            # Появится в (место, место, ширина трубы, высота трубы)
            pipes.append(pygame.Rect(WIDTH, 0, 52, pipeGatePos - pipeGateSize // 2))  # верхняя труба
            pipes.append(pygame.Rect(WIDTH, pipeGatePos + pipeGateSize // 2, 52, HEIGHT - pipeGatePos + pipeGateSize // 2))  # нижняя труба

            pipeGatePos += randint(-100, 100)
            if pipeGatePos < pipeGateSize:
                pipeGatePos = pipeGateSize
            elif pipeGatePos > HEIGHT - pipeGateSize:
                pipeGatePos = HEIGHT - pipeGateSize

        # top - верхняя граница, bottom - нижняя границы
        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'

        # ПРОВЕРКА НА СТОЛКНОВЕНИЕ КОТА С ТРУБАМИ
        for pipe in pipes:
            if player.colliderect(pipe):
                state = 'fall'

            if pipe.right < player.left and pipe not in pipesScores:

                pipesScores.append(pipe)
                scores += 5
                pipeSpeed = 3 + scores // 100

    elif state == 'fall':
        sndFall.play()
        sy, ay = 0, 0
        pipeGatePos = HEIGHT // 2

        lives -= 1
        if lives > 0:
            state = 'start'
            timer = 60
        else:
            state = 'game over'
            timer = 240

    # game over
    else:
        sndGameOver.play()
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if timer == 0:
            lives = 4  # НЕВЕРНО!!!
            scores = -10  # НЕВЕРНО!!!
            state = 'play'

    # ОТРИСОВКА
    for bg in bges:
        window.blit(imgBG, bg)

    # ОТРИСОВКА ТРУБ (перед отрисовкой кота, чтоб кот был на переднем плане)
    for pipe in pipes:
        # pygame.draw.rect(window, pygame.Color('red'), pipe)
        if pipe.y == 0:  #значит верхняя труба
            rect = imgPT.get_rect(bottomleft = pipe.bottomleft)
            window.blit(imgPT, rect)
        else:
            rect = imgPB.get_rect(topleft = pipe.topleft)
            window.blit(imgPB, rect)


    image = imgBird.subsurface(68 * int(frame), 0, 68, 48)
    image = pygame.transform.rotate(image, -sy * 2)
    window.blit(image, player)

    text = font1.render('Очки: ' + str(scores), 0, pygame.Color('black'))
    window.blit(text, (10,10))

    text = font1.render('Жизни: ' + str(lives), 0, pygame.Color('black'))
    window.blit(text, (10, 50))


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
