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
        for i in range(len(displace)):
            for j in range(len(displace[i])):
                self.arr[i + t_left[0]][j + t_left[1]] = displace[i][j]


class Piece:
    def __init__(self, piece):
        self.piece = piece

    def __str__(self):
        output = ""
        for r in self.piece:
            for c in r:
                output += f"{c} "
            output += "\n"
        return output

    def rotate(self):
        N = len(self.piece)
        for x in range(0, int(N / 2)):
            for y in range(x, N - x - 1):
                t = self.piece[x][y]

                # move values from right to top
                self.piece[x][y] = self.piece[y][N - 1 - x]

                self.piece[y][N - 1 - x] = self.piece[N - 1 - x][N - 1 - y]

                self.piece[N - 1 - x][N - 1 - y] = self.piece[N - 1 - y][x]
                self.piece[N - 1 - y][x] = t


if __name__ == "__main__":
    board = TetrisBoard()
    print(board)
    displace = Piece([[0, 0, 1, 1], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    print(displace)
    displace.rotate()
    print(displace)
