import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import heapq
import matplotlib.animation

class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

def is_valid(row, col, n):
    return (row >= 0) and (row < n) and (col >= 0) and (col < n)

def calculate_h_value(row, col, dest):
    return abs(row - dest[0]) + abs(col - dest[1])

def is_unblocked(grid, row, col):
    return grid[row][col] == 0 or grid[row][col] == 3 or grid[row][col] == 4  # 3 = button, 4 = bot

def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

def blocked_cells(grid, n):
    blocked_cells = []
    for i in range(1, n-1):
        for j in range(1, n-1):
            if grid[i][j] == 1:  # Marking walls
                open_neighbours = sum(1 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if grid[i+dx][j+dy] == 0)
                if open_neighbours == 1:
                    blocked_cells.append((i, j))
    return blocked_cells

def grid_init(n):
    grid = [[1 for _ in range(n)] for _ in range(n)]  # Initialize grid with walls (1)
    init_x, init_y = random.randint(1, n-2), random.randint(1, n-2)
    grid[init_x][init_y] = 0  # Opening the starting point
    while True:
        b_cells = blocked_cells(grid=grid, n=n)
        if not b_cells:
            break
        i, j = random.choice(b_cells)
        grid[i][j] = 0  # Carve open paths by setting to 0 (open cell)
    return np.array(grid)

def place_element(grid, n, value):
    while True:
        x, y = random.randint(1, n-2), random.randint(1, n-2)
        if (grid[x][y] != 1 and  # Not a wall
            grid[x+1][y] != 2 and grid[x-1][y] != 2 and  # Fire doesn't surround it
            grid[x][y+1] != 2 and grid[x][y-1] != 2):
            grid[x][y] = value  # Place element (bot or button)
            return x, y

def bot_init(grid, n, v):
    x, y = place_element(grid, n, v)
    return x, y

def button_init(grid, n, v):
    x, y = place_element(grid, n, v)
    return x, y

def predict_fire_spread(grid, q, n):
    fire_risk_map = np.zeros((n, n))  # Initialize risk map
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:  # Open cells only
                burning_neighbors = sum(1 for d in directions if is_valid(i+d[0], j+d[1], n) and grid[i+d[0]][j+d[1]] == 2)
                if burning_neighbors > 0:
                    fire_risk_map[i][j] = 1 - (1 - q) ** burning_neighbors
    return fire_risk_map

def find_safe_zones(grid, fire_risk_map, threshold=0.3):
    safe_zones = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if fire_risk_map[i][j] < threshold and grid[i][j] == 0:
                safe_zones.append((i, j))
    return safe_zones

def calculate_adaptive_h_value(row, col, dest, fire_risk_map):
    manhattan_distance = abs(row - dest[0]) + abs(col - dest[1])
    fire_risk_penalty = fire_risk_map[row][col] * 10  # Adjust weight of fire risk
    return manhattan_distance + fire_risk_penalty

