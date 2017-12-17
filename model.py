#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 12:14:36 2017

@author: charlotteviner

Create agents and provide methods to interact with the environment.

Build agents in a space and get them to interact with each other.
Read in environmental data and get the agents to interact with the
environment by moving and eating. Display the model as an animation
contained within a GUI. Provide the option of getting data by web
scraping or by parameter sweeping.

Args:
    max_store (int) -- Maximum food store of an agent.
    num_of_agents (int) -- Number of agents.
    num_of_steps (int) -- Number of iterations.
    neighbourhood (int) -- Maximum distance between agents required to 
        share data.
    
Returns:
    total (float) -- Total amount eaten by all the agents.
    store (.csv) -- File containing all totals.
    animation -- Animates the model.
    sweep_results (.csv) -- File containing sweeper outputs.
    environment (.txt) -- File containing data for the eaten
        environment.
"""


# Change backend to render as associated with TkInter.
import matplotlib
matplotlib.use('TkAgg')

import random
import matplotlib.pyplot
import matplotlib.animation
import agentframework
import csv
import sys
import tkinter
import matplotlib.backends.backend_tkagg
import requests
import bs4



# Set up list of agents.
agents = []

# Set up list of environment coordinates.
environment = []


max_store = 20000 # Set the maximum number of units an agent can eat.



if len(sys.argv) == 1: # Only run if web data is being used.
    td_ys = None
    td_xs = None
    # Request data from a website (web scraping).
    r = requests.get\
    ('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
    content = r.text
    soup = bs4.BeautifulSoup(content, 'html.parser')
    td_ys = soup.find_all(attrs = {"class" : "y"})
    td_xs = soup.find_all(attrs = {"class" : "x"})
    # Set up parameters.
    num_of_agents = 10
    num_of_steps = 100
    neighbourhood = 20
    print("Reading data from the web.")

else:
    # Run the sweeper.
    print('Argument List:', str(sys.argv))
    # Set up parameters using sweeper.
    num_of_agents = int(sys.argv[1])
    num_of_steps = int(sys.argv[2])
    neighbourhood = int(sys.argv[3])



# Set up the figure for later use in the animation.
fig = matplotlib.pyplot.figure(figsize = (7, 7))
ax = fig.add_axes([0, 0, 1, 1]) # Add axes.



# Read in environment data from text file.
f = open('in.txt', newline='')
reader = csv.reader(f, quoting = csv.QUOTE_NONNUMERIC)
for row in reader:
    rowlist = []
    for item in row:
        rowlist.append(item)
    environment.append(rowlist)
f.close() 



for i in range(num_of_agents):
    # If web scraper is being used, assign y and x values from web data.
    if len(sys.argv) == 1:
        y = int(td_ys[i].text)
        x = int(td_xs[i].text)
    else:
        # If sweeper is being used, assign y and x no value.
        y = None
        x = None
    # Append coordinates to list of agents.
    agents.append(agentframework.Agent(environment, agents, y, x))
    # All agents can access the environment and other agent positions.



carry_on = True   

def update(frame_number):
    """
    Move agents and create frames for use in animation using web data.
    
    Move the agents and get them to interact with the environment.
    Calculate the total amount eaten by all agents and appends this
    amount to a .csv file. Provide a stopping condition for the model.
    Create frames for use in the animation when the web data is being
    used.
    
    Args:
        frame_number (int) -- Number of each frame generated.
        
    Returns:
        Scatter plot of agents in the environment for each iteration.
        total (float) -- Total amount eaten by all the agents.
        store (.csv) -- File containing all totals.
    """
    
    fig.clear()
    global carry_on
    
    for j in range(num_of_steps):
        # Randomise order in which the agents are processed each step.
        random.shuffle(agents)
        for agent in agents:
            agent.move() # Agents move.
            agent.eat() # Agents eat the environment.
            agent.share_with_neighbours(neighbourhood)
            # Agents share food with neighbours when they are close.
    
    total = 0 
    
    for agent in agents:
        total += agent.store # Add to total store when an agent eats.
    
    # Create stopping condition.
    if agent.store >= max_store:
        carry_on = False
        print("Stopping condition met.\nTotal store = ", total)
        # Append total store and parameters to file 'store.csv'.
        with open('store.csv', 'a') as f1:
            f1.write(str(total) + "," + str(num_of_agents) + "," + 
                     str(num_of_steps) + "," + str(neighbourhood) + 
                     "\n")

    matplotlib.pyplot.ylim(0, 99) # Set limit of y axis.
    matplotlib.pyplot.xlim(0, 99) # Set limit of x axis.
    matplotlib.pyplot.imshow(environment) # Display environment in plot.

    for agent in agents:
        # Plot all agents on a scatter graph.
        matplotlib.pyplot.scatter(agent.x, agent.y)
    
    # Write a new text file containing data for the eaten environment.
    f2 = open('environment.txt', 'w', newline='') 
    writer = csv.writer(f2, delimiter=' ')
    for row in environment:		
        writer.writerow(row)
    f2.close()



def no_gui():
    """
    Move agents using data from the sweeper.
    
    Move the agents and get them to interact with the environment using
    the parameter sweeper.
    """
    
    for j in range(num_of_steps):
        # Randomise order in which the agents are processed each step.
        random.shuffle(agents)
        for agent in agents:
            agent.move() # Agents move.
            agent.eat() # Agents eat the environment.
            agent.share_with_neighbours(neighbourhood)
            # Agents share food with neighbours when they are close.
    
    
    
def gen_function(b = [0]):
    """
    Stop creating frames when stopping condition is met.
    
    Generator function that determines when frames should stop being
    created by checking whether the maximum number of iterations and/or
    the stopping condition has been met.
    """
    
    a = 0
    global carry_on
    while (a < num_of_steps) & (carry_on) :
        yield a # Return control and wait next call.
        a = a + 1
    


def run():
    """
    Run the animation.
    
    Run the animation, using the generator function, to determine the
    number of frames.
    
    Returns:
        animation -- Animates the model.
    """
    
    animation = matplotlib.animation.FuncAnimation(fig, update, repeat = False,
                                                   frames = gen_function)
    # Number of frames in animation determined by generator function.
    canvas.show() # Show animation in matplotlib canvas.



if len(sys.argv) == 1: # GUI only created if the web data is being used.
    root = tkinter.Tk() # Build the main GUI window.
    root.wm_title("Model") # Set the main window title.
    # Create a matplotlib canvas embedded within the GUI window.
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master = 
                                                                 root)
    canvas._tkcanvas.pack(side = tkinter.TOP, fill = tkinter.BOTH, expand = 1)

    # Create a menu.
    menu_bar = tkinter.Menu(root)
    root.config(menu=menu_bar)
    model_menu = tkinter.Menu(menu_bar)
    menu_bar.add_cascade(label="Model", menu=model_menu)
    # Associate menu with the run function.
    model_menu.add_command(label="Run model", command=run)
    
    tkinter.mainloop() # Set the GUI to wait for events.

else:
    for i in range(num_of_steps):
        no_gui() # Do not create GUI if sweeper is being used.
    
    total = 0 # Set up parameter for total amount stored by agents.
    
    for agent in agents:
        total += agent.store # Add to the total each time an agent eats.
    
    # Append total and parameters used to file 'sweep_results.csv'.   
    with open('sweep_results.csv', 'a') as f3:
        f3.write(str(total) + "," + sys.argv[1] + "," + sys.argv[2] + 
                 "," + sys.argv[3] + "\n")