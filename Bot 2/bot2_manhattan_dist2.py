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

def is_fire(grid, row, col):
    return grid[row][col] == 2

def calculate_h_value(row, col, dest):
    return abs(row - dest[0]) + abs(col - dest[1])

def is_unblocked(grid, row, col, t):
    if t == 0:
        return grid[row][col] == 0 or grid[row][col] == 3 or grid[row][col] == 4 or grid[row][col] == 2
    return grid[row][col] == 0 or grid[row][col] == 3 or grid[row][col] == 4

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

def time_lapse_fn(grid, q, n, frames, src, dest, fire_init):
    print(f"The bot is placed in position: {src}, button position is: {dest}")
    if not is_valid(src[0], src[1], n) or not is_valid(dest[0], dest[1], n):
        print("Invalid positions")
        return
    if is_destination(src[0], src[1], dest):
        print("The bot is placed with the button! LOL")
        return

    # Initialize the bot's starting position
    bot_pos = src
    t = 0

    # Fire Initialization
    grid[fire_init[0]][fire_init[1]] = 2
    frames.append(np.copy(grid))

    # Initial path planning
    def plan_path():
        print("plan path ran")
        closed_list = [[False for _ in range(n)] for _ in range(n)]
        cell_details = [[Cell() for _ in range(n)] for _ in range(n)]
        open_list = []
        i, j = bot_pos
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j
        print("pushing cell")
        heapq.heappush(open_list, (0.0, (i, j)))
        found_dest = False
        cell_details, found_dest = bot_planning(closed_list, cell_details, open_list, bot_pos, dest, grid, found_dest, n, t)
        print("if condition")
        if found_dest:
            return track_path(cell_details, dest, src, n)
        else:
            print("No path in plan_path")
            return None
        
    path = plan_path()
    if not path:
        print("No initial path found.")
        return

    while True:
        print(f"Time step: {t}")

        print("moving bot")
        # Move the bot one step along the path
        if len(path) > 1:
            grid[bot_pos[0]][bot_pos[1]] = 0  
            bot_pos = path.pop(1)
            if grid[bot_pos[0]][bot_pos[1]] == 2:
                print("The bot ran into the fire!")
                break
            grid[bot_pos[0]][bot_pos[1]] = 4
            frames.append(np.copy(grid))
        else:
            # Bot has reached the destination
            print("The bot has reached the button.")
            frames.append(np.copy(grid))
            break

        print("Spreading fire")
        # Spread the fire after bot moves
        grid = fire_spread(grid, n, q)
        frames.append(np.copy(grid))

        # Check if fire reached the bot or the button
        print("checking fire")
        if grid[bot_pos[0]][bot_pos[1]] == 2:
            print("The bot has caught fire!")
            frames.append(np.copy(grid))
            break
        if grid[dest[0]][dest[1]] == 2:
            print("The button has caught fire!")
            frames.append(np.copy(grid))
            break

        print(f"Replanning at step {t}")
        path = plan_path()
        if not path:
            print("No further path found.")
            break
            #return

        t += 1

    visualize_simulation(frames)

def track_path(cell_details, dest, src, n):
    print("tracking path")
    path = []
    i, j = dest
    visited = set()
    while not (i == src[0] and j == src[1]):
        print(f"Current cell: ({i}, {j}), Parent: ({cell_details[i][j].parent_i}, {cell_details[i][j].parent_j})")
        path.append((i, j))
        if (i, j) in visited:
            print("Detected loop in track_path.")
            break  # Prevent infinite loop
        visited.add((i, j))
        temp_i = cell_details[i][j].parent_i
        temp_j = cell_details[i][j].parent_j
        if not is_valid(temp_i, temp_j, n):
            print(f"Invalid parent cell: ({temp_i}, {temp_j})")
            break  # Prevent infinite loop
        i, j = temp_i, temp_j
    path.append((src[0], src[1]))  # Add the source cell
    path.reverse()
    print("Function almost done")
    return path

def fire_spread(grid, n, q):
    new_grid = grid.copy()
    for x in range(1, n-1):
        for y in range(1, n-1):
            if grid[x][y] == 0:
                k = sum(1 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if grid[x + dx][y + dy] == 2)
                if k > 0:
                    p_fire = 1 - (1 - q) ** k
                    if random.random() < p_fire:
                        new_grid[x][y] = 2
    return new_grid

def bot_planning(closed_list, cell_details, open_list, src, dest, grid, found_dest, n, t):
    while len(open_list) > 0:
        p = heapq.heappop(open_list)
        i, j = p[1]
        closed_list[i][j] = True
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dir in directions:
            new_i, new_j = i + dir[0], j + dir[1]
            if is_valid(new_i, new_j, n):
                if is_destination(new_i, new_j, dest):
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    found_dest = True
                    return cell_details, found_dest
                if not closed_list[new_i][new_j] and is_unblocked(grid, new_i, new_j, t) and not is_fire(grid, new_i, new_j):
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        heapq.heappush(open_list, (f_new, (new_i, new_j)))
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
    return cell_details, found_dest

# Main Execution
n = 40
q = 1.0
grid = grid_init(n)
frames = []
button_pos = button_init(grid, n, 3)
bot_pos = bot_init(grid, n, 4)
fire_init = fire_init_fn(grid, n, 2)
time_lapse_fn(grid, q, n, frames, bot_pos, button_pos, fire_init)