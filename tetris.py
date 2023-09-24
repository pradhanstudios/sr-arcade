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


if __name__ == "__main__":
    board = TetrisBoard()
    print(board)
    displace = [[0, 0, 0, 1], [1, 0, 0, 0]]
    board.displace((0, 3), displace)
    print("\n" * 4)
    print(board)