def bot_4_execution(grid, q, n, bot_pos, button_pos, fire_pos):
    frames = []
    fire_risk_map = predict_fire_spread(grid, q, n)
    
    def plan_path(destination):
        closed_list = [[False for _ in range(n)] for _ in range(n)]
        cell_details = [[Cell() for _ in range(n)] for _ in range(n)]
        open_list = []
        i, j = bot_pos
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j
        heapq.heappush(open_list, (0.0, (i, j)))
        found_dest = False
        while open_list:
            p = heapq.heappop(open_list)
            i, j = p[1]
            closed_list[i][j] = True
            for (add_i, add_j) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_i, next_j = i + add_i, j + add_j
                if is_valid(next_i, next_j, n) and grid[next_i][next_j] != 2:  # Ensure not moving into fire
                    if is_destination(next_i, next_j, destination):
                        cell_details[next_i][next_j].parent_i = i
                        cell_details[next_i][next_j].parent_j = j
                        found_dest = True
                        return track_path(cell_details, destination)
                    
                    if not closed_list[next_i][next_j] and is_unblocked(grid, next_i, next_j):
                        g_new = cell_details[i][j].g + 1.0
                        h_new = calculate_adaptive_h_value(next_i, next_j, destination, fire_risk_map)
                        f_new = g_new + h_new
                        if cell_details[next_i][next_j].f == float('inf') or cell_details[next_i][next_j].f > f_new:
                            heapq.heappush(open_list, (f_new, (next_i, next_j)))
                            cell_details[next_i][next_j].f = f_new
                            cell_details[next_i][next_j].g = g_new
                            cell_details[next_i][next_j].h = h_new
                            cell_details[next_i][next_j].parent_i = i
                            cell_details[next_i][next_j].parent_j = j
        return None

    path = plan_path(button_pos)
    if not path:
        safe_zones = find_safe_zones(grid, fire_risk_map)
        if safe_zones:
            safe_zone_pos = min(safe_zones, key=lambda z: calculate_adaptive_h_value(z[0], z[1], button_pos, fire_risk_map))
            path = plan_path(safe_zone_pos)
        if not path:
            print("No safe path found.")
            return frames

    t = 0
    while True:
        print(f"Time step: {t}")

        # Move the bot one step along the path
        if len(path) > 1:
            grid[bot_pos[0]][bot_pos[1]] = 0  # Clear previous bot position
            bot_pos = path.pop(1)  # Move to the next position
            grid[bot_pos[0]][bot_pos[1]] = 4  # Mark new bot position
            frames.append(np.copy(grid))  # Append a deep copy of the grid
        else:
            print("The bot has reached the button.")
            frames.append(np.copy(grid))
            break

        # Spread the fire
        grid = fire_spread(grid, n, q)
        frames.append(np.copy(grid))  # Append a deep copy of the grid

        # Check if fire reached the bot or the button
        if grid[bot_pos[0]][bot_pos[1]] == 2:
            print("The bot has caught fire!")
            frames.append(np.copy(grid))
            break
        if grid[button_pos[0]][button_pos[1]] == 2:
            print("The button has caught fire!")
            frames.append(np.copy(grid))
            break

        t += 1
        fire_risk_map = predict_fire_spread(grid, q, n)  # Recalculate fire risk

    return frames

def track_path(cell_details, dest):
    path = []
    i, j = dest
    while not (cell_details[i][j].parent_i == i and cell_details[i][j].parent_j == j):
        path.append((i, j))
        temp_i = cell_details[i][j].parent_i
        temp_j = cell_details[i][j].parent_j
        i, j = temp_i, temp_j
    path.append((i, j))
    return path[::-1]  # Return reversed path

def fire_spread(grid, n, q):
    fire_grid = np.copy(grid)
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 2:  # If current cell is on fire
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if is_valid(i + dx, j + dy, n) and grid[i + dx][j + dy] == 0:
                        if random.random() < q:
                            fire_grid[i + dx][j + dy] = 2  # Catch fire
    return fire_grid

def run_simulation(n=40, q=0.5, steps=50):
    grid = grid_init(n)
    bot_pos = bot_init(grid, n, 4)  # 4 represents the bot
    button_pos = button_init(grid, n, 3)  # 3 represents the button
    fire_pos = place_element(grid, n, 2)  # 2 represents the fire

    print("Initial Grid:")
    print(grid)
    frames = bot_4_execution(grid, q, n, bot_pos, button_pos, fire_pos)

    # Plotting the simulation
    cmap = ListedColormap(['white', 'black', 'red', 'blue', 'green'])  # 0=empty, 1=wall, 2=fire, 3=button, 4=bot
    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()
        ax.imshow(frame, cmap=cmap)
        ax.set_title('Fire Extinguisher Bot Simulation')

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=frames, repeat=False)
    plt.show()

run_simulation()
