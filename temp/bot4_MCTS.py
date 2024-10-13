from env_utils import *
import heapq
import numpy as np
import uuid
import copy
import random
import math
import time

def time_lapse_fn_bot4(grid, q, n, frames, src, dest, fire_init, seed_value):
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

    # Main loop
    while True:
        print(f"Time step: {t}")

        # Use MCTS to decide the next move
        next_move = mcts_decision(grid, bot_pos, dest, q, n, t)

        if next_move is None:
            print("No possible moves. Bot is stuck.")
            log_data['result'] = 'Bot stuck'
            break

        # Move the bot
        grid[bot_pos[0]][bot_pos[1]] = 0  # Clear previous position
        bot_pos = next_move
        if grid[bot_pos[0]][bot_pos[1]] == 2:
            print("The bot ran into the fire!")
            log_data['result'] = 'Bot caught fire'
            frames.append(np.copy(grid))
            break
        grid[bot_pos[0]][bot_pos[1]] = 4
        frames.append(np.copy(grid))

        # Check if bot has reached the destination
        if is_destination(bot_pos[0], bot_pos[1], dest):
            print("The bot has reached the button.")
            log_data['result'] = 'Success'
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


def mcts_decision(grid, bot_pos, dest, q, n, t, simulations=100):
    """
    Perform MCTS to decide the next move.
    """
    class Node:
        def __init__(self, state, parent=None, action=None):
            self.state = state
            self.parent = parent
            self.children = []
            self.visits = 0
            self.reward = 0.0
            self.action = action

        def is_fully_expanded(self):
            return len(self.children) == len(get_valid_actions(self.state[0], self.state[1], n))

        def best_child(self, c_param=1.4):
            choices_weights = [
                (child.reward / child.visits) + c_param * math.sqrt((2*math.log(self.visits) / child.visits))
                for child in self.children
            ]
            return self.children[np.argmax(choices_weights)]

    def tree_policy(node):
        while True:
            if is_terminal(node.state, dest):
                return node
            if not node.is_fully_expanded():
                return expand(node)
            else:
                node = node.best_child()

    def expand(node):
        tried_actions = [child.action for child in node.children]
        possible_actions = get_valid_actions(node.state[0], node.state[1], node.state[1].shape[0])
        for action in possible_actions:
            if action not in tried_actions:
                next_state = step(node.state, action, q, n)
                child_node = Node(next_state, parent=node, action=action)
                node.children.append(child_node)
                return child_node
        return node  # Should not reach here

    def default_policy(state):
        current_state = copy.deepcopy(state)
        for _ in range(10):  # Limit the rollout depth
            if is_terminal(current_state, dest):
                break
            actions = get_valid_actions(current_state[0], current_state[1], n)
            if not actions:
                break
            action = random.choice(actions)
            current_state = step(current_state, action, q, n)
        return rollout_reward(current_state, dest)

    def backup(node, reward):
        while node is not None:
            node.visits += 1
            node.reward += reward
            print(
                "Node:", node, "Visits:", node.visits, "Reward:", node.reward 
            )
            node = node.parent

    root = Node((bot_pos, grid))
    for _ in range(simulations):
        leaf = tree_policy(root)
        reward = default_policy(leaf.state)
        backup(leaf, reward)

    # Choose the action with the highest visit count
    if not root.children:
        return None  # No possible moves

    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.state[0]

def get_valid_actions(bot_pos, grid, n):
    actions = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dir in directions:
        new_i, new_j = bot_pos[0] + dir[0], bot_pos[1] + dir[1]
        if is_valid(new_i, new_j, n) and grid[new_i][new_j] in [0, 3]:
            actions.append((new_i, new_j))
    return actions

def step(state, action, q, n):
    bot_pos, grid = state
    new_grid = copy.deepcopy(grid)
    new_bot_pos = action
    # Move the bot
    new_grid[bot_pos[0]][bot_pos[1]] = 0  # Clear previous position
    new_grid[new_bot_pos[0]][new_bot_pos[1]] = 4  # Set new position

    # Spread the fire
    new_grid = fire_spread(new_grid, n, q)
    return (new_bot_pos, new_grid)

def is_terminal(state, dest):
    bot_pos, grid = state
    # Check if bot has reached the destination or caught fire
    if grid[bot_pos[0]][bot_pos[1]] == 2:
        return True  # Bot caught fire
    if is_destination(bot_pos[0], bot_pos[1], dest):
        return True  # Reached destination
    return False

def rollout_reward(state, dest):
    bot_pos, grid = state
    if grid[bot_pos[0]][bot_pos[1]] == 2:
        return -1  # Bad outcome
    if is_destination(bot_pos[0], bot_pos[1], dest):
        return 1  # Good outcome
    # Intermediate reward: negative distance to goal
    return -calculate_h_value(bot_pos[0], bot_pos[1], dest)
