import random
from config.settings import GRID_WIDTH, GRID_HEIGHT

class Chromosome:
    def __init__(self, genes=None):
        # kalau genes dikasih → pakai
        # kalau tidak → generate random
        self.genes = genes if genes is not None else self.random_genes()

    def random_genes(self):
        num_genes = random.randint(20, 30)

        genes = []
        max_length = min(GRID_WIDTH, GRID_HEIGHT) // 2
        for _ in range(num_genes):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            length = random.randint(2, max_length)
            orientation = random.randint(0, 1)

            genes.append((x, y, length, orientation))  # pakai tuple

        return genes

    def copy(self):
        # penting buat GA (biar ga reference ke object lama)
        return Chromosome(genes=self.genes.copy())

    def __len__(self):
        return len(self.genes)

    def __repr__(self):
        return f"Chromosome(num_genes={len(self.genes)})"