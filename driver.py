from environment_utils import grid_init, button_init, bot_init, fire_init_fn
import sys
import os
from Bot import *

n = 40
q = 1.0
grid = grid_init(n)
button_pos = button_init(grid, n, 3)
bot_pos = bot_init(grid, n, 4)
fire_init = fire_init_fn(grid, n, 2)

frames = []
time_lapse_fn_bot_1(grid, q, n, frames, bot_pos, button_pos, fire_init)

frames = []
time_lapse_fn_bot2(grid, q, n, frames, bot_pos, button_pos, fire_init)

frames = []
time_lapse_fn_bot3(grid, q, n, frames, bot_pos, button_pos, fire_init)