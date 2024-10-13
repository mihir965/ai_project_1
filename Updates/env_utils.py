# import random
# import matplotlib.pyplot as plt
# from matplotlib.colors import ListedColormap
# import numpy as np
# import heapq
# import matplotlib.animation
# import os
# import csv

# class Cell:
#     def __init__(self):
#         self.parent_i = 0
#         self.parent_j = 0
#         self.f = float('inf')
#         self.g = float('inf')
#         self.h = 0

# def is_valid(row, col, n):
#     return (row >= 0) and (row < n) and (col >= 0) and (col < n)

# def is_fire(grid, row, col):
#     return grid[row][col] == 2

# def calculate_h_value(row, col, dest):
#     return abs(row - dest[0]) + abs(col - dest[1])

# def is_unblocked_bot_1(grid, row, col, t):
#     if t == 0:
#         return grid[row][col] == 0 or grid[row][col] == 3 or grid[row][col] == 4 or grid[row][col] == 2
#     return grid[row][col] == 0 or grid[row][col] == 3 or grid[row][col] == 4

# def is_unblocked_bot_2(grid, row, col):
#     return grid[row][col] == 0 or grid[row][col] == 3 or grid[row][col] == 4

# def is_unblocked_bot_3(grid, row, col, avoid_adjacent_fire=False):
#     if grid[row][col] != 0 and grid[row][col] != 3 and grid[row][col] != 4:
#         return False
#     if avoid_adjacent_fire:
#         for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#             nx, ny = row + dx, col + dy
#             if is_valid(nx, ny, 40) and grid[nx][ny] == 2:
#                 return False
#     return True

# def is_destination(row, col, dest):
#     return row == dest[0] and col == dest[1]

# def count_open_neighbours(grid, i, j):
#     movement = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#     open_neighbours = 0
#     for mi, mj in movement:
#         test_i, test_j = i + mi, j + mj
#         if grid[test_i][test_j] == 0:
#             open_neighbours += 1
#     return open_neighbours

# def blocked_cells(grid, n):
#     blocked_cells = []
#     for i in range(1, n-1):
#         for j in range(1, n-1):
#             if grid[i][j] == 1:
#                 open_neighbours = count_open_neighbours(grid, i, j)
#                 if open_neighbours == 1:
#                     blocked_cells.append((i, j))
#     return blocked_cells

# def dead_end_cells(grid, n):
#     dead_ends = []
#     for i in range(1, n-1):
#         for j in range(1, n-1):
#             if grid[i][j] == 0 and count_open_neighbours(grid, i, j) == 1:
#                 dead_ends.append((i, j))
#     return dead_ends

# def grid_init(n):
#     grid = [[1 for _ in range(n)] for _ in range(n)]
#     init_x, init_y = random.randint(1, n-2), random.randint(1, n-2)
#     grid[init_x][init_y] = 0
#     while True:
#         b_cells = blocked_cells(grid=grid, n=n)
#         if not b_cells:
#             break
#         i, j = random.choice(b_cells)
#         grid[i][j] = 0

#     # Open approximately half of the dead-end cells
#     d_cells = dead_end_cells(grid, n)
#     num_to_open = len(d_cells) // 2
#     for _ in range(num_to_open):
#         if not d_cells:
#             break
#         i, j = random.choice(d_cells)
#         d_cells.remove((i, j))
#         movement = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#         closed_neighbors = [(i + mi, j + mj) for mi, mj in movement if grid[i + mi][j + mj] == 1]
#         if closed_neighbors:
#             ni, nj = random.choice(closed_neighbors)
#             grid[ni][nj] = 0

#     grid_matplot = np.array(grid)
#     return grid_matplot

# def place_element(grid, n, value):
#     while True:
#         x, y = random.randint(1, n-2), random.randint(1, n-2)
#         if (grid[x][y] != 1 and
#             grid[x+1][y] != 2 and grid[x-1][y] != 2 and
#             grid[x][y+1] != 2 and grid[x][y-1] != 2):
#             grid[x][y] = value
#             return x, y
    
# def bot_init(grid, n, v):
#     x, y = place_element(grid, n, v)
#     return x, y

# def button_init(grid, n, v):
#     x, y = place_element(grid, n, v)
#     return x, y

# def fire_init_fn(grid, n, v):
#     x, y = place_element(grid, n, v)
#     return x, y

# def visualize_simulation(frames, interval=100):
#     cmap = ListedColormap(['white', 'black', 'red', 'blue', 'green'])
#     fig, ax = plt.subplots()
#     ax.set_title('Grid Simulation')
#     mat = ax.matshow(frames[0], cmap=cmap, vmin=0, vmax=4)
#     def update(frame):
#         mat.set_data(frame)
#         return [mat]
#     ani = matplotlib.animation.FuncAnimation(fig, update, frames=frames, interval=interval)
#     plt.show()

# def fire_spread(grid, n, q):
#     new_grid = grid.copy()
#     for x in range(1, n-1):
#         for y in range(1, n-1):
#             if grid[x][y] == 0 or grid[x][y]==3 or grid[x][y]==4:
#                 k = sum(1 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
#                         if grid[x + dx][y + dy] == 2)
#                 if k > 0:
#                     p_fire = 1 - (1 - q) ** k
#                     if random.random() < p_fire:
#                         new_grid[x][y] = 2
#     return new_grid

# def log_results(log_data, filename='C:/Users/shaiv/Downloads/ai_project_1-main/simulation_results.csv'):
#     file_exists = os.path.isfile(filename)
#     with open(filename, 'a', newline='') as csvfile:
#         fieldnames = ['bot_type','run_id' ,'q', 'bot_pos_init', 'button_pos_init', 'fire_init', 'steps', 'result', 'final_frame','seed_value']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         if not file_exists:
#             writer.writeheader()
#         writer.writerow(log_data)

