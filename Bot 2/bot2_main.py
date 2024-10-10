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
    return (0 <= row < n) and (0 <= col < n)

def calculate_h_value_bot1(row, col, dest):
    return ((row - dest[0])**2 + (col - dest[1])**2)**0.5

def is_unblocked(grid, row, col):
    return grid[row][col] == 0 or grid[row][col] == 3 or grid[row][col] == 4

def is_destination(row, col, dest):
    return (row, col) == dest

def count_open_neighbours(grid, i, j):
    movement = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    open_neighbours = 0
    for mi, mj in movement:
        test_i, test_j = i + mi, j + mj
        if is_valid(test_i, test_j, len(grid)) and grid[test_i][test_j] == 0:
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
    return place_element(grid, n, v)

def button_init(grid, n, v):
    return place_element(grid, n, v)

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

def time_lapse_fn(grid, q, n, frames, src, dest):
    print(f"The bot is placed in position: {src}, button position is: {dest}")
    if not is_valid(src[0], src[1], n) or not is_valid(dest[0], dest[1], n):
        print("Invalid positions")
        return
    if not (is_unblocked(grid, src[0], src[1]) and is_unblocked(grid, dest[0], dest[1])):
        print("The map is bugging")
        return
    if is_destination(src[0], src[1], dest):
        print("The bot is placed with the button! LOL")
        return

    bot_pos = src
    t = 0

    # Fire Initialization
    while True:
        f_x, f_y = random.randint(1, n-2), random.randint(1, n-2)
        if grid[f_x][f_y] == 0:
            grid[f_x][f_y] = 2
            break
    frames.append(np.copy(grid))  # Append a deep copy of the grid

    while True:
        print(f"Time step: {t}")

        path = plan_path(grid, bot_pos, dest, n)
        if not path:
            print("No path found. Bot is stuck!")
            break

        # Move the bot one step along the path
        if len(path) > 1:
            grid[bot_pos[0]][bot_pos[1]] = 0  # Clear previous bot position
            bot_pos = path.pop(1)  # Move to the next position
            grid[bot_pos[0]][bot_pos[1]] = 4  # Mark new bot position
            frames.append(np.copy(grid))  # Append a deep copy of the grid
        else:
            # Bot has reached the destination
            print("The bot has reached the button.")
            frames.append(np.copy(grid))
            break

        # Spread the fire after bot moves
        grid = fire_spread(grid, n, q)
        frames.append(np.copy(grid))  # Append a deep copy of the grid

        # Check if fire reached the bot or the button
        if grid[bot_pos[0]][bot_pos[1]] == 2:
            print("The bot has caught fire!")
            frames.append(np.copy(grid))
            break
        if grid[dest[0]][dest[1]] == 2:
            print("The button has caught fire!")
            frames.append(np.copy(grid))
            break

        # Replan if path is blocked by fire
        if any(grid[step[0]][step[1]] == 2 for step in path[1:]):
            print("Path blocked by fire, replanning...")
            path = plan_path(grid, bot_pos, dest, n)
            if not path:
                print("Replanning failed, no path found.")
                frames.append(np.copy(grid))
                break

        t += 1

    visualize_simulation(frames)

def plan_path(grid, bot_pos, dest, n):
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
    cell_details, found_dest = bot_planning(closed_list, cell_details, open_list, bot_pos, dest, grid, found_dest, n)
    if found_dest:
        return track_path(cell_details, dest)
    else:
        return None

def track_path(cell_details, dest):
    path = []
    i, j = dest
    while not (cell_details[i][j].parent_i == i and cell_details[i][j].parent_j == j):
        path.append((i, j))
        temp_i = cell_details[i][j].parent_i
        temp_j = cell_details[i][j].parent_j
        i, j = temp_i, temp_j
    path.append((i, j))  # Include the start cell
    path.reverse()
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

def bot_planning(closed_list, cell_details, open_list, src, dest, grid, found_dest, n):
    while len(open_list) > 0:
        p = heapq.heappop(open_list)[1]
        i, j = p

        closed_list[i][j] = True

        if is_destination(i, j, dest):
            found_dest = True
            break

        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if is_valid(i + x, j + y, n):
                if is_unblocked(grid, i + x, j + y) and not closed_list[i + x][j + y]:
                    g_new = cell_details[i][j].g + 1
                    h_new = calculate_h_value_bot1(i + x, j + y, dest)
                    f_new = g_new + h_new
                    
                    if cell_details[i + x][j + y].f > f_new:
                        cell_details[i + x][j + y].f = f_new
                        cell_details[i + x][j + y].g = g_new
                        cell_details[i + x][j + y].h = h_new
                        cell_details[i + x][j + y].parent_i = i
                        cell_details[i + x][j + y].parent_j = j
                        heapq.heappush(open_list, (f_new, (i + x, j + y)))

    return cell_details, found_dest

if __name__ == "__main__":
    n = 40  # Size of the grid
    q = 1  # Probability of fire spreading
    frames = []
    grid = grid_init(n)

    # Initialize bot and button
    bot_pos = bot_init(grid, n, 4)  # Bot represented by 4
    button_pos = button_init(grid, n, 3)  # Button represented by 3

    time_lapse_fn(grid, q, n, frames, bot_pos, button_pos)
