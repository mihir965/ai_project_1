import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import heapq
import matplotlib.animation

class Cell3D:
    def __init__(self):
        self.parent = (0, 0, 0)
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

def is_valid(row, col, n):
    return (row >= 0) and (row < n) and (col >= 0) and (col < n)

def calculate_h_value(row, col, dest):
    return abs(row - dest[0]) + abs(col - dest[1])

def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

def grid_init(n):
    grid = [[1 for _ in range(n)] for _ in range(n)]
    init_x, init_y = random.randint(1, n - 2), random.randint(1, n - 2)
    grid[init_x][init_y] = 0
    while True:
        b_cells = blocked_cells(grid=grid, n=n)
        if not b_cells:
            break
        i, j = random.choice(b_cells)
        grid[i][j] = 0
    grid_matplot = np.array(grid)
    return grid_matplot

def blocked_cells(grid, n):
    blocked_cells = []
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if grid[i][j] == 1:
                open_neighbours = count_open_neighbours(grid, i, j)
                if open_neighbours == 1:
                    blocked_cells.append((i, j))
    return blocked_cells

def count_open_neighbours(grid, i, j):
    movement = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    open_neighbours = 0
    for mi, mj in movement:
        test_i, test_j = i + mi, j + mj
        if is_valid(test_i, test_j, len(grid)) and grid[test_i][test_j] == 0:
            open_neighbours += 1
    return open_neighbours

def place_element(grid, n, value):
    while True:
        x, y = random.randint(1, n - 2), random.randint(1, n - 2)
        if (grid[x][y] != 1 and
            grid[x + 1][y] != 2 and grid[x - 1][y] != 2 and
            grid[x][y + 1] != 2 and grid[x][y - 1] != 2):
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
    for x in range(1, n - 1):
        for y in range(1, n - 1):
            if grid[x][y] == 0:
                k = sum(1 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if grid[x + dx][y + dy] == 2)
                if k > 0:
                    p_fire = 1 - (1 - q) ** k
                    if random.random() < p_fire:
                        new_grid[x][y] = 2
    return new_grid

def simulate_fire(grid, q, n, steps):
    future_grids = [grid.copy()]
    current_grid = grid.copy()
    for _ in range(steps):
        new_grid = current_grid.copy()
        for x in range(1, n - 1):
            for y in range(1, n - 1):
                if current_grid[x][y] == 0:
                    k = sum(1 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                            if current_grid[x + dx][y + dy] == 2)
                    if k > 0:
                        p_fire = 1 - (1 - q) ** k
                        if p_fire >= 0.7:  # Threshold can be adjusted
                            new_grid[x][y] = 2
        future_grids.append(new_grid)
        current_grid = new_grid.copy()
    return future_grids

def build_3d_grid(future_grids, n, steps):
    grid_3d = np.zeros((n, n, steps + 1), dtype=int)
    for t in range(steps + 1):
        grid_3d[:, :, t] = future_grids[t]
    return grid_3d

def a_star_3d(grid_3d, src, dest, n, steps):
    closed_list = np.full((n, n, steps + 1), False)
    cell_details = np.full((n, n, steps + 1), None)
    for i in range(n):
        for j in range(n):
            for t in range(steps + 1):
                cell_details[i][j][t] = Cell3D()
    i, j, k = src
    cell_details[i][j][k].f = 0.0
    cell_details[i][j][k].g = 0.0
    cell_details[i][j][k].h = 0.0
    cell_details[i][j][k].parent = (i, j, k)
    open_list = []
    heapq.heappush(open_list, (0.0, (i, j, k)))
    movements = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]  # Including stay in place
    while open_list:
        f, (i, j, k) = heapq.heappop(open_list)
        closed_list[i][j][k] = True
        if (i, j) == dest:
            return reconstruct_path_3d(cell_details, dest, k)
        if k + 1 > steps:
            continue
        for move in movements:
            new_i, new_j = i + move[0], j + move[1]
            new_k = k + 1
            if is_valid(new_i, new_j, n):
                if closed_list[new_i][new_j][new_k]:
                    continue
                if grid_3d[new_i][new_j][new_k] == 0 or grid_3d[new_i][new_j][new_k] == 3:
                    g_new = cell_details[i][j][k].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new
                    if cell_details[new_i][new_j][new_k].f == float('inf') or cell_details[new_i][new_j][new_k].f > f_new:
                        heapq.heappush(open_list, (f_new, (new_i, new_j, new_k)))
                        cell_details[new_i][new_j][new_k].f = f_new
                        cell_details[new_i][new_j][new_k].g = g_new
                        cell_details[new_i][new_j][new_k].h = h_new
                        cell_details[new_i][new_j][new_k].parent = (i, j, k)
    return None  # No path found

