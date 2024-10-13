# Add to environment_utils.py
import copy
import random
from env_utils import *
import uuid

def fire_forecast(grid, n, q, forecast_steps=2, seed_value=None):
    probability_grid = np.zeros((n, n))  # Initialize a grid to store fire probabilities
    temp_grid = grid.copy()

    # Create a separate random generator instance for fire forecasting
    forecast_random = random.Random(seed_value)

    for _ in range(forecast_steps):
        new_grid = temp_grid.copy()
        for x in range(1, n-1):
            for y in range(1, n-1):
                if temp_grid[x][y] == 0:
                    k = sum(1 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if temp_grid[x + dx][y + dy] == 2)
                    if k > 0:
                        p_fire = 1 - (1 - q) ** k
                        probability_grid[x][y] += p_fire
                        if forecast_random.random() < p_fire:
                            new_grid[x][y] = 2  
        temp_grid = new_grid

    # Normalization
    probability_grid = probability_grid / forecast_steps
    return probability_grid

def find_safe_zones(grid, probability_grid, threshold=0.3):
    safe_zones = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if probability_grid[i][j] < threshold and grid[i][j] == 0:
                safe_zones.append((i, j))
    return safe_zones

def calculate_adaptive_h_value(row, col, dest, fire_risk_map):
    manhattan_distance = abs(row - dest[0]) + abs(col - dest[1])
    fire_risk_penalty = fire_risk_map[row][col] * 10  # Adjust weight of fire risk
    return manhattan_distance + fire_risk_penalty

def time_lapse_fn_bot4_prob_safe(grid, q, n, frames, src, dest, fire_init, seed_value):
    run_id = str(uuid.uuid4())

    # For keeping track of results:
    log_data = {
        'Bot Type': 'Bot 4',
        'run_id': run_id,
        'q': q,
        'bot_pos_init': src,
        'button_pos_init': dest,
        'fire_init': fire_init,
        'steps': 0,
        'result': '',
        'final_frame': f'/Users/drcrocs22/Developer/Rutgers Projects/Intro To AI/PROJECT_1_FINAL/final_frames/{run_id}.png',
        'seed_value': seed_value
    }

    bot_pos = src
    t = 0

    # Fire Initialization
    grid[fire_init[0]][fire_init[1]] = 2
    frames.append(np.copy(grid))

    while True:
        print(f"Time step: {t}")

        probability_grid = fire_forecast(grid, n, q, forecast_steps=5, seed_value=seed_value)

        path = plan_path_bot4(grid, bot_pos, dest, n, probability_grid)
        if not path:
            safe_zones = find_safe_zones(grid, probability_grid)
            if safe_zones:
                safe_zone_pos = min(safe_zones, key=lambda z: calculate_adaptive_h_value(z[0], z[1], src, probability_grid))
                path = plan_path_bot4(grid, bot_pos, safe_zone_pos, n, probability_grid)
            if not path:
                print("No safe path found.")
                frames.append(np.copy(grid))
                log_data['result'] = 'Path blocked'
                break

        # Move the bot one step along the path
        if len(path) >= 2:
            grid[bot_pos[0]][bot_pos[1]] = 0
            bot_pos = path[1]  # Move to the next position
            if grid[bot_pos[0]][bot_pos[1]] == 2:
                print("The bot ran into the fire!")
                frames.append(np.copy(grid))
                log_data['result'] = 'Bot ran into fire'
                break
            grid[bot_pos[0]][bot_pos[1]] = 4
            frames.append(np.copy(grid))
            print(f"Bot moved to {bot_pos}")
        elif len(path) == 1:
            # Bot has reached the destination
            print("The bot has reached the button.")
            frames.append(np.copy(grid))
            log_data['result'] = 'Success'
            break
        else:
            # Unexpected empty path
            print("Unexpected empty path.")
            frames.append(np.copy(grid))
            break

        # Spread the fire after bot moves
        grid = fire_spread(grid, n, q)
        frames.append(np.copy(grid))

        # Check if fire reached the bot or the button
        if grid[bot_pos[0]][bot_pos[1]] == 2:
            print("The bot has caught fire!")
            log_data['result'] = 'Bot caught fire'
            frames.append(np.copy(grid))
            break
        if grid[dest[0]][dest[1]] == 2:
            print("The button has caught fire!")
            log_data['result'] = 'Button caught fire'
            frames.append(np.copy(grid))
            break

        t += 1

    log_data['steps'] = t
    log_results(log_data)
    # Save the final frame
    save_final_frame(frames[-1], filename=f'/Users/drcrocs22/Developer/Rutgers Projects/Intro To AI/PROJECT_1_FINAL/final_frames/{run_id}.png')
    visualize_simulation(frames)

def plan_path_bot4(grid, bot_pos, dest, n, probability_grid):
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
    cell_details, found_dest = bot_planning_bot4(closed_list, cell_details, open_list, bot_pos, dest, grid, found_dest, n, probability_grid)
    if found_dest:
        return track_path_bot3(cell_details, dest, bot_pos, n)  # Reuse bot 3's tracking function
    else:
        return None

def bot_planning_bot4(closed_list, cell_details, open_list, src, dest, grid, found_dest, n, probability_grid):
    while len(open_list) > 0:
        p = heapq.heappop(open_list)
        i, j = p[1]
        closed_list[i][j] = True
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dir in directions:
            new_i, new_j = i + dir[0], j + dir[1]
            if is_valid(new_i, new_j, n):
                # Avoid blocked cells
                if is_blocked(grid, new_i, new_j):
                    continue

                # Check if it's the destination
                if is_destination(new_i, new_j, dest):
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    found_dest = True
                    return cell_details, found_dest
                
                # Check if it's a fire cell and exclude it
                if not closed_list[new_i][new_j] and not is_fire(grid, new_i, new_j):
                    # Include fire probability as part of the cost
                    g_new = cell_details[i][j].g + 1.0 + probability_grid[new_i][new_j]
                    h_new = calculate_adaptive_h_value(new_i, new_j, dest, probability_grid)
                    f_new = g_new + h_new
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        heapq.heappush(open_list, (f_new, (new_i, new_j)))
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
    return cell_details, found_dest


def track_path_bot3(cell_details, dest, src, n):
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