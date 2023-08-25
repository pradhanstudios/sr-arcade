import pygame

from pygame.locals import *
from random import randint, choice


#############
# functions #
#############
def tuple_addition(t1: tuple, t2: tuple):
    return (t1[0] + t2[0], t1[1] + t2[1])


def generate_random_snake_pos() -> tuple:
    return (
        randint(
            (DIM_TILES // 2) - (DIM_TILES // 10),
            (DIM_TILES // 2) + 2 * (DIM_TILES // 10),
        ),
        randint(
            (DIM_TILES // 2) - (DIM_TILES // 10),
            (DIM_TILES // 2) + 2 * (DIM_TILES // 10),
        ),
    )


def snake_move(keys, player_dir) -> tuple:
    if keys[K_w] and player_dir != DOWN:
        return UP
    if keys[K_a] and player_dir != RIGHT:
        return LEFT
    if keys[K_s] and player_dir != UP:
        return DOWN
    if keys[K_d] and player_dir != LEFT:
        return RIGHT

    return player_dir


def snake_update(body: list[tuple], dir: tuple, fruit: tuple):
    prev_tail = body[-1]
    ate_fruit = False
    new_body = []

    ate_fruit = tuple_addition(body[0], dir) == fruit

    new_body.append(tuple_addition(body[0], dir))
    prev = body[0]
    for i in range(1, len(body)):
        new_body.append(prev)
        prev = body[i]

    if ate_fruit:
        new_body.append(prev_tail)

    return new_body


def board_update(body, fruit):
    body_segment_count = 0
    new_fruit = fruit
    new_board = []
    for r in range(DIM_TILES):
        new_row = []
        for c in range(DIM_TILES):
            if (r, c) == fruit:
                if (r, c) in body:
                    new_fruit = generate_random_fruit_pos(board)
                    new_row.append(1)
                    body_segment_count += 1
                else:
                    new_row.append(2)
                    body_segment_count += 1
            elif (r, c) in body:
                new_row.append(1)
                body_segment_count += 1
            else:
                new_row.append(0)
        new_board.append(new_row)
    if new_fruit != fruit:
        new_board[new_fruit[0]][new_fruit[1]]
    return new_board, (body_segment_count >= len(body)), new_fruit


def draw_head(surface, r, c):
    pygame.draw.rect(
        surface,
        "black",
        pygame.Rect(
            c * TILE_SIZE + 2,
            r * TILE_SIZE + 2,
            TILE_SIZE - 4,
            TILE_SIZE - 4,
        ),
        border_radius=25,
    )

    pygame.draw.rect(
        surface,
        "red",
        pygame.Rect(
            c * TILE_SIZE + (TILE_SIZE // 2 - 15),
            r * TILE_SIZE + (TILE_SIZE // 2 - 15),
            30,
            30,
        ),
        border_radius=20,
    )


def draw_body(surface, r, c):
    pygame.draw.rect(
        surface,
        "black",
        pygame.Rect(
            c * TILE_SIZE + 2,
            r * TILE_SIZE + 2,
            TILE_SIZE - 4,
            TILE_SIZE - 4,
        ),
        border_radius=25,
    )


def draw_fruit(surface, r, c):
    pygame.draw.rect(
        surface,
        "red",
        pygame.Rect(
            (c * TILE_SIZE) + (TILE_SIZE // 4),
            (r * TILE_SIZE) + (TILE_SIZE // 4),
            (TILE_SIZE // 2),
            (TILE_SIZE // 2),
        ),
        border_radius=50,
    )


def board_draw(surface, board, head):
    for r in range(DIM_TILES):
        for c in range(DIM_TILES):
            if (r, c) == head:
                draw_head(surface, r, c)
            elif board[r][c] == 1:
                draw_body(surface, r, c)
            elif board[r][c] == 2:
                draw_fruit(surface, r, c)


def generate_random_fruit_pos(board) -> tuple:
    return choice(find_open_positions(board))


def find_open_positions(board) -> list[tuple]:
    out = []
    for i in range(DIM_TILES):
        for j in range(DIM_TILES):
            if board[i][j] == 0:
                out.append((i, j))
    return out


# constants

# directions
STOP = (0, 0)
UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

# board cell states
EMPTY = 0
SNAKE = 1
FRUIT = 2

RESOLUTION = WIDTH, HEIGHT = (800, 800)
DIM_TILES = 10
TILE_SIZE = HEIGHT // DIM_TILES

# pygame setup
pygame.init()

# screen
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Snake")

# font
font = pygame.font.SysFont("arial", 20)

# clock
clock = pygame.time.Clock()

# game objects
high_score = 0
score = 0

# row, col format
board = [[EMPTY for _ in range(DIM_TILES)] for _ in range(DIM_TILES)]

player_body = [generate_random_snake_pos()]
player_head = player_body[0]
player_body.append((player_head[0] + 1, player_head[1]))
for coord in player_body:
    board[coord[0]][coord[1]] = 1
player_dir = UP

fruit_pos = generate_random_fruit_pos(board)
board[fruit_pos[0]][fruit_pos[1]] = 2

################################# GAME LOOP ###################################
frame_counter = 0
dir_change = False
running = True
while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    # clear last frame
    screen.fill("lightgreen")

    keys = pygame.key.get_pressed()

    # UPDATE
    old_dir = player_dir
    if not dir_change:
        player_dir = snake_move(keys, player_dir)
    if player_dir != old_dir:
        dir_change = True

    if frame_counter % 15 == 0:
        dir_change = False
        player_body = snake_update(player_body, player_dir, fruit_pos)

        player_head = player_body[0]

        if (
            player_head[0] < 0
            or player_head[0] > DIM_TILES - 1
            or player_head[1] < 0
            or player_head[0] > DIM_TILES - 1
        ):
            high_score = score if score > high_score else high_score
            score = 0

            board = [[EMPTY for _ in range(DIM_TILES)] for _ in range(DIM_TILES)]

            player_body = [generate_random_snake_pos()]
            player_head = player_body[0]
            player_body.append((player_head[0] + 1, player_head[1]))
            for coord in player_body:
                board[coord[0]][coord[1]] = 1
            player_dir = UP

            fruit_pos = generate_random_fruit_pos(board)
            board[fruit_pos[0]][fruit_pos[1]] = 2

        old_fruit_pos = fruit_pos
        board, running, fruit_pos = board_update(player_body, fruit_pos)
        if old_fruit_pos != fruit_pos:
            score += 1

    # DRAW
    board_draw(screen, board, player_head)
    pygame.display.set_caption(f"Snake -- high score: {high_score} -- score: {score}")

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    frame_counter += 1
    if frame_counter == 60:
        frame_counter = 0
    clock.tick(60)

pygame.quit()
