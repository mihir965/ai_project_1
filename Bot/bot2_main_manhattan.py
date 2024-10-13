# from environment_utils import grid_init, bot_init, button_init, fire_init_fn, fire_spread, is_valid, is_destination, calculate_h_value, visualize_simulation,Cell, is_unblocked_bot_2, log_results, save_final_frame
from env_utils import *
import random
import numpy as np
import heapq
import uuid

def time_lapse_fn_bot2(grid, q, n, frames, src, dest, fire_init, seed_value, trial):

    run_id = str(uuid.uuid4())

    #For keeping track of results:
    log_data = {
        'Bot Type': 'Bot 2',
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
    if not (is_unblocked_bot_2(grid, src[0], src[1]) and is_unblocked_bot_2(grid, dest[0], dest[1])):
        print("The map is bugging")
        return
    if is_destination(src[0], src[1], dest):
        print("The bot is placed with the button! LOL")
        log_data['result'] = 'Bot already at button'
        return

    bot_pos = src
    t = 0
    
    f_x, f_y = fire_init
    grid[f_x, f_y] = 2
    frames.append(np.copy(grid))  # Append a deep copy of the grid

    while True:
        print(f"Time step: {t}")

        path = plan_path_bot2(grid, bot_pos, dest, n)
        if not path:
            print("No path found. Bot is stuck!")
            log_data['result'] = 'Path blocked'
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
            log_data['result'] = 'Success'
            break

        # Spread the fire after bot moves
        grid = fire_spread(grid, n, q)
        frames.append(np.copy(grid))  # Append a deep copy of the grid

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

        # Replan if path is blocked by fire
        if any(grid[step[0]][step[1]] == 2 for step in path[1:]):
            print("Path blocked by fire, replanning...")
            path = plan_path_bot2(grid, bot_pos, dest, n)
            if not path:
                print("Replanning failed, no path found.")
                frames.append(np.copy(grid))
                break

        t += 1

    log_data['steps'] = t
    log_results(log_data)
    # Save the final frame
    save_final_frame(frames[-1], filename=f'/Users/drcrocs22/Developer/Rutgers Projects/Intro To AI/PROJECT_1_FINAL/final_frames/{run_id}.png')
    # if trial == 0:
    #     visualize_simulation(frames)
    return log_data

def plan_path_bot2(grid, bot_pos, dest, n):
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
    cell_details, found_dest = bot_planning_bot2(closed_list, cell_details, open_list, bot_pos, dest, grid, found_dest, n)
    if found_dest:
        return track_path_bot2(cell_details, dest)
    else:
        return None

def track_path_bot2(cell_details, dest):
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

def bot_planning_bot2(closed_list, cell_details, open_list, src, dest, grid, found_dest, n):
    while len(open_list) > 0:
        p = heapq.heappop(open_list)[1]
        i, j = p

        closed_list[i][j] = True

        if is_destination(i, j, dest):
            found_dest = True
            break

        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if is_valid(i + x, j + y, n):
                if is_unblocked_bot_2(grid, i + x, j + y) and not closed_list[i + x][j + y]:
                    g_new = cell_details[i][j].g + 1
                    h_new = calculate_h_value(i + x, j + y, dest)
                    f_new = g_new + h_new

                    if cell_details[i + x][j + y].f > f_new:
                        cell_details[i + x][j + y].f = f_new
                        cell_details[i + x][j + y].g = g_new
                        cell_details[i + x][j + y].h = h_new
                        cell_details[i + x][j + y].parent_i = i
                        cell_details[i + x][j + y].parent_j = j
                        heapq.heappush(open_list, (f_new, (i + x, j + y)))

    return cell_details, found_dest