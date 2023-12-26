import random
import sys
import pygame
from pygame.locals import *

FPS = 32
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND_Y = SCREEN_HEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
BASE = 'gallery/sprites/base.png'
PIPE = 'gallery/sprites/pipe.png'


def welcomeScreen():
    playerx = int(SCREEN_WIDTH / 5)
    playery = int((SCREEN_HEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    welcomex = int((SCREEN_WIDTH - GAME_SPRITES['welcome'].get_width()) / 2)
    welcomey = int((SCREEN_HEIGHT * 0.13))
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['welcome'], (welcomex, welcomey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUND_Y))
                pygame.display.update()
                FPS_CLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREEN_WIDTH / 5)
    playery = int(SCREEN_HEIGHT / 2)
    basex = 0

    newPipe1 = get_random_pipe()
    newPipe2 = get_random_pipe()

    upper_pipes = [
        {'x': SCREEN_WIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH / 2), 'y': newPipe2[0]['y']}
    ]
    lower_pipes = [
        {'x': SCREEN_WIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH / 2), 'y': newPipe2[1]['y']}
    ]
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    # playerMinVelY = -8
    playerAccY = 1

    playerFlapAccVel = -8
    playerFlapped = False  # it is True only when bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccVel
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upper_pipes, lower_pipes)

        if crashTest:
            return
        player_mid_position = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upper_pipes:
            pipe_mid_position = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipe_mid_position <= player_mid_position < pipe_mid_position + 4:
                score += 1
                print(f'Your Score is {score}')
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUND_Y - playery - playerHeight)

        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipeVelX
            lower_pipe['x'] += pipeVelX

        if 0 < upper_pipes[0]['x'] < 5:
            new_pipe = get_random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])

        if upper_pipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lower_pipe['x'], lower_pipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREEN_WIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREEN_HEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def isCollide(playerx, playery, upper_pipes, lower_pipes):
    if playery > GROUND_Y - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upper_pipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lower_pipes:
        if playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < \
                GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def get_random_pipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREEN_HEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREEN_HEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREEN_WIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper pipe
        {'x': pipeX, 'y': y2}
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()

    FPS_CLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

    GAME_SPRITES['welcome'] = pygame.image.load('gallery/sprites/welcome.png').convert_alpha()

    GAME_SPRITES['base'] = (pygame.image.load(BASE).convert_alpha())

    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
