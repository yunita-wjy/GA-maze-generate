import random

class Chromosome:
    def __init__(self, genes=None):
        # genes = list of tuples
        self.genes = genes if genes is not None else []