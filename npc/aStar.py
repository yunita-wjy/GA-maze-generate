import heapq

def heuristic(a, b):
    # Manhattan distance (no diagonal)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(pos, maze):
    x, y = pos
    moves = [(0,1),(1,0),(0,-1),(-1,0)]  # kanan, bawah, kiri, atas

    neighbors = []
    for dx, dy in moves:
        nx, ny = x + dx, y + dy

        if 0 <= nx < maze.width and 0 <= ny < maze.height:
            if maze.grid[ny][nx] != 1:  # bukan tembok
                neighbors.append((nx, ny))

    return neighbors


def astar(maze, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}

    g_score = {start: 0}
    explored_nodes = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        explored_nodes += 1

        if current == goal:
            path = reconstruct_path(came_from, current)
            turns = count_turns(path)
            return path, len(path), turns, explored_nodes

        for neighbor in get_neighbors(current, maze):
            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)

                heapq.heappush(open_set, (f, neighbor))

    return None, 0, 0, explored_nodes


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def count_turns(path):
    if not path or len(path) < 3:
        return 0

    turns = 0
    for i in range(2, len(path)):
        dx1 = path[i-1][0] - path[i-2][0]
        dy1 = path[i-1][1] - path[i-2][1]

        dx2 = path[i][0] - path[i-1][0]
        dy2 = path[i][1] - path[i-1][1]

        if (dx1, dy1) != (dx2, dy2):
            turns += 1

    return turns