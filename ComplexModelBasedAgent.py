'''
*************************************************************************
* File Name: ComplexModelBasedVacuumAgent.py
* Description: AI Assessment 1 - Exercise 3
* Programmer: Alan Ryan (s00248142)
* Date: 31/10/2024
* Version: 1.0
**************************************************************************
'''

from agents import * # Includes locations
from stack import Stack # Stack structure from Robin Andrews
from helpers import offsets # Helpers file from Robin Andrews
import random

'''is_legal_pos is a modified version of Robin Andrew's code, minus obstacles.
    It defines the boundarys of the environent for the DFS algorithm'''
def is_legal_pos(grid, pos):
    i, j = pos
    num_rows = len(grid)
    num_cols = len(grid[0])
    return 0 <= i < num_rows and 0 <= j < num_cols

def print_grid_status(status, title):
        grid = []
        grid = [[(i, j)
                  for j in range(self.columns)] 
                  for i in range(self.rows)]
        print(title)



# --------------------- Expanded Environment Subclass --------------------------

class ExpandedVacuumEnvironment(Environment):
    """This environment has a gridded N x N environment (3 x 3).
    Each can be Dirty or Clean.
    The agent perceives its location and the location's status.
    This serves as an example of how to implement a complex Environment."""

    def __init__(self):
        super().__init__()
        # Specify dimensions of desired environment
        self.rows = 3
        self.columns = 3
        # Generate grid using tuples contains in a matrix using dimensions above
        self.grid = [[(i, j)
                      for j in range(self.columns)] 
                      for i in range(self.rows)]
        # Create a dictionary to hold the clean/dirty status of each location
        self.status = {}
        for row in self.grid:
            for item in row:
                self.status[item] = random.choice(['Clean', 'Dirty'])

    def thing_classes(self):
        return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent, 
                TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location."""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        if thing in self.things:
            print("Can't add the same thing twice")
        else:
            thing.location = location if location is not None \
                else self.default_location(thing)
            self.things.append(thing)
            if isinstance(thing, Agent):
                thing.performance = 0
                self.agents.append(thing)
        '''Initialise the agent DFS stack list and predecessor dictionary'''
        if hasattr(thing, 'dfs_stack') and thing.dfs_stack:
            thing.dfs_stack.push(location)
            thing.predecessors.update({location: None})
            thing.model = {}
            for row in self.grid:
                for item in row:
                    thing.model[item] = None

    def percept(self, agent):
        """Returns the agent's location, and the 
        location status (Dirty/Clean)."""
        return agent.location, self.status[agent.location]

    def execute_action(self, agent, action): # Usually called from Env step()
        """Change agent's location and/or location's status; track performance.
        Score 10 for each dirt cleaned; -1 for each move."""
        '''The "Move" section is a subsection of the DFS algorithm'''
        if action == 'Move':
            # For model-based agents we can update the model using hasattr()
            # with the Dirty/Clean status of current location
            if hasattr(agent, 'model') and agent.model:
                agent.model[agent.location] = self.status[agent.location]
            
            # Next, update predecessors and move agent to new location
            if not agent.dfs_stack.is_empty():
                next_cell = agent.dfs_stack.peek()
                agent.location = next_cell
                print('Action: Moved to {}'.format(next_cell))
            else:
                print('No action!')
        elif action == 'Suck':
            if self.status[agent.location] == 'Dirty':
                agent.performance += 10
            print('Action: {}'.format(action)) # Helps track progress
            self.status[agent.location] = 'Clean'
            
            # Update status of location on the agent model
            if hasattr(agent, 'model') and agent.model:
                # agent.model[agent.location] = 'Clean'
                agent.model[agent.location] = self.status[agent.location]


# ---------- Complex MB Agent (Subclass of Agent (Subclass of Thing) -----------

class Complex_MB_Vac_Agent(Agent):
    def __init__(self, program_agent_input):
        super().__init__()
        self.model = {}             # Initialised during add_thing
        self.program = program_agent_input
        self.dfs_stack = Stack()    # Stack used in DFS search
        self.predecessors = {}      # Essential part of DFS search
        self.visited = []           # Stores path for later extraction
        

# ------------------------------ DFS Program -----------------------------------

'''Define the program that the agent will use. This program will take a percept
as an input parameter from step()'''
def dfs_program(percept_program_input):
    location, status = percept_program_input
    agent = complex_m_based_agent
    grid = expanded_vacuum_env.grid
    if location not in agent.visited: # Update 'visited' list for DFS trace
        agent.visited.append(location)

    # First if statement checks for finish (goal) and stops the agent
    if all(status == 'Clean' for status in agent.model.values()):
        agent.alive = False # Stops 'step()' method in Env
        print("\n>>>All locations in model are 'Clean'. Program is finished<<<")
    
    # Next elif is first part of DFS algorithm (pop stack, push predecessors)
    # The 'Move' action is returned to execute_action() for next part of DFS
    elif status == 'Clean':
        print('At {}: It is clean.'.format(location), end=" ")

        # Pop stack to make space for discovered neighbours (1st step in DFS)
        if not agent.dfs_stack.is_empty():
            current_cell = agent.dfs_stack.pop()

        # Discover next possible cells
        for direction in ["up", "right", "down", "left"]:
            row_offset, col_offset = offsets[direction]
            neighbour = (current_cell[0] + row_offset,
                         current_cell[1] + col_offset)
            if is_legal_pos(grid, neighbour) and \
                neighbour not in agent.predecessors: # Checks against dict keys
                agent.dfs_stack.push(neighbour) # Add discovered to stack
                agent.predecessors[neighbour] = current_cell
        return 'Move'
    
    # This elif simply identifies a dirty location to be cleaned.
    elif status == 'Dirty':
        print('At {}: It is dirty.'.format(location), end=" ")
        return 'Suck'
    else:
        print('ERROR at {}: It neither clean or dirty'.format(location))


# -------------------- Agent & Enviornment Setup and Run -----------------------

# 1 Create a model-based reflex agent object and attach the chosen program
complex_m_based_agent = Complex_MB_Vac_Agent(program_agent_input=dfs_program)


# 2 Create the two-state environment object
expanded_vacuum_env = ExpandedVacuumEnvironment()
my_step_counter = {} # Step counter to show when agent finishes
start_loc = (0,0) # Start position of the agent


# 3 Add the agent to the environment with a starting location of (0,0)
expanded_vacuum_env.add_thing(complex_m_based_agent, location=start_loc)

print("Current agents: {} Is alive? {}."\
      .format(expanded_vacuum_env.agents, complex_m_based_agent.alive))
print("\n\nAgent added to environment at location: {}."\
      .format(complex_m_based_agent.location))
print("Initial Environment: {}.".format(expanded_vacuum_env.status))
print("Initial Agent Model: {}.".format(complex_m_based_agent.model))


# 4 Run the environment
expanded_vacuum_env.run(step_counter=my_step_counter)

# After running, display final state of agent, model, and environment. 
print("Final Environment: {}.".format(expanded_vacuum_env.status))
print("Final Agent Model: {}.".format(complex_m_based_agent.model))
print("Agent is located at {}.".format(complex_m_based_agent.location))
print("Path taken: {}".format(complex_m_based_agent.visited))
print("Total steps ran:", my_step_counter.get('steps', 0))
print("Current agents: {} Is alive? {}."\
      .format(expanded_vacuum_env.agents, complex_m_based_agent.alive))
