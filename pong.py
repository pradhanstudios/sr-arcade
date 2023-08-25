import pygame
from pygame.locals import *

# setup
pygame.init()

# window
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pong")

# font
font = pygame.font.SysFont("arial", 20)

# clock
clock = pygame.time.Clock()

# game loop
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
    screen.fill("gray")

    # UPDATE

    # DRAW

    # flip() display to put your work on screen
    pygame.display.flip()

    # fps cap
    clock.tick(60)

pygame.quit()
