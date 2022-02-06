# Modules
import pygame
import sys
import random

# setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

# CONSTANTS
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 140
FPS = 60
BALL_SIZE = 30

BALL_SPEED_X = 7 * random.choice([-1, 1])
BALL_SPEED_Y = 7 * random.choice([-1, 1])
OPPONENT_SPEED = 7

BG_COLOR = pygame.Color('grey12')
LIGHT_GREY = (200, 200, 200)

# Game Rectangles
ball = pygame.Rect(SCREEN_WIDTH / 2 - BALL_SIZE / 2, SCREEN_HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)
player = pygame.Rect(10 , SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT)
opponent = pygame.Rect(SCREEN_WIDTH - PLAYER_WIDTH - 10, SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT)

# Game values
player_speed = 0

## Functions
def draw():
    global SCREEN_WIDTH, SCREEN_HEIGHT

    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, LIGHT_GREY, player)
    pygame.draw.rect(screen, LIGHT_GREY, opponent)
    pygame.draw.ellipse(screen, LIGHT_GREY, ball)
    pygame.draw.aaline(screen, LIGHT_GREY, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
    pygame.display.update()

def ball_animation():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        BALL_SPEED_Y *= -1
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_restart()
    
    if ball.colliderect(player) or ball.colliderect(opponent):
        BALL_SPEED_X *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT

def opponent_animation():
    if opponent.top < ball.y:
        opponent.top += OPPONENT_SPEED
    if opponent.bottom > ball.y:
        opponent.bottom -= OPPONENT_SPEED
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT

def ball_restart():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    BALL_SPEED_X *= random.choice([-1, 1])
    BALL_SPEED_Y *= random.choice([-1, 1])

# Game loop
isRunning = True
while isRunning:

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 7
            if event.key == pygame.K_DOWN:
                player_speed += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 7
            if event.key == pygame.K_DOWN:
                player_speed -= 7

    # Game logic
    ball_animation()
    player_animation()
    opponent_animation()

    # Drawing
    draw()

    # Framerate
    clock.tick(FPS)