# def save_final_frame(frame, filename='final_frame.png'):
#     cmap = ListedColormap(['white', 'black', 'red', 'blue', 'green'])
#     plt.figure()
#     plt.title('Final Frame')
#     plt.imshow(frame, cmap=cmap, vmin=0, vmax=4)
#     plt.axis('off')  # Hide axis ticks and labels
#     plt.savefig(filename, bbox_inches='tight', pad_inches=0)
#     plt.close()


import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import heapq
import matplotlib.animation
import os
import csv

class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

def is_blocked(grid, row, col):
    return grid[row][col] == 1

def is_valid(row, col, n):
    return (row >= 0) and (row < n) and (col >= 0) and (col < n)

def is_fire(grid, row, col):
    return grid[row][col] == 2

def calculate_h_value(row, col, dest):
    return abs(row - dest[0]) + abs(col - dest[1])

def is_unblocked_bot_1(grid, row, col, t):
    if t == 0:
        return grid[row][col] == 0 or grid[row][col] == 3 or grid[row][col] == 4 or grid[row][col] == 2
    return grid[row][col] == 0 or grid[row][col] == 3 or grid[row][col] == 4

def is_unblocked_bot_2(grid, row, col):
    return grid[row][col] == 0 or grid[row][col] == 3 or grid[row][col] == 4

def is_unblocked_bot_3(grid, row, col, avoid_adjacent_fire=False):
    if grid[row][col] != 0 and grid[row][col] != 3 and grid[row][col] != 4:
        return False
    if avoid_adjacent_fire:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = row + dx, col + dy
            if is_valid(nx, ny, 40) and grid[nx][ny] == 2:
                return False
    return True

def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

def count_open_neighbours(grid, i, j):
    movement = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    open_neighbours = 0
    for mi, mj in movement:
        test_i, test_j = i + mi, j + mj
        if grid[test_i][test_j] == 0:
            open_neighbours += 1
    return open_neighbours

def blocked_cells(grid, n):
    blocked_cells = []
    for i in range(1, n-1):
        for j in range(1, n-1):
            if grid[i][j] == 1:
                open_neighbours = count_open_neighbours(grid, i, j)
                if open_neighbours == 1:
                    blocked_cells.append((i, j))
    return blocked_cells

def dead_end_cells(grid, n):
    dead_ends = []
    for i in range(1, n-1):
        for j in range(1, n-1):
            if grid[i][j] == 0 and count_open_neighbours(grid, i, j) == 1:
                dead_ends.append((i, j))
    return dead_ends

def grid_init(n):
    grid = [[1 for _ in range(n)] for _ in range(n)]
    init_x, init_y = random.randint(1, n-2), random.randint(1, n-2)
    grid[init_x][init_y] = 0
    while True:
        b_cells = blocked_cells(grid=grid, n=n)
        if not b_cells:
            break
        i, j = random.choice(b_cells)
        grid[i][j] = 0

    d_cells = dead_end_cells(grid, n)
    num_to_open = len(d_cells) // 2
    for _ in range(num_to_open):
        if not d_cells:
            break
        i, j = random.choice(d_cells)
        d_cells.remove((i, j))
        movement = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        closed_neighbors = [(i + mi, j + mj) for mi, mj in movement if grid[i + mi][j + mj] == 1]
        if closed_neighbors:
            ni, nj = random.choice(closed_neighbors)
            grid[ni][nj] = 0

    grid_matplot = np.array(grid)
    return grid_matplot

def place_element(grid, n, value):
    while True:
        x, y = random.randint(1, n-2), random.randint(1, n-2)
        if (grid[x][y] != 1 and
            grid[x+1][y] != 2 and grid[x-1][y] != 2 and
            grid[x][y+1] != 2 and grid[x][y-1] != 2):
            grid[x][y] = value
            return x, y
    
def bot_init(grid, n, v):
    x, y = place_element(grid, n, v)
    return x, y

def button_init(grid, n, v):
    x, y = place_element(grid, n, v)
    return x, y

def fire_init_fn(grid, n, v):
    x, y = place_element(grid, n, v)
    return x, y

def visualize_simulation(frames, interval=100):
    cmap = ListedColormap(['white', 'black', 'red', 'blue', 'green'])
    fig, ax = plt.subplots()
    ax.set_title('Grid Simulation')
    mat = ax.matshow(frames[0], cmap=cmap, vmin=0, vmax=4)
    def update(frame):
        mat.set_data(frame)
        return [mat]
    ani = matplotlib.animation.FuncAnimation(fig, update, frames=frames, interval=interval)
    plt.show()

def fire_spread(grid, n, q):
    new_grid = grid.copy()
    for x in range(1, n-1):
        for y in range(1, n-1):
            if grid[x][y] == 0 or grid[x][y]==3 or grid[x][y]==4:
                k = sum(1 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if grid[x + dx][y + dy] == 2)
                if k > 0:
                    p_fire = 1 - (1 - q) ** k
                    if random.random() < p_fire:
                        new_grid[x][y] = 2
    return new_grid

def log_results(log_data, filename='C:/Users/shaiv/Downloads/ai_project_1-main/simulation_results.csv'):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['bot_type','run_id' ,'q', 'bot_pos_init', 'button_pos_init', 'fire_init', 'steps', 'result', 'final_frame','seed_value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_data)

def save_final_frame(frame, filename='final_frame.png'):
    cmap = ListedColormap(['white', 'black', 'red', 'blue', 'green'])
    plt.figure()
    plt.title('Final Frame')
    plt.imshow(frame, cmap=cmap, vmin=0, vmax=4)
    plt.axis('off')  # Hide axis ticks and labels
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close()