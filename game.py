# Modules
import pygame
import sys
import os
import random
import math

# setup
pygame.init()
clock = pygame.time.Clock()

# CONSTANTS
SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 648
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 140
FPS = 60
BALL_SIZE = 30

OPPONENT_SPEED = 7

BG_COLOR = pygame.Color('grey12')
LIGHT_GREY = (200, 200, 200)
RED = (255, 40, 0)

FONT_SIZE = 32
GAME_FONT = pygame.font.Font(os.path.join("Fonts", "BRLNSDB.TTF"), FONT_SIZE)
PAUSE_FONT = pygame.font.Font(os.path.join("Fonts", "BRLNSDB.TTF"), FONT_SIZE * 2)

# Sprites
player_sprite = pygame.image.load(os.path.join("assets", "player-sprite.png"))
opponent_sprite = pygame.image.load(os.path.join("assets", "opponent-sprite.png"))
ball_sprite = pygame.image.load(os.path.join("assets", "dream-ball.png"))
game_logo = pygame.image.load(os.path.join("assets", "game-logo.png"))

# Sounds
paddle_hit_sound = pygame.mixer.Sound(os.path.join("sounds", "paddle_hit.wav"))
game_over_sound = pygame.mixer.Sound(os.path.join("sounds", "game_over.wav"))

# Game variables
scoreboard = {
    "player": 0,
    "opponent": 0
}
isPaused = True
stopTick = pygame.time.get_ticks()
currentTick = pygame.time.get_ticks()

## Functions
def draw():
    screen.fill(BG_COLOR)
    screen.blit(player.image, player.rect)
    screen.blit(opponent.image, opponent.rect)
    pygame.draw.aaline(screen, LIGHT_GREY, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))

    player_score_text = GAME_FONT.render(str(scoreboard["player"]), False, LIGHT_GREY)
    screen.blit(player_score_text, (SCREEN_WIDTH / 2 - player_score_text.get_width() / 2 - 40, SCREEN_HEIGHT / 2 - FONT_SIZE / 2))

    opponent_score_text = GAME_FONT.render(str(scoreboard["opponent"]), False, LIGHT_GREY)
    screen.blit(opponent_score_text, (SCREEN_WIDTH / 2 - opponent_score_text.get_width() / 2 + 40, SCREEN_HEIGHT / 2 - FONT_SIZE / 2))

    screen.blit(ball.image, ball.rect)

    if isPaused:
        timer_text = math.ceil((3000 - (int(currentTick) - int(stopTick))) / 1000)
        pause_text = PAUSE_FONT.render(str(timer_text), False, LIGHT_GREY)
        screen.blit(pause_text, (SCREEN_WIDTH / 2 - pause_text.get_width() / 2, SCREEN_HEIGHT / 2 - FONT_SIZE / 2 - 100))

    pygame.display.update()
       

def countdown_timer():
    global isPaused, stopTick, currentTick
    currentTick = pygame.time.get_ticks()
    if currentTick - stopTick > 3000:
        ball.restart()
        isPaused = False

# Setting up the main window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")
pygame.display.set_icon(game_logo)

## Classes

class Ball:
    def __init__(self, image, scoreboard):
        self.rect = pygame.Rect(SCREEN_WIDTH / 2 - BALL_SIZE / 2, SCREEN_HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)
        self.speedX = 7 * random.choice([-1, 1])
        self.speedY = 7 * random.choice([-1, 1])
        self.scoreboard = scoreboard
        self.isPaused = isPaused
        self.image = image

    def move(self):
        global isPaused, stopTick

        self.rect.x += self.speedX
        self.rect.y += self.speedY

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speedY *= -1
        if self.rect.left <= 0:
            self.scoreboard["opponent"] += 1
            stopTick = pygame.time.get_ticks()
            isPaused = True
            game_over_sound.play()
        if self.rect.right >= SCREEN_WIDTH:
            self.scoreboard["player"] += 1
            stopTick = pygame.time.get_ticks()
            isPaused = True
            game_over_sound.play()
        
        if self.rect.colliderect(player):
            if abs(self.rect.left - player.rect.right) < 10:
                self.speedX *= -1
            else:
                self.speedY *= -1
            paddle_hit_sound.play()
        
        if self.rect.colliderect(opponent):
            if abs(self.rect.right - opponent.rect.left) < 10:
                self.speedX *= -1
            else:
                self.speedY *= -1
            paddle_hit_sound.play()
    
    def restart(self):
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.speedX *= random.choice([-1, 1])
        self.speedY *= random.choice([-1, 1])

class Paddle:
    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image

    def move(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Player(Paddle):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.speed = 0
    
    def move(self):
        self.rect.y += self.speed
        super().move()

class Opponent(Paddle):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.speed = 7
    
    def move(self):
        if self.rect.top < ball.rect.top:
            self.rect.top += self.speed
        if self.rect.bottom > ball.rect.bottom:
            self.rect.bottom -= self.speed
        super().move()

# Objects
ball = Ball(ball_sprite, scoreboard)
player = Player(10 , SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT, player_sprite)
opponent = Opponent(SCREEN_WIDTH - PLAYER_WIDTH - 10, SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT, opponent_sprite)

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
                player.speed -= 7
            if event.key == pygame.K_DOWN:
                player.speed += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.speed += 7
            if event.key == pygame.K_DOWN:
                player.speed -= 7

    # Game logic
    if not isPaused:
        ball.move()
    else:
        countdown_timer()

    player.move()
    opponent.move()

    # Drawing
    draw()

    # Framerate
    clock.tick(FPS)

