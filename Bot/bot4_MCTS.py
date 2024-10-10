from environment_utils import *
import numpy as np
import copy

class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.action = action
        self.visits = 0
        self.reward = 0.0

    def is_fully_expanded(self):
        possible_actions = get_possible_actions()


def get_possible_actions(bot_pos, grid):
    actions = []
    n = len(grid)
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    for dx, dy in directions:
        new_x, new_y = bot_pos[0] + dx, bot_pos[y] + dy
        if is_valid(new_x, new_y, n):
            cell_value = grid[new_x][new_y]
            if is_valid(new_x, new_y, n):
                cell_value = grid[new_x][new_y]
                if cell_value!=1 and cell_value != 2:
                    actions.append((dx, dy))
    return actions

def apply_action(state, action, q):
    bot_pos, grid = state
    n = len(grid)
    new_bot_pos = (bot_pos[0] + action[0], bot_pos[1] + action[1])

    new_grid = np.copy(grid)
    new_grid[bot_pos[0]][bot_pos[1]] = 0
    new_grid[new_bot_pos[0]][new_bot_pos[1]] = 4

    new_grid = fire_spread(new_grid, n, q)
    
    return (new_bot_pos, new_grid)

def rollout_policy(possibly_actions):
    return random.choice(possibly_actions)

def rollout(node, dest):
    current_state = node.state
    depth = 0
    max_depth = 20
    while depth < max_depth:
        bot_pos, grid = current_state
        if is_destination(bot_pos[0], bot_pos[1], dest):
            return 1.0
        if grid[bot_pos[0]][bot_pos[1]] == 2:
            return -1.0
        possible_actions = get_possible_actions(bot_pos, grid)
        if not possible_actions:
            return -1.0
        action = rollout_policy(possible_actions)
        current_state = apply_action(current_state, action)
        depth+=1
    return 0.0

def backpropogate(node, reward):
    while node is not None:
        node.visits +=1
        node.reward += reward
        node = node.parent

def mcts(root_state, max_iterations=100):
    root_node = MCTSNode(root_state)
    for _ in range(max_iterations):
        node = root_node
        while node.is_fully_expanded() and node.children:
            node = node.best_child()