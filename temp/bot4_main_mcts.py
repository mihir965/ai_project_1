from bot4_MCTS import *
import uuid
from environment_utils import *

def time_lapse_fn_bot4(grid, q, n, frames, src, dest, fire_init):
    run_id = str(uuid.uuid4())

    # For logging results
    log_data = {
        'Bot Type': 'Bot 4',
        'run_id': run_id,
        'q': q,
        'bot_pos_init': src,
        'button_pos_init': dest,
        'fire_init': fire_init,
        'steps': 0,
        'result': '',
        'final_frame': f'/Users/drcrocs22/Developer/Rutgers Projects/Intro To AI/PROJECT_1_FINAL/final_frames/{run_id}.png'
    }

    print(f"The bot is placed in position: {src}, button position is: {dest}")
    if not is_valid(src[0], src[1], n) or not is_valid(dest[0], dest[1], n):
        print("Invalid positions")
        return
    if is_destination(src[0], src[1], dest):
        print("The bot is placed with the button! LOL")
        log_data['result'] = 'Bot already at button'
        return  
    
    # Initialize bot position and time
    bot_pos = src
    t = 0

    # Initialize fire
    grid[fire_init[0]][fire_init[1]] = 2
    frames.append(np.copy(grid))

    while True:
        print(f"Time step: {t}")

        # Use MCTS to decide the next move
        root_state = (bot_pos, grid.copy())
        action = mcts(root_state, max_iterations=100)

        if action is None:
            print("The bot has no valid actions.")
            frames.append(np.copy(grid))
            log_data['result'] = 'No valid actions'
            break

        # Apply the action
        new_bot_pos = (bot_pos[0] + action[0], bot_pos[1] + action[1])
        if not is_valid(new_bot_pos[0], new_bot_pos[1], n):
            print("Invalid move.")
            frames.append(np.copy(grid))
            log_data['result'] = 'Invalid move'
            break

        if grid[new_bot_pos[0]][new_bot_pos[1]] == 2:
            print("The bot ran into the fire!")
            frames.append(np.copy(grid))
            log_data['result'] = 'Bot caught fire'
            break

        # Move the bot
        grid[bot_pos[0]][bot_pos[1]] = 0
        bot_pos = new_bot_pos
        grid[bot_pos[0]][bot_pos[1]] = 4
        frames.append(np.copy(grid))
        print(f"Bot moved to {bot_pos}")

        # Check if bot reached the destination
        if is_destination(bot_pos[0], bot_pos[1], dest):
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
            log_data['result'] = 'Bot caught fire'
            break
        if grid[dest[0]][dest[1]] == 2:
            print("The button has caught fire!")
            log_data['result'] = 'Button caught fire'
            break

        t += 1

    log_data['steps'] = t
    log_results(log_data)
    # Save the final frame
    save_final_frame(frames[-1], filename=f'/Users/drcrocs22/Developer/Rutgers Projects/Intro To AI/PROJECT_1_FINAL/final_frames/{run_id}.png')
    visualize_simulation(frames)