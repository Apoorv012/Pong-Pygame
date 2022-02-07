# Modules
import pygame
import sys
import random

# setup
pygame.init()
clock = pygame.time.Clock()

# CONSTANTS
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 140
FPS = 60
BALL_SIZE = 30

OPPONENT_SPEED = 7

BG_COLOR = pygame.Color('grey12')
LIGHT_GREY = (200, 200, 200)

FONT_SIZE = 32
GAME_FONT = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
PAUSE_FONT = pygame.font.Font("freesansbold.ttf", FONT_SIZE * 2)

# Setting up the main window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

# Game Rectangles
ball = pygame.Rect(SCREEN_WIDTH / 2 - BALL_SIZE / 2, SCREEN_HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)
player = pygame.Rect(10 , SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT)
opponent = pygame.Rect(SCREEN_WIDTH - PLAYER_WIDTH - 10, SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT)

# Game variables
ball_speed_x = 7 * random.choice([-1, 1])
ball_speed_y = 7 * random.choice([-1, 1])
player_speed = 0
player_score = 0
opponent_score = 0
isPaused = False
stopTick = None
currentTick = None

## Functions
def draw():
    global SCREEN_WIDTH, SCREEN_HEIGHT

    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, LIGHT_GREY, player)
    pygame.draw.rect(screen, LIGHT_GREY, opponent)
    pygame.draw.ellipse(screen, LIGHT_GREY, ball)
    pygame.draw.aaline(screen, LIGHT_GREY, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))

    player_score_text = GAME_FONT.render(f"{player_score}", False, LIGHT_GREY)
    screen.blit(player_score_text, (SCREEN_WIDTH / 2 - player_score_text.get_width() / 2 - 40, SCREEN_HEIGHT / 2 - FONT_SIZE / 2))

    opponent_score_text = GAME_FONT.render(f"{opponent_score}", False, LIGHT_GREY)
    screen.blit(opponent_score_text, (SCREEN_WIDTH / 2 - opponent_score_text.get_width() / 2 + 40, SCREEN_HEIGHT / 2 - FONT_SIZE / 2))

    if isPaused:
        pause_text = PAUSE_FONT.render("PAUSED", False, LIGHT_GREY)
        screen.blit(pause_text, (SCREEN_WIDTH / 2 - pause_text.get_width() / 2, SCREEN_HEIGHT / 2 - FONT_SIZE / 2 - 100))

    pygame.display.update()

def ball_animation():
    global ball_speed_x, ball_speed_y, opponent_score, player_score, isPaused, stopTick
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1
    if ball.left <= 0:
        opponent_score += 1
        stopTick = pygame.time.get_ticks()
        isPaused = True
    if ball.right >= SCREEN_WIDTH:
        player_score += 1
        stopTick = pygame.time.get_ticks()
        isPaused = True
    
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT

def opponent_animation():
    if opponent.top < ball.top:
        opponent.top += OPPONENT_SPEED
    if opponent.bottom > ball.bottom:
        opponent.bottom -= OPPONENT_SPEED
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])

def countdown_timer():
    global isPaused, stopTick, currentTick
    currentTick = pygame.time.get_ticks()
    if currentTick - stopTick > 2000:
        ball_restart()
        isPaused = False

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
    if not isPaused:
        ball_animation()
    else:
        countdown_timer()

    player_animation()
    opponent_animation()

    # Drawing
    draw()

    # Framerate
    clock.tick(FPS)

