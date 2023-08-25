import pygame
from pygame.locals import *
from math import pi
from random import randint


# constants
WIDTH, HEIGHT = 1000, 720
PADDLE_DIM = PADDLE_WIDTH, PADDLE_HEIGHT = (20, 100)
RAND = -1
LEFT = UP = 0
RIGHT = DOWN = 1


# FUNCTIONS
###############################################################################


def deg_to_reg(deg):
    return deg * 180 / pi


def generate_rand_vel(side=RAND):
    if side == RAND:
        side = randint(LEFT, RIGHT)
    up_or_down = randint(UP, DOWN)

    if up_or_down == UP:
        v_y = randint(-8, -3)
    elif up_or_down == DOWN:
        v_y = randint(3, 8)

    v_x = -5 if side == LEFT else 5

    return v_x, v_y


###############################################################################

# setup
pygame.init()

# window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# font
font = pygame.font.SysFont("arial", 20)

# clock
clock = pygame.time.Clock()

# game objects
paddle1 = pygame.Rect(
    10,
    (HEIGHT // 2) - (PADDLE_HEIGHT // 2),
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
)
paddle2 = pygame.Rect(
    WIDTH - 10 - PADDLE_WIDTH,
    (HEIGHT // 2) - (PADDLE_HEIGHT // 2),
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
)

# ball info
ball = pygame.Rect((WIDTH // 2) - 10, HEIGHT // 2 - 10, 20, 20)
ball_vel_x, ball_vel_y = 0, 0

# game loop
start = False
running = True
while running:
    # event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    # clear last frame
    screen.fill("black")

    # UPDATE
    keys = pygame.key.get_pressed()

    if not start and keys[K_SPACE]:
        ball_vel_x, ball_vel_y = generate_rand_vel()
        start = True

    if start:
        ball.centerx += ball_vel_x
        ball.centery += ball_vel_y

    # bounce at top and bottom of screen
    if ball.top <= 0:
        ball.top = 1
        ball_vel_y *= -1
    elif ball.bottom >= HEIGHT:
        ball.bottom = HEIGHT - 1
        ball_vel_y *= -1

    # bounce at left and right of screen
    if ball.left <= 0:
        ball.left = 1
        ball_vel_x *= -1
    elif ball.right >= WIDTH:
        ball.right = WIDTH - 1
        ball_vel_x *= -1

    # DRAW
    pygame.draw.rect(screen, "white", paddle1, border_radius=10)
    pygame.draw.rect(screen, "white", paddle2, border_radius=10)
    pygame.draw.ellipse(screen, "white", ball)

    # flip() display to put your work on screen
    pygame.display.flip()

    # fps cap
    clock.tick(60)

pygame.quit()
