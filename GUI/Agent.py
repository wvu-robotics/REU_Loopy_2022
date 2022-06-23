import random

def TourqeState(Agent):
    Agent.torque = int(random.randrange(-1,100))
    ## call Nate's function that reads in load, adjust to be out of 100
def GoalAngle(Agent):
    Agent.goal = int(random.randrange(0,359))

def CurrentAngle(Agent):
    Agent.angle = int(random.randrange(0,359))
    Loopy.agents
def Position(Agent):
    Agent.pose = [random.randint(1,9),random.randint(1,9)]


class Agent:
    def __init__(self, name, torque, goal, angle, pose):
        self.name = name
        self.torque = torque     #torque (#s, off good high)
        self.goal = goal      #goal angle
        self.angle = angle      #current angle
        self.pose = pose        #current position (x,y)
        #self.servo = servo     #assigns it to a physical servo/agent from Nate's Agent/Servo class


