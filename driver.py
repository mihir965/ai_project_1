from environment_utils import grid_init, button_init, bot_init, fire_init_fn
import sys
import os
from Bot import *
import numpy as np
import random

n = 40
q = 0.6

seed_value = random.randrange(1, 100)
print(seed_value)
random.seed(seed_value)
np.random.seed(seed_value)

grid = grid_init(n)
button_pos = button_init(grid, n, 3)
bot_pos = bot_init(grid, n, 4)
fire_init = fire_init_fn(grid, n, 2)

frames_bot1 = []
frames_bot2 = []
frames_bot3 = []

print("Bot 1")
random.seed(seed_value)
np.random.seed(seed_value)
time_lapse_fn_bot_1(grid.copy(), q, n, frames_bot1, bot_pos, button_pos, fire_init)

print("Bot 2")
random.seed(seed_value)
np.random.seed(seed_value)
time_lapse_fn_bot2(grid.copy(), q, n, frames_bot2, bot_pos, button_pos, fire_init)

print("Bot 3")
random.seed(seed_value)
np.random.seed(seed_value)
time_lapse_fn_bot3(grid.copy(), q, n, frames_bot3, bot_pos, button_pos, fire_init)