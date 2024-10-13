# from environment_utils import *
from env_utils import *
import sys
import os
from Bot import *
import numpy as np
import random

n = 40
q = 0.45

seed_value = random.randrange(1, 1000)
# seed_value = 27
# seed_value = 999
# seed_value = 176
# seed_value = 616
# seed_value = 29
# seed_value = 604
# seed_value = 195
# seed_value = 964
# seed_value = 867
seed_value = 809
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
frames_bot4 = []

print("Bot 1")
random.seed(seed_value)
np.random.seed(seed_value)
time_lapse_fn_bot_1(grid.copy(), q, n, frames_bot1, bot_pos, button_pos, fire_init, seed_value)

print("Bot 2")
random.seed(seed_value)
np.random.seed(seed_value)
time_lapse_fn_bot2(grid.copy(), q, n, frames_bot2, bot_pos, button_pos, fire_init, seed_value)

print("Bot 3")
random.seed(seed_value)
np.random.seed(seed_value)
time_lapse_fn_bot3(grid.copy(), q, n, frames_bot3, bot_pos, button_pos, fire_init, seed_value)

print("Bot 4")
random.seed(seed_value)
np.random.seed(seed_value)
time_lapse_fn_bot4_prob(grid.copy(), q, n, frames_bot4, bot_pos, button_pos, fire_init, seed_value)