import pygame
from pygame.locals import *

# CONTSTANTS
"""
PIECES (for my refence)
#####
0 1 1
1 1 0
-----
0 1
1 1
1 0
----
1 0
1 1
0 1
----
1 1 0
0 1 1
#####
1 1 
1 1
#####
0 1 0
1 1 1
-----
1 0
1 1
1 0
-----
1 1 1
0 1 0
-----
0 1
1 1
0 1
#####
1 1 1 1
-----
1
1
1
1
"""
PIECES = [
    [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
    [
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
]
RESOLUTION = WIDTH, HEIGHT = (800, 800)


def displace_arr(arr: list[list[int]], t_left: tuple, displace: list[list[int]]):
    carr = [[0 for _ in arr[0]] for _ in arr]
    for i in range(len(displace)):
        for j in range(len(displace[i])):
            carr[i + t_left[0]][j + t_left[1]] = displace[i][j]

    return carr


def merge_list(l1, l2):  # l1 and l2 should be the same size
    output = [[0 for _ in l1[0]] for _ in l1]
    for i in range(len(l1)):
        for j in range(len(l1[i])):
            output[i][j] = l1[i][j] | l2[i][j]
    return output


class TetrisBoard:
    def __init__(self, rows=20, cols=10):
        self.arr = [[0 for _ in range(cols)] for _ in range(rows)]

    def __str__(self):
        output = ""
        for row in self.arr:
            for c in row:
                output += f"{c} "
            output += "\n"
        return output

    def displace(self, t_left: tuple, displace: list[list[int]]):
        self.arr = merge_list(self.arr, displace_arr(self.arr, t_left, displace))


class Piece:
    def __init__(self, piece, cur_pos):
        self.piece = piece
        self.undo = [[0 for _ in range(len(piece[0]))] for _ in range(len(piece))]
        self.cur_pos = cur_pos

    def __str__(self):
        output = ""
        for r in self.piece:
            for c in r:
                output += f"{c} "
            output += "\n"
        return output

    def rotate(self):
        N = len(self.piece)
        for i in range(N // 2):
            for j in range(i, N - i - 1):
                temp = self.piece[i][j]
                self.piece[i][j] = self.piece[N - 1 - j][i]
                self.piece[N - 1 - j][i] = self.piece[N - 1 - i][N - 1 - j]
                self.piece[N - 1 - i][N - 1 - j] = self.piece[j][N - 1 - i]
                self.piece[j][N - 1 - i] = temp
        self.undo = [
            [0 for _ in range(len(self.piece[0]))] for _ in range(len(self.piece))
        ]


pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Snake")

# font
font = pygame.font.SysFont("arial", 20)

pygame.display.set_caption("Tetris")


running = True
while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        screen.fill("darkgray")
        pygame.display.flip()


pygame.quit()
