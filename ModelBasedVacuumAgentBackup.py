from agents import * # Includes locations

# Define two locations for the two-state environment
loc_A, loc_B = (0, 0), (1, 0)

# To get the program to stop we need to create a subclass called ModelBasedVacuumAgent
# We would need to be able access the object that has the program attached to it
# There will be an internal model within the subclass
class ModelBasedVacuumAgent(Agent):
    def __init__(self, program):
        super().__init__()
        self.model = {loc_A: None, loc_B: None}
        self.program = program

    # def act(self, percept):
    #     location, status = percept
    #     self.model[location] = status
        
    #     # Check if both locations are clean
    #     if self.model[loc_A] == self.model[loc_B] == 'Clean':
    #         #print("Both locations are clean. Performing NoOp.")
    #         #return 'NoOp'
    #         print("Both locations are clean. Stopping agent.")
    #         model_based_reflex_agent.alive = False
    #         return
        
        # Otherwise, call the program to determine the action
    #    return self.program(percept)

# Then there will be a program outside of the class definition within this file

def program(percept):
    '''Just need to manage the two-state environment actions'''
    location, status = percept

    if status == 'Dirty':
        print('Dirty')
        return 'Suck'
    elif location == loc_A:
        print('At loc_A and it is clean')
        return 'Right'
    elif location == loc_B:
        print('At loc_B and it is clean')
        return 'Left'

# def ModelBasedVacuumAgent():
#     """An agent that keeps track of what locations are clean or dirty.
#     >>> agent = ModelBasedVacuumAgent()
#     >>> environment = TrivialVacuumEnvironment()
#     >>> environment.add_thing(agent)
#     >>> environment.run()
#     >>> environment.status == {(1,0):'Clean' , (0,0) : 'Clean'}
#     True
#     """
#     model = {loc_A: None, loc_B: None}

#     def program(percept):
#         """Same as ReflexVacuumAgent, except if everything is clean, do NoOp."""
#         location, status = percept
#         model[location] = status  # Update the model here
#         if model[loc_A] == model[loc_B] == 'Clean':
#             return 'NoOp'
#         elif status == 'Dirty':
#             return 'Suck'
#         elif location == loc_A:
#             return 'Right'
#         elif location == loc_B:
#             return 'Left'

#     return Agent(program)

# Then create the ModelBased object and attach the program to it.

# How to spot when something is done: change TrivialVacuumEnv
# Check attribute of the model and update the model attribute of the agent

# These are the two locations for the two-state environment
# loc_A, loc_B = (0, 0), (1, 0)

# Initialize the two-state environment
trivial_vacuum_env = TrivialVacuumEnvironment()
step_counter = {}

# Check the initial state of the environment
print("Begin: State of the Environment: {}.".format(trivial_vacuum_env.status))

# Create a model-based reflex agent
model_based_reflex_agent = ModelBasedVacuumAgent(program=program)

# Add the agent to the environment
trivial_vacuum_env.add_thing(model_based_reflex_agent)
print("Current agents: {} Is alive? {}.".format(trivial_vacuum_env.agents, model_based_reflex_agent.alive))
print("ModelBasedVacuumAgent is located at {}.".format(model_based_reflex_agent.location))

# Run the environment
# trivial_vacuum_env.step()
trivial_vacuum_env.run(step_counter=step_counter)
# trivial_vacuum_env.run()

# Check the current state of the environment
print("State of the Environment: {}.".format(trivial_vacuum_env.status))

print("ModelBasedVacuumAgent is located at {}.".format(model_based_reflex_agent.location))

# Check step count at finish.
print("Total steps run:", step_counter.get('steps', 0))
print("Current agents: {} Is alive? {}.".format(trivial_vacuum_env.agents, model_based_reflex_agent.alive))