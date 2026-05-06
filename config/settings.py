# Dummy testing
GRID_SIZE = 20
CELL_SIZE = 30
WIDTH = GRID_SIZE * CELL_SIZE   # 600 pixel
HEIGHT = GRID_SIZE * CELL_SIZE  # 600 pixel

START = (0, 0)
GOAL = (9, 9)

EMPTY = 0
WALL = 1
START_CELL = 5
GOAL_CELL = 6

POP_SIZE = 40                   # Jumlah individu per generasi
GEN_LIMIT = 200                 # Batas maksimum generasi

MUTATION_RATE = 0.1

# Fitness weights
W_LENGTH = 1.0
W_TURN = 1.0
W_EFFORT = 0.5