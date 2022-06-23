import random
from Controls import Loopy 

def TourqeState(Agent):
    Agent.state = int(random.randrange(-1,100)) ##change to actual range later - 0 low/off grey, 1 med/good green, 2 high/danger red

def GoalAngle(Agent):
    Loopy.Loopy.agents[Agent.name].set_goal_angle( Agent.goal )

def CurrentAngle(Agent):
    Agent.angle = int(random.randrange(0,359))

def Position(Agent):
    Agent.pose = [random.randint(1,9),random.randint(1,9)]

class Agent:
    def __init__(self, name, state, goal, angle, pose):
        self.name = name
        self.state = state      #tourque (#s, high med low)
        self.goal = goal      #goal angle
        self.angle = angle      #current angle
        self.pose = pose        #current position (x,y)





