import pygame
from pygame.locals import *
import numpy as np

# CONTSTANTS
"""
PIECES (for my refence)
#####
0 1 1
1 1 0 red
-----
0 1
1 1
1 0 red
----
1 0
1 1
0 1 red
----
1 1 0
0 1 1 red
#####
1 1 
1 1 yellow
#####
0 1 0 purple
1 1 1
-----
1 0
1 1
1 0 purple
-----
1 1 1
0 1 0 purple
-----
0 1
1 1
0 1 purple
#####
1 1 1 1 light blue
-----
1 light blue
1
1
1
"""
DOWN = (0, 1)
FPS = 60

PIECES = [
    np.array([[0, 1, 1], [1, 1, 0], [0, 0, 0]]),
    np.array([[1, 1], [1, 1]]),
    np.array([[0, 1, 0], [1, 1, 1], [0, 0, 0]]),
    np.array([
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]),
]
PIECE_COLORS = ["red", "yellow", "purple", "lightblue"]
PIECE_SIZE = 40
RESOLUTION = WIDTH, HEIGHT = (800, 800)


def displace_arr(arr, t_left: tuple, displace, color, color_arr):
    x1, y1 = t_left
    x2, y2 = displace.shape
    # print(arr)
    # print(arr[y1: y2 + y1, x1:x2 + x1] )
    arr[y1: y2 + y1, x1:x2 + x1] |= displace
    color_arr[y1: y2 + y1, x1: x2 + x1] = np.array([[color if j == 1 else 0 for j in i] for i in displace])
    
    # carr = [[0 for _ in arr[0]] for _ in arr]
    # for i in range(len(displace)):
    #     for j in range(len(displace[i])):
    #         carr[i + t_left[0]][j + t_left[1]] = displace[i][j]

    # return carr

def undo_displace_arr(arr, t_left: tuple, displace, color_arr):
    x1, y1 = t_left
    x2, y2 = displace.shape
    # print(arr)
    # print(arr[y1: y2 + y1, x1:x2 + x1] )
    arr[y1: y2 + y1, x1:x2 + x1] &= np.bitwise_not(displace)
    color_arr[y1: y2 + y1, x1: x2 + x1] = np.zeros((x2, y2))


t_addition = lambda t1, t2: (t1[0] + t2[0], t1[1] + t2[1])
t_flip = lambda t1: (t1[1], t1[0])

def merge_list(l1, l2):  # l1 and l2 should be the same size
    return l1 | l2

def touching(arr, t_left, displace):
    places = []
    checkrow = [i for i in displace[::-1] if any(i)][0]
    top_left = t_flip(t_left)

    for i in range(len(checkrow)):
        places.append(t_addition(top_left, (checkrow[i]+1, i)))
    

    print(places, checkrow)

    for y, x in places:
        if arr[y][x]:
            return True
    
    return False

class TetrisBoard:
    def __init__(self, rows=20, cols=10):
        self.arr = np.array([[0 for _ in range(cols)] for _ in range(rows)])
        self.color_arr = np.array([[0 for _ in range(cols)] for _ in range(rows)])

    def __str__(self):
        output = ""
        for row in self.arr:
            for c in row:
                output += f"{c} "
            output += "\n"
        return output

    def displace(self, t_left: tuple, displace, color):
        displace_arr(self.arr, t_left, displace, color, self.color_arr)

    def undo_displace(self, t_left: tuple, displace):
        undo_displace_arr(self.arr, t_left, displace, self.color_arr)

    def update(self):
        for i in range(len(self.arr)-1, -1, -1):
            if all(self.arr[i]):
                self.arr.pop(i)
                self.arr.append([0 for i in range(10)])



class Piece:
    def __init__(self, piece, cur_pos, color="white"):
        self.piece = piece
        self.cur_pos = cur_pos
        self.color = color

    def __str__(self):
        output = ""
        for r in self.piece:
            for c in r:
                output += f"{c} "
            output += "\n"
        return output

    def rotate(self):
        self.piece = np.rot90(self.piece)

    def is_on_last_row(self):
        return not (self.cur_pos[0] - self.piece.size + 1)

    def displace_on(self, board: TetrisBoard):
        board.displace(self.cur_pos, self.piece, self.color)

    def undo_displace_on(self, board: TetrisBoard):
        # print(self.undo)
        board.undo_displace(self.cur_pos, self.piece)

    def move_down_on(self, board: TetrisBoard):
        if not self.is_on_last_row():
            self.undo_displace_on(board)
            self.cur_pos = t_addition(self.cur_pos, DOWN)
            self.displace_on(board)
            return True # if succesful
        return False



pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Snake")
board = TetrisBoard()
frame_counter = 0

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
        #############
        # DRAW GRID #
        #############
        pygame.draw.line(screen, "black", (200, 0), (200, 800))
        pygame.draw.line(screen, "black", (600, 0), (600, 800))
        for i in range(20):
            pygame.draw.line(screen, "black", (200, PIECE_SIZE*i), (600, PIECE_SIZE*i))
        for i in range(10):
            pygame.draw.line(screen, "black", (i*PIECE_SIZE + 200, 0), (i*PIECE_SIZE + 200, 800))

        # for i in range(20):
        #     for j in range(10):
        #         if board.color_arr[i][j]


        pygame.display.flip()
        frame_counter += 1
        if frame_counter >= 60:
            frame_counter %= 60
        clock.tick(FPS)


pygame.quit()
