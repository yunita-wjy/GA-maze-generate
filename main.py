import pygame
import random
import heapq
import sys

# ==========================================
# 1. Konfigurasi & Parameter Global
# ==========================================
GRID_SIZE = 20
CELL_SIZE = 30
WIDTH = GRID_SIZE * CELL_SIZE   # 600 pixel
HEIGHT = GRID_SIZE * CELL_SIZE  # 600 pixel

POP_SIZE = 40                   # Jumlah individu per generasi
GEN_LIMIT = 200                 # Batas maksimum generasi

# ==========================================
# 2. Kromosom & Representasi Maze
# ==========================================
class Maze:
    def __init__(self, chromosome=None):
        self.chromosome = chromosome if chromosome is not None else self.generate_initial()
        self.grid = []
        self.fitness = 0
        self.path = []      
        self.steps = 0      
        self.turns = 0      
        self.explored = 0   
        self.overlap_count = 0
        self.decode()

    def generate_initial(self):
        return [
            [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1), 
             random.randint(5, 12), random.randint(0, 1)] 
            for _ in range(random.randint(20, 30))
        ]

    def decode(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.overlap_count = 0
        
        for x, y, length, orient in self.chromosome: #ini loop tiap gene
            for i in range(length):
                # 0 = horizontal, 1 = vertical
                nx, ny = (x + i, y) if orient == 0 else (x, y + i)
                mx = (GRID_SIZE - 1) - nx
                my = (GRID_SIZE - 1) - ny
                
                # Tembok Utama
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    in_start_zone = (nx < 2 and ny < 2)
                    in_finish_zone = (nx >= GRID_SIZE-2 and ny >= GRID_SIZE-2)
                    if not in_start_zone and not in_finish_zone:
                        if self.grid[ny][nx] == 1: self.overlap_count += 1
                        self.grid[ny][nx] = 1

                # Tembok Cermin
                if 0 <= mx < GRID_SIZE and 0 <= my < GRID_SIZE:
                    m_in_start_zone = (mx < 2 and my < 2)
                    m_in_finish_zone = (mx >= GRID_SIZE-2 and my >= GRID_SIZE-2)
                    if not m_in_start_zone and not m_in_finish_zone:
                        if self.grid[my][mx] == 1: self.overlap_count += 1
                        self.grid[my][mx] = 1

    def check_reachability(self):
        reachable = set()
        stack = [(0, 0)] 
        empty_cells = 0
        
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] == 0: empty_cells += 1
                    
        reachable.add((0, 0))
        while stack:
            x, y = stack.pop()
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if self.grid[ny][nx] == 0 and (nx, ny) not in reachable:
                        reachable.add((nx, ny))
                        stack.append((nx, ny))
                        
        unreachable_count = empty_cells - len(reachable)
        return unreachable_count 

    def check_structure(self):
        block_2x2_pen = 0
        diagonal_pen = 0
        isolated_pen = 0    

        for y in range(GRID_SIZE - 1):
            for x in range(GRID_SIZE - 1):
                if self.grid[y][x] + self.grid[y+1][x] + self.grid[y][x+1] + self.grid[y+1][x+1] == 4:
                    block_2x2_pen += 20 
                if (self.grid[y][x] == 1 and self.grid[y+1][x+1] == 1 and self.grid[y][x+1] == 0 and self.grid[y+1][x] == 0):
                    diagonal_pen += 15
                elif (self.grid[y][x] == 0 and self.grid[y+1][x+1] == 0 and self.grid[y][x+1] == 1 and self.grid[y+1][x] == 1):
                    diagonal_pen += 15

        for y in range(GRID_SIZE): 
            for x in range(GRID_SIZE):
                if self.grid[y][x] == 1:
                    neighbors = 0
                    if y > 0: neighbors += self.grid[y-1][x]
                    if y < GRID_SIZE-1: neighbors += self.grid[y+1][x]
                    if x > 0: neighbors += self.grid[y][x-1]
                    if x < GRID_SIZE-1: neighbors += self.grid[y][x+1]
                    if neighbors == 0: isolated_pen += 5 

        return block_2x2_pen + diagonal_pen + isolated_pen

    def draw(self, screen):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                color = (44, 62, 80) if self.grid[y][x] == 1 else (236, 240, 241)
                pygame.draw.rect(screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, (200, 200, 200), (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        
        if self.path:
            for pos in self.path:
                center = (pos[0]*CELL_SIZE + CELL_SIZE//2, pos[1]*CELL_SIZE + CELL_SIZE//2)
                pygame.draw.circle(screen, (52, 152, 219), center, CELL_SIZE//3)

        # start
        pygame.draw.rect(screen, (46, 204, 113), (0, 0, CELL_SIZE, CELL_SIZE))
        # goal
        pygame.draw.rect(screen, (231, 76, 60), ((GRID_SIZE-1)*CELL_SIZE, (GRID_SIZE-1)*CELL_SIZE, CELL_SIZE, CELL_SIZE))

# ==========================================
# 3. Algoritma Evaluasi (A* Pathfinding)
# ==========================================
def a_star(maze):
    start, goal = (0, 0), (GRID_SIZE-1, GRID_SIZE-1)
    queue = [(0 + abs(goal[0]-start[0]) + abs(goal[1]-start[1]), start, [start], None)]
    visited = {}

    while queue:
        f, current, path, last_dir = heapq.heappop(queue)
        
        if current in visited and visited[current] <= f: continue
        visited[current] = f

        if current == goal:
            turns = 0
            for i in range(1, len(path)):
                dir_now = (path[i][0]-path[i-1][0], path[i][1]-path[i-1][1])
                if i > 1:
                    dir_prev = (path[i-1][0]-path[i-2][0], path[i-1][1]-path[i-2][1])
                    if dir_now != dir_prev: turns += 1
            return path, len(path), turns, len(visited)

        x, y = current
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and maze.grid[ny][nx] == 0:
                g = len(path)
                h = abs(nx - goal[0]) + abs(ny - goal[1]) 
                heapq.heappush(queue, (g + h, (nx, ny), path + [(nx, ny)], (dx, dy)))
    
    return [], 0, 0, 0 

# ==========================================
# 4. Operator Genetika: Mutasi & Evolusi
# ==========================================
def mutate(maze):
    if random.random() < 0.4: 
        r = random.random()
        if r < 0.3 and len(maze.chromosome) > 0: 
            idx = random.randint(0, len(maze.chromosome)-1)
            maze.chromosome[idx][0] = random.randint(0, GRID_SIZE-1)
            maze.chromosome[idx][1] = random.randint(0, GRID_SIZE-1)
        elif r < 0.8: 
            maze.chromosome.append([random.randint(0,GRID_SIZE-1), random.randint(0,GRID_SIZE-1), 
                                    random.randint(5,12), random.randint(0,1)])
        elif len(maze.chromosome) > 5:
            maze.chromosome.pop(random.randint(0, len(maze.chromosome)-1))

def evolve(population):
    population.sort(key=lambda x: x.fitness, reverse=True)
    new_pop = [population[0]] 

    while len(new_pop) < POP_SIZE:
        tournament = random.sample(population, 10)
        tournament.sort(key=lambda x: x.fitness, reverse=True)
        p1, p2 = tournament[0], tournament[1]
        
        cp1 = random.randint(0, len(p1.chromosome))
        cp2 = random.randint(0, len(p2.chromosome))
        
        child_chrom = []
        if p1.chromosome[:cp1]: child_chrom.extend(p1.chromosome[:cp1])
        if p2.chromosome[cp2:]: child_chrom.extend(p2.chromosome[cp2:])
        
        # --- REPAIR MECHANISM (Mekanisme Keamanan Panjang Gen) ---
        if len(child_chrom) > 45:
            child_chrom = child_chrom[:45] 
        elif len(child_chrom) < 20:
            kekurangan = 20 - len(child_chrom)
            sisa_bapak = p1.chromosome[cp1:]
            child_chrom.extend(sisa_bapak[:kekurangan])
        
        child = Maze(child_chrom)
        mutate(child)
        child.decode() 
        new_pop.append(child)
        
    return new_pop

# ==========================================
# 5. Main Loop & Visualisasi
# ==========================================
def main():
    print("========================================")
    print("  GA MAZE GENERATOR - DIFFICULTY MENU   ")
    print("========================================")
    print("1. Mudah  (Jalur cenderung lurus)")
    print("2. Sedang (Seimbang)")
    print("3. Sulit  (Zig-zag ekstrim & berliku)")
    print("========================================")
    
    choice = input("Pilih tingkat kesulitan (1/2/3) [Default: 3]: ")
    if choice == '1':
        w_turns = -2.0      # Hukuman untuk belokan
        penalty_limit = 0   # Tidak ada hukuman jalur pendek
        print(">> Mode Mudah diaktifkan! Memulai simulasi...\n")
    elif choice == '2':
        w_turns = 1.0       # Belokan dinilai normal
        penalty_limit = 0   # Tidak ada hukuman jalur pendek
        print(">> Mode Sedang diaktifkan! Memulai simulasi...\n")
    else:
        w_turns = 5.0       # Hadiah besar untuk belokan
        penalty_limit = 50  # Hukuman pemotongan skor jika langkah < 50
        print(">> Mode Sulit diaktifkan! Memulai simulasi...\n")

    # Inisiasi Pygame & Setup Window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"GA Maze Evaluator - Mode: {'Mudah' if choice=='1' else 'Sedang' if choice=='2' else 'Sulit'}")
    clock = pygame.time.Clock()

    population = [Maze() for _ in range(POP_SIZE)]
    gen_count = 0
    running = True

    while running and gen_count < GEN_LIMIT:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
                sys.exit()

        # Tahap 1: Evaluasi Fitness
        for m in population:
            unreachable_cells = m.check_reachability()
            path, steps, turns, explored = a_star(m)
            m.path, m.steps, m.turns, m.explored = path, steps, turns, explored
            
            if steps == 0: 
                m.fitness = 0.001 
            else: 
                # Skor Dasar
                base_fitness = (1.0 * steps) + (w_turns * turns) + (1.0 * explored)
                
                # Hukuman jalur pendek
                if steps < penalty_limit: 
                    base_fitness *= 0.1 
                
                wall_count = sum(row.count(1) for row in m.grid)
                wall_bonus = wall_count * 2.0
                
                density_penalty = 0
                if wall_count > 160: 
                    density_penalty = (wall_count - 160) * 5
                
                under_density_penalty = 0
                if wall_count < 100: 
                    under_density_penalty = (100 - wall_count) * 10
                
                structural_penalty = m.check_structure()
                overlap_penalty = m.overlap_count * 5 
                
                m.fitness = base_fitness + wall_bonus - density_penalty - under_density_penalty - structural_penalty - overlap_penalty
                
                if unreachable_cells > 0:
                    m.fitness *= 0.2 
                    
                m.fitness = max(0.1, m.fitness)

        # Tahap 2: Proses Evolusi
        population = evolve(population)
        best_maze = population[0] 

        # Tahap 3: Visualisasi
        screen.fill((255, 255, 255))
        best_maze.draw(screen)
        pygame.display.flip()
        
        gen_count += 1
        print(f"Gen {gen_count:03d} | Fit: {best_maze.fitness:.2f} | Steps: {best_maze.steps:03d} | Turns: {best_maze.turns:02d} | Walls: {sum(row.count(1) for row in best_maze.grid)}")
        
        clock.tick(10) 

    print("\n--- EVOLUSI SELESAI ---")
    print("Tutup jendela Pygame untuk mengakhiri program.")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()