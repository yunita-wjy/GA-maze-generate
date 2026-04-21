import random
from config.settings import GRID_WIDTH, GRID_HEIGHT

class Chromosome:
    def __init__(self, genes=None):
        self.genes = genes if genes else self.generate_initial()

    def generate_initial(self):
        return [
            [
                random.randint(0, GRID_WIDTH-1),
                random.randint(0, GRID_HEIGHT-1),
                random.randint(5, 12),
                random.randint(0, 1)
            ]
            for _ in range(random.randint(20, 30))
        ]