def reconstruct_path_3d(cell_details, dest, dest_k):
    path = []
    i, j, k = dest[0], dest[1], dest_k
    while True:
        path.append((i, j))
        parent = cell_details[i][j][k].parent
        if (i, j, k) == parent:
            break
        i, j, k = parent
    path.reverse()
    return path

def time_lapse_fn_bot4(grid, q, n, frames, src, dest, fire_init, prediction_steps=5):
    print(f"The bot is placed in position: {src}, button position is: {dest}")
    if not is_valid(src[0], src[1], n) or not is_valid(dest[0], dest[1], n):
        print("Invalid positions")
        return
    if is_destination(src[0], src[1], dest):
        print("The bot is placed with the button! LOL")
        return
    bot_pos = src
    t = 0
    grid[fire_init[0]][fire_init[1]] = 2
    frames.append(np.copy(grid))
    while True:
        print(f"Time step: {t}")
        # Simulate future fire spread
        future_grids = simulate_fire(grid, q, n, prediction_steps)
        grid_3d = build_3d_grid(future_grids, n, prediction_steps)
        # Plan path using 3D A* algorithm
        src_3d = (bot_pos[0], bot_pos[1], 0)
        path = a_star_3d(grid_3d, src_3d, dest, n, prediction_steps)
        if not path:
            print("The bot has no path to the button due to the fire.")
            frames.append(np.copy(grid))
            break
        # Move the bot one step along the path
        if len(path) >= 2:
            grid[bot_pos[0]][bot_pos[1]] = 0
            bot_pos = path[1]  # Move to the next position
            if grid[bot_pos[0]][bot_pos[1]] == 2:
                print("The bot ran into the fire!")
                frames.append(np.copy(grid))
                break
            grid[bot_pos[0]][bot_pos[1]] = 4
            frames.append(np.copy(grid))
            print(f"Bot moved to {bot_pos}")
        elif len(path) == 1:
            print("The bot has reached the button.")
            frames.append(np.copy(grid))
            break
        else:
            print("Unexpected empty path.")
            frames.append(np.copy(grid))
            break
        # Spread the fire after bot moves
        grid = fire_spread(grid, n, q)
        frames.append(np.copy(grid))
        # Check if fire reached the bot or the button
        if grid[bot_pos[0]][bot_pos[1]] == 2:
            print("The bot has caught fire!")
            frames.append(np.copy(grid))
            break
        if grid[dest[0]][dest[1]] == 2:
            print("The button has caught fire!")
            frames.append(np.copy(grid))
            break
        t += 1
        if t > 1000:
            print("Exceeded maximum time steps, exiting to prevent infinite loop.")
            break
    visualize_simulation(frames)

# Main Execution for Bot 4
n = 40
q = 0 # Adjusted fire spread probability for testing
grid = grid_init(n)
frames = []
button_pos = button_init(grid, n, 3)
bot_pos = bot_init(grid, n, 4)
fire_init = fire_init_fn(grid, n, 2)
time_lapse_fn_bot4(grid, q, n, frames, bot_pos, button_pos, fire_init)