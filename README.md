Authors: Mihir Atul Kulkarni; Shaivi Bansal

Overview: This is a pathfinding bot developed for navigating a D x D square grid (ship) consisting of blocked and open cells. This was the first assignment where we were to create a grid and then intialize it for simulation by opening cells based on certain conditions.

The bot initially occupies a random open cell in the grid, and moves to an adjacent cell at every time step.

At a random open cell, a fire starts. Every time step, the fire has the ability to spread to adjacent open cells. The fire cannot spread to blocekd cells. The fire spreads accoridng to the following rules: At a time step, a non-burning cell catches on fire with the probability 1 - (1-q)^k

Here:
1. q: [0-1] Flammability of the ship
2. K is the number of currently bruning neighbors of the cell

Located somewhere in the ship in an empty cell, a button that triggers the fire supression system exists.

The Task: The bot can decide which open neighbor to move to. If the bot moves to the button cell, it presses the button and the simulation is a success. Otherwise, the fire advances stochastically.
