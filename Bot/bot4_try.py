import random
import math
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import heapq
import matplotlib.animation
import os
import csv
from env_utils import *
import uuid

class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0
        self.row = 0
        self.col = 0

class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.action = action
        self.visits = 0
        self.reward = 0.0

    def is_fully_expanded(self, n):
        bot_pos, grid = self.state
        possible_actions = get_possible_actions(bot_pos, grid, n)
        return len(self.children) == len(possible_actions)
    
    def expand(self, q, n):
        bot_pos, grid = self.state
        tried_actions = [child.action for child in self.children]
        possible_actions = get_possible_actions(bot_pos, grid, n)
        for action in possible_actions:
            if action not in tried_actions:
                new_state = apply_action(self.state, action, q, n)
                child_node = MCTSNode(new_state, parent=self, action=action)
                self.children.append(child_node)
                return child_node
        return None
    
    def best_child(self, c_param=2.0):
        choices_weights = [
            (child.reward / child.visits) + c_param * np.sqrt((2 * np.log(self.visits) / child.visits)) + random.uniform(0, 0.01)
            for child in self.children
        ]
        return self.children[np.argmax(choices_weights)]

def get_possible_actions(bot_pos, grid, n):
    actions = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        new_x, new_y = bot_pos[0] + dx, bot_pos[1] + dy
        if is_valid(new_x, new_y, n):
            cell_value = grid[new_x][new_y]
            if cell_value != 1 and cell_value != 2:
                actions.append((dx, dy))
    return actions

def apply_action(state, action, q, n):
    bot_pos, grid = state
    new_bot_pos = (bot_pos[0] + action[0], bot_pos[1] + action[1])

    new_grid = np.copy(grid)
    new_grid[bot_pos[0]][bot_pos[1]] = 0
    new_grid[new_bot_pos[0]][new_bot_pos[1]] = 4

    new_grid = fire_spread(new_grid, n, q)
    
    return (new_bot_pos, new_grid)

def rollout_policy(bot_pos, possible_actions, dest, previous_pos=None):
    # Avoid going back to the previous position
    if previous_pos:
        possible_actions = [action for action in possible_actions if (bot_pos[0] + action[0], bot_pos[1] + action[1]) != previous_pos]

    # If actions are left after filtering, choose a random one; otherwise, use original list
    if possible_actions:
        if random.random() < 0.3:  # Add randomness to explore more paths
            return random.choice(possible_actions)

        # Otherwise, choose action minimizing distance to destination
        distances = []
        for action in possible_actions:
            new_pos = (bot_pos[0] + action[0], bot_pos[1] + action[1])
            distance = abs(new_pos[0] - dest[0]) + abs(new_pos[1] - dest[1])
            distances.append((distance, action))
        distances.sort()
        return distances[0][1]
    else:
        return random.choice(possible_actions)

def rollout(node, dest, q, n):
    current_state = node.state
    depth = 0
    max_depth = 15  # Increased depth limit
    previous_pos = None
    visited_states = set()

    while depth < max_depth:
        bot_pos, grid = current_state
        visited_states.add(bot_pos)

        if is_destination(bot_pos[0], bot_pos[1], dest):
            return 1.0
        if grid[bot_pos[0]][bot_pos[1]] == 2:
            return -1.0
        possible_actions = get_possible_actions(bot_pos, grid, n)
        if not possible_actions:
            return -1.0
        action = rollout_policy(bot_pos, possible_actions, dest, previous_pos)
        previous_pos = bot_pos
        current_state = apply_action(current_state, action, q, n)
        depth += 1

    return 0.0

def backpropagate(node, reward):
    while node is not None:
        node.visits += 1
        node.reward += reward
        node = node.parent

def mcts(root_state, dest, q, n, max_iterations=200):  # Increased number of iterations
    root_node = MCTSNode(root_state)
    for _ in range(max_iterations):
        node = root_node
        # Selection step
        while node.is_fully_expanded(n) and node.children:
            node = node.best_child()
        # Expansion step
        if not node.is_fully_expanded(n):
            child = node.expand(q, n)
            if child is not None:
                reward = rollout(child, dest, q, n)
                backpropagate(child, reward)
                continue
        # Rollout and backpropagation for non-expanded nodes
        reward = rollout(node, dest, q, n)
        backpropagate(node, reward)
    
    # Choose the best action from the root node's children
    if root_node.children:
        best_child = max(root_node.children, key=lambda c: c.visits)
        return best_child.action
    else:
        return None

def time_lapse_fn_bot4_try(grid, q, n, frames, src, dest, fire_init, seed_value):
    run_id = str(uuid.uuid4())

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
    
    bot_pos = src
    t = 0

    grid[fire_init[0]][fire_init[1]] = 2
    frames.append(np.copy(grid))

    while True:
        print(f"Time step: {t}")

        root_state = (bot_pos, grid.copy())
        action = mcts(root_state, dest, q, n, max_iterations=50)  # Increase iterations for better exploration

        if action is None:
            print("The bot has no valid actions.")
            frames.append(np.copy(grid))
            log_data['result'] = 'No valid actions'
            break

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

        grid[bot_pos[0]][bot_pos[1]] = 0
        bot_pos = new_bot_pos
        grid[bot_pos[0]][bot_pos[1]] = 4
        frames.append(np.copy(grid))
        print(f"Bot moved to {bot_pos}")

        if is_destination(bot_pos[0], bot_pos[1], dest):
            print("The bot has reached the button.")
            frames.append(np.copy(grid))
            log_data['result'] = 'Success'
            break

        grid = fire_spread(grid, n, q)
        frames.append(np.copy(grid))

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
    save_final_frame(frames[-1], filename=log_data['final_frame'])
    visualize_simulation(frames)
