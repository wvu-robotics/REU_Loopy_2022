import random

def TourqeState(Agent):
    Agent.state = int(random.randrange(-1,100)) ##change to actual range later - 0 low/off grey, 1 med/good green, 2 high/danger red
     ## call Nate's function that reads in load, adjust to be out of 100
def GoalAngle(Agent):
    Agent.goal = int(random.randrange(0,359))
    #set_goal_angle(servo, Agent.goal)
def CurrentAngle(Agent):
    Agent.angle = int(random.randrange(0,359))
    #Agent.angle = get_present_position(servo)*(3405/360)
def Position(Agent):
    Agent.pose = [random.randint(1,9),random.randint(1,9)]

class Agent:
    def __init__(self, name, torque, goal, angle, pose, servo):
        self.name = name
        self.torque = torque     #torque (#s, off good high)
        self.goal = goal      #goal angle
        self.angle = angle      #current angle
        self.pose = pose        #current position (x,y)
        self.servo = servo     #assigns it to a physical servo/agent from Nate's Agent/Servo class


