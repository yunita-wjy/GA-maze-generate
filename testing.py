from GA.chromosome import *
from maze.generator import *
from config import settings

# maze = MazeGrid(settings.GRID_WIDTH, settings.GRID_HEIGHT)

# maze.add_wall(2, 2, 5, 0)  # horizontal
# maze.add_wall(10, 5, 6, 1) # vertical
# maze.add_wall(10, 5, 6, 0)
#
# maze.print_grid()

c = Chromosome()
c.random_init()

maze = generate_maze(c)

maze.print_grid()