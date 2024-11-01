from agents import * # Includes locations

# Define two locations for the two-state environment
loc_A, loc_B = (0, 0), (1, 0)


class ModelBasedVacuumAgent(Agent):
    def __init__(self, program):
        super().__init__()
        self.model = {loc_A: None, loc_B: None}
        self.program = program

    # def update_model(percept):
    #     location, status = percept
    #     self.model[location] = status  # Update model based on the agent's perception
    
    # def killEnv():
    #     if self.model[loc_A] == self.model[loc_B] == 'Clean':
    #         trivial_vacuum_env.is_done()
    #         return 'NoOp'

# Then there will be a program outside of the class definition within this file

def program(percept):
    '''Just need to manage the two-state environment actions'''
    location, status = percept
    #model_based_reflex_agent.update_model(percept)
    
    #model_based_reflex_agent.killEnv()
    if model_based_reflex_agent.model[loc_A] == model_based_reflex_agent.model[loc_B] == 'Clean':
        trivial_vacuum_env.is_done()

    if status == 'Dirty':
        print('Dirty')
        return 'Suck'
    elif location == loc_A:
        print('At loc_A and it is clean')
        return 'Right'
    elif location == loc_B:
        print('At loc_B and it is clean')
        return 'Left'

# 2
# Initialize the two-state environment
trivial_vacuum_env = TrivialVacuumEnvironment()
step_counter = {}

# Check the initial state of the environment
print("Begin: State of the Environment: {}.".format(trivial_vacuum_env.status))

# 1
# Create a model-based reflex agent
model_based_reflex_agent = ModelBasedVacuumAgent(program=program)
print(model_based_reflex_agent.model)
# 3
# Add the agent to the environment
trivial_vacuum_env.add_thing(model_based_reflex_agent)
print("Current agents: {} Is alive? {}.".format(trivial_vacuum_env.agents, model_based_reflex_agent.alive))
print("ModelBasedVacuumAgent is located at {}.".format(model_based_reflex_agent.location))
print(model_based_reflex_agent.model)

# Run the environment
# trivial_vacuum_env.step()
trivial_vacuum_env.run(step_counter=step_counter)
# trivial_vacuum_env.run()
print(model_based_reflex_agent.model)
# Check the current state of the environment
print("State of the Environment: {}.".format(trivial_vacuum_env.status))
print("ModelBasedVacuumAgent is located at {}.".format(model_based_reflex_agent.location))

# Check step count at finish.
print("Total steps run:", step_counter.get('steps', 0))
print("Current agents: {} Is alive? {}.".format(trivial_vacuum_env.agents, model_based_reflex_agent.alive))