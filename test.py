# Modules
import pygame, sys

# setup
pygame.init()
clock = pygame.time.Clock()

# CONSTANTS
SRCEEN_WIDTH = 1536
SCREEN_HEIGHT = 864
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 140
FPS = 60
BALL_SIZE = 30

BG_COLOR = pygame.Color('grey12')
LIGHT_GREY = (200, 200, 200)

# Game Rectangles
ball = pygame.Rect(SRCEEN_WIDTH / 2 - BALL_SIZE / 2, SCREEN_HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)
player = pygame.Rect(10 , SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT)
opponent = pygame.Rect(SRCEEN_WIDTH - PLAYER_WIDTH - 10, SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT)

# Setting up the main window
screen = pygame.display.set_mode((SRCEEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")


## Functions
def draw(SCREEN_WIDTH, SCREEN_HEIGHT):
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, LIGHT_GREY, player)
    pygame.draw.rect(screen, LIGHT_GREY, opponent)
    pygame.draw.ellipse(screen, LIGHT_GREY, ball)
    pygame.draw.aaline(screen, LIGHT_GREY, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
    pygame.display.flip()


# Game loop
isRunning = True
while isRunning:

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            pygame.quit()
            sys.exit()

    # Game logic

    # Drawing
    draw(SRCEEN_WIDTH, SCREEN_HEIGHT)

    # Framerate
    clock.tick(FPS)