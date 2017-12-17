#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  30 13:45:28 2017

@author: charlotteviner
"""

import random


class Agent():
    """
    Set up and provide methods for agents.
    
    Set up agent coordinates and provide methods to allow the agents
    to interact with the environment and with each other. Implement
    property attributes for the x and y coordinates.
    
    __init__ -- Set up agent coordinates.
    getx -- Get the x-coordinate of an agent.
    setx -- Set the x-coordinate of an agent.
    gety -- Get the y-coordinate of an agent.
    sety -- Set the y-coordinate of an agent.
    move -- Move the agents.
    eat -- Tell agent to eat the environment.
    distance_between -- Calculate distance between two agents.
    share_with_neighbours -- Tell agents to share food.
    __str__ -- Cast an agent store to a string.
    """
    
    def __init__ (self, environment, agents, y = None, x = None):
        """
        Set up agent coordinates.
        
        Args:
            environment (list) -- Environment coordinate list.
            agents (list) -- Agent coordinate list.
            y (int) -- Agent y-coordinate (default None).
            x (int) -- Agent x-coordinate (default None).
        """
        
        # Create parameters.
        self._x = 0
        self._y = 0
        
        if (x == None):
            self._x = random.randint(0, 99)
            # If x has no value, assign it a random integer.
        else:
            self._x = x
            # Otherwise, assign it the value from the web data.
            
        if (y == None):
            self._y = random.randint(0, 99)
            # If y has no value, assign it a random integer.
        else:
            self._y = y
            # Otherwise, assign it the value from the web data.
          
        # Allow agents to access environment data.
        self.environment = environment
        
        # Allow agents to access other agent positions.
        self.agents = agents
        
        # Set default agent store to zero.
        self.store = 0
    
    
    
    # Implement a property attribute for x.
    
    def getx(self):
        """
        Get the x-coordinate of an agent.
        
        Returns:
            The x-coordinate of an agent.
        """
        
        return self._x
    

    def setx(self, value):
        """
        Set the x-coordinate of an agent.
        
        Args:
            value -- An integer.
        """
        
        self._x = value
      
        
    # Define the property of x.
    x = property(getx, setx)
      
    
    # Implement a property attribute for y.
    
    def gety(self):
        """
        Get the y-coordinate of an agent.
        
        Returns:
            The y-coordinate of an agent.
        """
        
        return self._y
    
    
    def sety(self, value):
        """
        Set the y-coordinate of an agent.
        
        Args:
            value -- An integer.
        """
        
        self._y = value
     
        
    # Define the property of y.    
    y = property(gety, sety)
      
    
    
    def move(self):
        """
        Move the agents.
        
        Move the agents by randomly increasing or decreasing the x and y
        coordinates by 1, moving the agents around a torus so they
        never move out of the frame.
        
        Returns:
            y (int) -- New y-coordinate.
            x (int) -- New x-coordinate.
        """
        
        if random.random() < 0.5:
            self._y = (self._y + 1) % 100
            
        else:
            self._y = (self._y - 1) % 100
            
        if random.random() < 0.5:
            self._x = (self._x + 1) % 100
            
        else:
            self._x = (self._x - 1) % 100
      
        
        
    def eat(self):
        """
        Tell agent to eat the environment.
        
        Tell the agents to eat 10 units of the environment if there are
        more than 10 units available at their location.
        """
        
        if self.environment[self._y][self._x] > 10:
            self.environment[self._y][self._x] -= 10
            self.store += 10 # Agent eats 10 units at each point.

            
        
    def distance_between(self, agent):
        """
        Calculate distance between two agents.
        
        Args:
            agent -- Coordinates of an agent.
            
        Returns:
            Distance between two agents.
        """
        
        return (((self._y - agent._y)**2)+((self._x - agent._x)**2))**0.5
    
    
    
    def share_with_neighbours(self, neighbourhood):
        """
        Tell agents to share food with other nearby agents.
        
        Tell the agents to share food if another agent is of a distance
        less than the neighbourhood parameter.
        
        Args:
            neighbourhood (int) -- Distance to define 'nearby'.
        """
        
        for agent in self.agents:
            # Calculate distance between the two agents.
            distance = self.distance_between(agent)
            
            if distance <= neighbourhood:
                sum = self.store + agent.store
                average = sum / 2
                self.store = average
                agent.store = average



    def __str__(self):
        """
        Cast an agent store to a string.
        
        Override the default __str__() function in the class.
        
        Returns:
            An agent's store as a string.
        """
        
        return str(self.store)
