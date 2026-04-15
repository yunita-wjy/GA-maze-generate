import numpy as np

class MazeGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)  # 0 = jalan, 1 = tembok

    def add_wall(self, x, y, length, orientation):
        """
        orientation:
        0 = horizontal →
        1 = vertical ↓
        """
        if orientation == 0:  # horizontal
            for i in range(length):
                nx = x + i
                if self.is_valid_cell(nx, y):
                    self.grid[y][nx] = 1

        elif orientation == 1:  # vertical
            for i in range(length):
                ny = y + i
                if self.is_valid_cell(x, ny):
                    self.grid[ny][x] = 1

    def is_valid_cell(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def reset(self):
        self.grid.fill(0)

    def print_grid(self):
        for row in self.grid:
            print(" ".join(str(int(cell)) for cell in row))