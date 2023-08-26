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
PADDLE_SPEED = 10


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
font = pygame.font.SysFont("arial", 48)

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
player_1_score = player_2_score = 0

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

    # wait for SPACE to start game
    if not start and keys[K_SPACE]:
        ball_vel_x, ball_vel_y = generate_rand_vel()
        start = True

    # if game has started
    if start:
        # paddle 1 movement
        if keys[K_w]:
            paddle1.y -= PADDLE_SPEED
        if keys[K_s]:
            paddle1.y += PADDLE_SPEED

        # paddle 2 movement
        if keys[K_UP]:
            paddle2.y -= PADDLE_SPEED
        if keys[K_DOWN]:
            paddle2.y += PADDLE_SPEED

        # update ball when game has started
        ball.centerx += ball_vel_x
        ball.centery += ball_vel_y

    # keep paddle 2 on screen
    if paddle2.top <= 0:
        paddle2.top = 0
    elif paddle2.bottom >= HEIGHT:
        paddle2.bottom = HEIGHT

    # keep paddle 1 on screen
    if paddle1.top <= 0:
        paddle1.top = 0
    elif paddle1.bottom >= HEIGHT:
        paddle1.bottom = HEIGHT

    # bounce at top and bottom of screen
    if ball.top <= 0:
        ball.top = 1
        ball_vel_y *= -1
    elif ball.bottom >= HEIGHT:
        ball.bottom = HEIGHT - 1
        ball_vel_y *= -1

    # bounce at left and right of screen
    if ball.left <= 0:
        player_2_score += 1
        ball_vel_x *= -1
        # ball_vel_x, ball_vel_y = 10, 10
        ball.x = WIDTH//2
        ball.y = HEIGHT//2
    elif ball.right >= WIDTH:
        player_1_score += 1
        # ball_vel_x, ball_vel_y = 10, 10
        ball_vel_x *= -1
        ball.x = WIDTH//2
        ball.y = HEIGHT//2

    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_vel_x *= -1

    # DRAW
    text1 = font.render(f"{player_1_score}", False, (255, 255, 255))
    text2 = font.render(f"{player_2_score}", False, (255, 255, 255))
    screen.blit(text1, (0+200, 0))
    screen.blit(text2, (WIDTH-50-200, 0))
    pygame.draw.rect(screen, "white", paddle1, border_radius=10)
    pygame.draw.rect(screen, "white", paddle2, border_radius=10)
    pygame.draw.ellipse(screen, "white", ball)

    # flip() display to put your work on screen
    pygame.display.flip()

    # fps cap
    clock.tick(60)

pygame.quit()
