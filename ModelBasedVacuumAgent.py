'''
*************************************************************************
* File Name: ModelBasedVacuumAgent.py
* Description: AI Assessment 1 - Exercise 2
* Programmer: Alan Ryan (s00248142)
* Date: 31/10/2024
* Version: 1.0
**************************************************************************
'''

from agents import * # Includes locations A and B

# ----------- Simple MB Agent (Subclass of Agent (Subclass of Thing) -----------

'''Create subclass for a model based vacuum agent with an 'Agent' superclass.
Include a model of the locations with empty status on object instantiation.
The agent object will be attached to a program passed in as a parameter during
creation.'''
class ModelBasedVacuumAgent(Agent):
    def __init__(self, program_agent_input):
        super().__init__()
        self.model = {loc_A: None, loc_B: None}
        self.program = program_agent_input

# --------------------------------- Program ------------------------------------

'''Define the program that the agent will use. This program will take a percept
as an input parameter from '''
def my_program(percept_program_input):
    '''Just need to manage the two-state environment actions'''
    location, status = percept_program_input

    if (
    model_based_reflex_agent.model[loc_A]
    == model_based_reflex_agent.model[loc_B] 
    == 'Clean'
    ):
        model_based_reflex_agent.alive = False # Stops 'step()' method in Env
        print("All locations in model are 'Clean'. Program is finished.")
    elif status == 'Dirty':
        print('At {}: It is dirty'.format(location))
        action = 'Suck'
        return action
    elif location == loc_A:
        print('At {}: It is clean'.format(location))
        action = 'Right'
        return action
    elif location == loc_B:
        print('At {}: It is clean'.format(location))
        action = 'Left'
        return action

# -------------------- Agent & Enviornment Setup and Run -----------------------

# 1 Create a model-based reflex agent object and attach the chosen program
model_based_reflex_agent = ModelBasedVacuumAgent(program_agent_input=my_program)

# 2 Create the two-state environment object
trivial_vacuum_env = TrivialVacuumEnvironment()
my_step_counter = {} # Step counter to show when agent finishes

# 3 Add the agent to the environment
trivial_vacuum_env.add_thing(model_based_reflex_agent)
print("Current agents: {} Is alive? {}."\
      .format(trivial_vacuum_env.agents, model_based_reflex_agent.alive))
print("ModelBasedVacuumAgent added to environment at location: {}."\
      .format(model_based_reflex_agent.location))
print("Initial Environment: {}.".format(trivial_vacuum_env.status))
print("Initial Agent Model: {}.".format(model_based_reflex_agent.model))

# 4 Run the environment
trivial_vacuum_env.run(step_counter=my_step_counter)

# After running, display final state of agent, model, and environment. 
print("Final Environment: {}.".format(trivial_vacuum_env.status))
print("Final Agent Model: {}.".format(model_based_reflex_agent.model))
print("ModelBasedVacuumAgent is located at {}."\
      .format(model_based_reflex_agent.location))
print("Total steps ran:", my_step_counter.get('steps', 0))
print("Current agents: {} Is alive? {}."\
      .format(trivial_vacuum_env.agents, model_based_reflex_agent.alive))