import pygame
from pygame.locals import *

##########
# consts #
##########
WIDTH, HEIGHT = 700, 800

#########
# setup #
#########
pygame.init()

# window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# clock
clock = pygame.time.Clock()

# fonts
font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 20)

################
# game objects #
################

# game info
score = 0
lives = 3

# surfaces
status_bar = pygame.surface.Surface((WIDTH, 50))
game_screen = pygame.surface.Surface((WIDTH, 700))
instr_bar = pygame.surface.Surface((WIDTH, 50))

#############
# game loop #
#############
running = True
while running:
    ##############
    # event loop #
    ##############
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    # clear last frame
    screen.fill("black")

    ##################
    # update objects #
    ##################

    ########
    # draw #
    ########

    # status bar
    screen.blit(status_bar, (0, 0))
    score_text = font.render(f"SCORE: {score}", True, "white")
    status_bar.blit(score_text, (10, 15))
    lives_text = font.render(f"LIVES: {lives}", True, "white")
    status_bar.blit(lives_text, (WIDTH - font.size(f"LIVES: {lives}")[0] - 10, 15))
    pygame.draw.aaline(status_bar, "white", (0, 49), (WIDTH, 49))

    # game screen
    screen.blit(game_screen, (0, 50))

    # instructions bar
    screen.blit(instr_bar, (0, 750))

    ##########
    # render #
    ##########
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
