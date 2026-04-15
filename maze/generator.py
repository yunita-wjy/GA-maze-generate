from maze.grid import MazeGrid
from config import settings

def generate_maze(chromosome):
    maze = MazeGrid(settings.GRID_WIDTH, settings.GRID_HEIGHT)

    for gene in chromosome.genes:
        x, y, length, orientation = gene
        maze.add_wall(x, y, length, orientation)

    # OPTIONAL (basic constraint awal)
    protect_start_goal(maze)

    return maze


def protect_start_goal(maze):
    """
    Biar start & goal ga ketutup tembok
    """
    sx, sy = settings.START
    gx, gy = settings.GOAL

    maze.grid[sy][sx] = settings.START_CELL
    maze.grid[gy][gx] = settings.GOAL_CELL