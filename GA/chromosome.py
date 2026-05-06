import random
from config.settings import GRID_SIZE

class Chromosome:
    def __init__(self, genes=None):
        # kalau genes dikasih → pakai, kalau tidak → generate random
        self.genes = genes if genes is not None else self.generate_initial()

    def random_gene(self):
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)

        if random.random() < 0.6:
            length = random.randint(4, 6)  # mayoritas pendek
        else:
            length = random.randint(7, 12)  # mayoritas panjang

        orientation = random.randint(0, 1)

        return [x, y, length, orientation]

    def generate_initial(self):
        num_genes = random.randint(20, 30)
        genes = []

        max_attempt = 1000
        attempt = 0

        while len(genes) < num_genes and attempt < max_attempt:
            attempt += 1

            raw_gene = self.random_gene()

            # STEP 1: validate boundary
            gene = self.validate_gene(raw_gene)
            if gene is None:
                continue

            # STEP 2: cek overlap = cek duplicate
            if self.is_overlap(gene, genes):
                continue

            # STEP 3: lolos semua → masuk
            genes.append(gene)

        if len(genes) < num_genes:
            print(f"Warning: initial chromosome tidak penuh. {len(genes)} < {num_genes} gene")

        return genes

    def validate_gene(self, gene):
        x, y, length, orientation = gene

        if orientation == 0:  # horizontal
            if x + length > GRID_SIZE:
                # coba geser ke kiri
                x = GRID_SIZE - length
        else:  # vertical
            if y + length > GRID_SIZE:
                # coba geser ke atas
                y = GRID_SIZE - length

        # kalau masih out of bound (kasus length > grid)
        if orientation == 0:
            max_len = GRID_SIZE - x
        else:
            max_len = GRID_SIZE - y

        # minimal ukuran panjang tembok = 2
        if max_len < 2:
            return None

        length = min(length, max_len)

        return [x, y, length, orientation]

    def is_overlap(self, gene, existing_genes):
        x, y, length, orientation = gene

        new_cells = set()
        for i in range(length):
            nx, ny = (x + i, y) if orientation == 0 else (x, y + i)
            new_cells.add((nx, ny))

        for g in existing_genes:
            gx, gy, gl, go = g
            for i in range(gl):
                ex, ey = (gx + i, gy) if go == 0 else (gx, gy + i)
                if (ex, ey) in new_cells:
                    return True

        return False

    def copy(self):
        # penting buat GA (biar ga reference ke object lama)
        return Chromosome(genes=[g[:] for g in self.genes])

    def __len__(self):
        return len(self.genes)

    def __repr__(self):
        return f"Chromosome(num_genes={len(self.genes)})"