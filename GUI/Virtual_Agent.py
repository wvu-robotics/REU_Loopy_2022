import random
# import Controls


def update_torque(Agent):
    pass
    # Agent.torque = int(random.randrange(-1,100))
    ## call Nate's function that reads in load, adjust to be out of 100


def update_goal_angle(Agent):
    Agent.goal = int(random.randrange(0,359))


def update_current_angle(Agent):
    # Agent.angle = int(random.randrange(0,359))
    Agent.angle = int(170)
    # Loopy.agents


class Agent:
    def __init__(self, name, torque, goal, angle, real_agent):
        self.name = name
        self.torque = torque     #torque (#s, off good high)
        self.goal = goal      #goal angle
        self.angle = angle      #current angle
        self.real_agent = real_agent
    


