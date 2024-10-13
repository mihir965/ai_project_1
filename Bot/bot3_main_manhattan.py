# from environment_utils import grid_init, bot_init, button_init, fire_init_fn, fire_spread, is_valid, is_destination, calculate_h_value, visualize_simulation,Cell, is_unblocked_bot_3, is_fire, log_results, save_final_frame
from env_utils import *
import random
import numpy as np
import heapq
import uuid

def time_lapse_fn_bot3(grid, q, n, frames, src, dest, fire_init, seed_value, trial):

    run_id = str(uuid.uuid4())

    #For keeping track of results:
    log_data = {
        'Bot Type': 'Bot 3',
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

    def plan_path_bot3():
        # First attempt: Avoid cells adjacent to fire cells
        print("Attempting to find path avoiding adjacent fire cells.")
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
        cell_details, found_dest = bot_planning_bot3(closed_list, cell_details, open_list, bot_pos, dest, grid, found_dest, n, avoid_adjacent_cells=True)
        if found_dest:
            return track_path_bot3(cell_details, dest, bot_pos, n)
        else:
            # Fallback: Avoid only current fire cells
            print("No path found avoiding adjacent fire cells. Trying to find path avoiding fire cells only.")
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
            cell_details, found_dest = bot_planning_bot3(closed_list, cell_details, open_list, bot_pos, dest, grid, found_dest, n, avoid_adjacent_cells=False)
            if found_dest:
                return track_path_bot3(cell_details, dest, bot_pos, n)
            else:
                return None

    while True:
        print(f"Time step: {t}")

        # Replan path at every time step
        path = plan_path_bot3()
        if not path:
            print("The bot has no path to the button due to the fire.")
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
            # Empty path (should not occur)
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
    if trial==0:
        visualize_simulation(frames)
    return log_data

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

def bot_planning_bot3(closed_list, cell_details, open_list, src, dest, grid, found_dest, n, avoid_adjacent_cells):
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
                if not closed_list[new_i][new_j] and is_unblocked_bot_3(grid, new_i, new_j, avoid_adjacent_cells) and not is_fire(grid, new_i, new_j):
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