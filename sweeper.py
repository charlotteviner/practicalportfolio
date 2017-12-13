#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 12:24:49 2017

@author: charlotteviner

Run the model with multiple parameters using a sweeper.

Allows the model to be run multiple times with a different number of
agents each time.

Args:
    interval (int) -- Number of times to run the sweeper.
    num_of_agents (int) -- Number of agents.
    num_of_steps (int) -- Number of iterations.
    neighbourhood (int) -- Maximum distance between agents required to 
        share data.
"""

import subprocess

# Set up parameters.
interval = 10
num_of_agents = 0
num_of_steps = 20
neighbourhood = 30

print("Sweeper initiated.")

for i in range(interval):
    num_of_agents += 10 # For each interval, increase agents by 10.
    s = "python model.py "
    s = s + str(num_of_agents) + " " + str(num_of_steps) + " " + \
    str(neighbourhood)
    subprocess.call(s, shell = True) # Input parameters into model.
    print("Running the model with " + str(num_of_agents) + " agents.")
    
print("Sweeper complete.")