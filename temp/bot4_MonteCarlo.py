import heapq
import numpy as np
from environment_utils import is_valid, is_destination, fire_spread, visualize_simulation

class DLiteCell:
    def __init__(self):
        self.g = float('inf')  # Actual cost from start
        self.rhs = float('inf')  # One-step lookahead
        self.parent = None

def calculate_key(cell, start, heuristic):
    return (min(cell.g, cell.rhs) + heuristic, min(cell.g, cell.rhs))

def initialize_grid(n):
    grid_cells = [[DLiteCell() for _ in range(n)] for _ in range(n)]
    return grid_cells

def compute_shortest_path(open_list, grid_cells, start, goal, heuristic, n):
    while len(open_list) > 0:
        k_old, (i, j) = heapq.heappop(open_list)

        cell = grid_cells[i][j]
        if cell.g > cell.rhs:
            # Update g value to the rhs value (finalizing the value)
            cell.g = cell.rhs
        else:
            # Reset to inf to replan
            cell.g = float('inf')
            update_vertex(i, j, grid_cells, heuristic, open_list, n)

        if (start[0], start[1]) == (i, j):
            break

def update_vertex(i, j, grid_cells, start, goal, heuristic, open_list, n):
    if not is_destination(i, j, goal):
        # Update rhs value with minimum cost of moving to a neighbor
        neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
        min_rhs = float('inf')
        for ni, nj in neighbors:
            if is_valid(ni, nj, n):
                min_rhs = min(min_rhs, grid_cells[ni][nj].g + 1)  # Assumes cost = 1 to move

        grid_cells[i][j].rhs = min_rhs

    # Update priority queue
    for k, (r, c) in open_list:
        if (r, c) == (i, j):
            open_list.remove((k, (r, c)))
            heapq.heapify(open_list)
            break

    if grid_cells[i][j].g != grid_cells[i][j].rhs:
        key = calculate_key(grid_cells[i][j], start, heuristic)
        heapq.heappush(open_list, (key, (i, j)))

def time_lapse_fn_bot4(grid, q, n, frames, src, dest, fire_init):

    # Initialize grid with D*-Lite cells
    grid_cells = initialize_grid(n)
    
    # Set start and goal cells
    start = src
    goal = dest

    # Set initial rhs of goal to 0
    grid_cells[goal[0]][goal[1]].rhs = 0

    # Set up priority queue
    open_list = []
    heuristic = calculate_h_value(start[0], start[1], goal)
    heapq.heappush(open_list, (calculate_key(grid_cells[goal[0]][goal[1]], start, heuristic), goal))

    # Initialize fire
    grid[fire_init[0]][fire_init[1]] = 2
    frames.append(np.copy(grid))

    bot_pos = start
    t = 0

    while True:
        print(f"Time step: {t}")

        # Compute the shortest path
        compute_shortest_path(open_list, grid_cells, start, goal, heuristic, n)

        # If there's no valid path, break
        if grid_cells[start[0]][start[1]].g == float('inf'):
            print("No path found. Bot is stuck!")
            break

        # Move the bot to the next best position
        bot_pos = get_next_position(bot_pos, grid_cells, n)
        if is_destination(bot_pos[0], bot_pos[1], goal):
            print("The bot has reached the button.")
            break

        # Update grid and fire spread
        frames.append(np.copy(grid))
        grid = fire_spread(grid, n, q)

        # Update vertices affected by the fire
        update_vertices_affected_by_fire(grid, grid_cells, open_list, n)

        t += 1

    visualize_simulation(frames)


