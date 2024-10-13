# from environment_utils import grid_init, bot_init, button_init, fire_init_fn, fire_spread, is_valid, is_destination, calculate_h_value, visualize_simulation,Cell, is_unblocked_bot_1, log_results, save_final_frame
from env_utils import *
import heapq
import numpy as np
import uuid

def time_lapse_fn_bot_1(grid, q, n, frames, src, dest, fire_init, seed_value, trial):

    run_id = str(uuid.uuid4())

    #For keeping track of results:
    log_data = {
        'Bot Type': 'Bot 1',
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

    print(f"The bot is placed in position: {src}, button position is: {dest}")
    if not is_valid(src[0], src[1], n) or not is_valid(dest[0], dest[1], n):
        print("Invalid positions")
        return
    if is_destination(src[0], src[1], dest):
        print("The bot is placed with the button! LOL")
        log_data['result'] = 'Bot already at button'
        return

    # Initialize the bot's starting position
    bot_pos = src
    t = 0

    # Fire Initialization
    grid[fire_init[0]][fire_init[1]] = 2
    frames.append(np.copy(grid))

    # Initial path planning
    def plan_path_bot_1():
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
        cell_details, found_dest = bot_planning_bot1(closed_list, cell_details, open_list, bot_pos, dest, grid, found_dest, n, t)
        if found_dest:
            return track_path_bot1(cell_details, dest)
        else:
            return None

    path = plan_path_bot_1()
    if not path:
        print("No initial path found.")
        log_data['result'] = 'Path blocked'
        return

    while True:
        print(f"Time step: {t}")

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
            log_data['result'] = 'Success'
            break

        # Spread the fire after bot moves
        grid = fire_spread(grid, n, q)
        frames.append(np.copy(grid))

        # Check if fire reached the bot or the button
        if grid[bot_pos[0]][bot_pos[1]] == 2:
            print("The bot has caught fire!")
            frames.append(np.copy(grid))
            log_data['result'] = 'Bot caught fire'
            break
        if grid[dest[0]][dest[1]] == 2:
            print("The button has caught fire!")
            frames.append(np.copy(grid))
            log_data['result'] = 'Button caught fire'
            break

        t += 1

    log_data['steps'] = t
    log_results(log_data)
    # Save the final frame
    save_final_frame(frames[-1], filename=f'/Users/drcrocs22/Developer/Rutgers Projects/Intro To AI/PROJECT_1_FINAL/final_frames/{run_id}.png')
    if trial == 0:
        visualize_simulation(frames)
    return log_data

def track_path_bot1(cell_details, dest):
    path = []
    i, j = dest
    while not (cell_details[i][j].parent_i == i and cell_details[i][j].parent_j == j):
        path.append((i, j))
        temp_i = cell_details[i][j].parent_i
        temp_j = cell_details[i][j].parent_j
        i, j = temp_i, temp_j
    path.append((i, j))
    path.reverse()
    return path

def bot_planning_bot1(closed_list, cell_details, open_list, src, dest, grid, found_dest, n, t):
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
                if not closed_list[new_i][new_j] and is_unblocked_bot_1(grid, new_i, new_j, t):
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

# def calculate_euclidean_distance(row, col, dest):
#     # Euclidean distance = sqrt((x1 - x2)^2 + (y1 - y2)^2)
#     return ((row - dest[0])**2 + (col - dest[1])**2)**0.5