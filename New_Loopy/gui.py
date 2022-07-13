from time import sleep
import tkinter as tk
from threading import Thread
import Loopy
import Experimental.dataSender as dataSender
import numpy as np


AVE_CONSENSUS_ITERATIONS = 500
NUMBER_OF_AGENTS = 36
LOAD_WARNING_THRESHOLD = 700 # 70%
UPDATE_LABELS_TIME = 100 # ms 

ROW_CIRCLE = 26

loopy = Loopy.Loopy(NUMBER_OF_AGENTS)


window = tk.Tk()
###window.title doesnt work, needs to be configure or something
window.title = "Loopy GUI"
window.geometry = "1080x350"
window.configure(bg="light blue")

'''
Below: rows of lights, agent numbers, agent load, current angle, & goal angle are made & shown
'''

# Display Agent Status 'Lights'
def update_lights():
    for i in range(36):
        light_canvas = tk.Canvas(window, width=30, height=30, background='light blue', highlightthickness=0)
        my_oval = light_canvas.create_oval(13, 13, 26, 26)  # Create a circle on the Canvas
        
        if loopy.agents[i].torque_on_off == True:
            light_canvas.itemconfig(my_oval, fill='light green')

        elif loopy.agents[i].torque_on_off == False:
            light_canvas.itemconfig(my_oval, fill='light grey')

        light_canvas.grid(column=i, row=ROW_CIRCLE)

update_lights()

##Create light number labels
for i in range(36):
    my_NumberLabel = tk.Label(window, text=str(i), background='light blue')
    my_NumberLabel.grid(column=i, row= ROW_CIRCLE + 1 )

## agent load labels
load_labels = []
def create_load_labels():
    for i in range(loopy.agent_count):
        load_labels.append(tk.Label(window, text=str(loopy.agents[i].get_present_load()).zfill(3), background='light blue',borderwidth=3, relief='groove'))
        load_labels[i].grid(column=i, row= ROW_CIRCLE + 3)
        
def update_load_labels():
    print("Updating Load")
    for i in range(loopy.agent_count):
        a = loopy.agents[i].get_present_load()/10
        if a < 1 :
            a = 1
        elif a > 999:
            a = 999
        else:
            a = int(a)
        load_labels[i].config(text=str(a).zfill(3), background='light blue',borderwidth=3, relief='groove')
        # load_labels[i].config(window, text=str(loopy.agents[i].get_present_load()).zfill(3), background='light blue',borderwidth=3, relief='groove')

##agent goal labels
goal_angles_labels = [] 
def create_goal_angle_labels():
    for i in range(loopy.agent_count):
        goal_angles_labels.append(tk.Label(window, text=str(loopy.agents[i].desired_angle).zfill(3), background='light blue', borderwidth=3, relief='groove'))
        goal_angles_labels[i].grid(column=i, row= ROW_CIRCLE + 5)

def update_goal_angle_labels():
    print("Updating Goal Angles")
    for i in range(loopy.agent_count):
        goal_angles_labels[i].config(text=str(loopy.agents[i].desired_angle).zfill(3), background='light blue', borderwidth=3, relief='groove')
        #goal_angles_labels[i].config(tk.Label(window, text=str(loopy.agents[i].desired_angle).zfill(3), background='light blue', borderwidth=3, relief='groove'))

##agent current angle labels
current_angle_labels = [] 
def create_current_angle_labels():
    for i in range(loopy.agent_count):
        current_angle_labels.append(tk.Label(window, text=str(loopy.agents[i].get_present_angle()).zfill(3), background='light blue',borderwidth=3, relief='groove'))
        current_angle_labels[i].grid(column=i, row= ROW_CIRCLE + 7)

def update_current_angle_labels():
    print("Updating Current Angles")
    for i in range(loopy.agent_count):
        current_angle_labels[i].config(text=str(loopy.agents[i].get_present_angle()).zfill(3), background='light blue',borderwidth=3, relief='groove')
        # current_angle_labels[i].config(tk.Label(window, text=str(loopy.agents[i].get_present_angle()).zfill(3), background='light blue',borderwidth=3, relief='groove'))

##Text above label rows
TorqueLabel = tk.Label(window, text='Agent Load:', background='light blue')
TorqueLabel.grid(columnspan=3, row= ROW_CIRCLE + 2 )

GoalAngleLabel = tk.Label(window, text='Goal Angle:', background='light blue')
GoalAngleLabel.grid(columnspan=3, row= ROW_CIRCLE + 4)

CurrentAngleLabel = tk.Label(window, text='Current Angle:', background='light blue')
CurrentAngleLabel.grid(columnspan=3, row= ROW_CIRCLE + 6)


######Ave Consensus
       
def AveCon():

    current_shape = dataSender.collect_positions()

    chosen_shape = LetterClicked.get()

    #LetterList = dataSender.create_shape_list(chosen_shape)
    LetterList = [2064,2030,2091,2851,2139,2839,2118,2080,2053,1186,1974,2080,943,1903,1967,2055,2047,2003,2063,1969,2070,1967,995,1941,2036,2041,2029,2042,2074,2080,1959,1958,878,2040,2063,1170]



    ###below is for matrix:

    # make an initial error list for each of 36 goals for each of 36 agents
    def errorM():
        # agents error lists are error for each orientation (where their goal for orientation i is (i + id))
        for agent in loopy.agents:
            agent.ErrorList = []
            for i in range(len(LetterList)): # i is orientation, j is goal for that orientation
                j = i+agent.id
                if j > 35:
                    error = abs(current_shape[agent.id] - LetterList[j-36])
                else:
                    error = abs(current_shape[agent.id] - LetterList[j])
                agent.ErrorList.append(error)
    errorM()

    ##make matrix of each agent' error list (each error list is a row): (36 agents x 36 orientations)
    agents = loopy.agents
    A = np.array([[agents[0].ErrorList],[agents[1].ErrorList],[agents[2].ErrorList],[agents[3].ErrorList],[agents[4].ErrorList],
                [agents[5].ErrorList],[agents[6].ErrorList],[agents[7].ErrorList],[agents[8].ErrorList],[agents[9].ErrorList],
                [agents[10].ErrorList],[agents[11].ErrorList],[agents[12].ErrorList],[agents[13].ErrorList],[agents[14].ErrorList],
                [agents[15].ErrorList],[agents[16].ErrorList],[agents[17].ErrorList],[agents[18].ErrorList],[agents[19].ErrorList],
                [agents[20].ErrorList],[agents[21].ErrorList],[agents[22].ErrorList],[agents[23].ErrorList],[agents[24].ErrorList],
                [agents[25].ErrorList],[agents[26].ErrorList],[agents[27].ErrorList],[agents[28].ErrorList],[agents[29].ErrorList],
                [agents[30].ErrorList],[agents[31].ErrorList],[agents[32].ErrorList],[agents[33].ErrorList],[agents[34].ErrorList],
                [agents[35].ErrorList]], dtype=int)


    # average the agent's error list values
    #for each agent (each row), average with rows above/below (shifted by +/- 1) !!!!PROBLEM!!!
    def average():
        for i in range(len(A)):
            if i == 0:
                prevRow = A[-1 ].tolist()
                currRow = A[i ].tolist()
                nextRow = A[i + 1 ].tolist()
            elif i == 35:
                prevRow = A[i - 1 ].tolist()
                currRow = A[i ].tolist()
                nextRow = A[0 ].tolist()
            else:
                prevRow  = A[i-1].tolist()
                currRow = A[i].tolist()
                nextRow = A[i+1].tolist()
            #print(str(currRow))
            temp = np.array([prevRow, currRow, nextRow], dtype=int)
            temp = temp.sum(axis=0)
            temp = temp/3
            A[i] = temp


    for i in range(500):
        average()
    print("consensus has been reached")

#print/ assign chosen orientation for each agent
    for i in range(loopy.agent_count):
        row = A[i].tolist()
        Ochoice = row[0].index(np.amin(row))
        print('agent ' + str(i) + 's goal is ' + str((Ochoice)))
        goal = Ochoice + agents[i].id
        if goal > 35:
            goal = goal - 36
        agents[i].desired_angle = LetterList[goal]


'''non matrix ave con:

    #make an initial error list for each of 36 goals for each of 36 agents
    def error():
        for agent in loopy.agents:
            agent.ErrorList = []
            for j in LetterList:
                    error = abs(current_shape[agent.id] - j)
                    agent.ErrorList.append(error)
    error()

    #average the agent's error list values
    def LocalAveError(CirList):
        curr_node = CirList.head
        while curr_node.next:
            print("Calculating average local error for: " + curr_node.next.data.name)
            for j in curr_node.next.data.ErrorList:
                my_error_index = curr_node.next.data.ErrorList.index(j)
                if my_error_index == 0:
                    average = (curr_node.data.ErrorList[35] + curr_node.next.data.ErrorList[my_error_index] +
                               curr_node.next.next.data.ErrorList[my_error_index + 1]) / 3
                elif my_error_index == 35:
                    average = (curr_node.data.ErrorList[my_error_index - 1] + curr_node.next.data.ErrorList[my_error_index] +
                               curr_node.next.next.data.ErrorList[0]) / 3
                elif my_error_index >0 and my_error_index <35:
                    average = (curr_node.data.ErrorList[my_error_index-1] + curr_node.next.data.ErrorList[my_error_index] + curr_node.next.next.data.ErrorList[my_error_index+1]) / 3
                curr_node.next.data.ErrorList[my_error_index] = average
            curr_node = curr_node.next
            if curr_node == CirList.head:
                break


    for i in range(AVE_CONSENSUS_ITERATIONS):
        LocalAveError(CircularAgentList)
    print("\nconsensus has been reached\n")


    def AssignOrientation(CirList): # assign chosen orientation to all agents
        curr_node = CirList.head
        while curr_node.next:
            print("Assinging an orientation for: " + curr_node.next.data.name)
            index = curr_node.data.name
            my_orientation = curr_node.data.ErrorList.index(min(curr_node.data.ErrorList))
            #print (str(index) + 'goal orient' + str(my_orientation))
            curr_node.data.desired_angle = LetterList[my_orientation]
            curr_node = curr_node.next
            if curr_node == CirList.head:
                break
    AssignOrientation(CircularAgentList)
'''    
    
# ###Economic Consensus
# def agentErrorSums(agent):
#     # returns errorList of sums (of len3 error lists' abs)
#     agentSumList = []
#     for list in agent.errorList:
#         agentSumList.append(sum(map(abs, list)))
#     return agentSumList

def GoalAngles():
    GoalAngles  = []
    for agent in loopy.agents:
        print("adding goal positions to a list")
        GoalAngles.append(agent.desired_angle)
    print("returning the new goal list")
    return GoalAngles

# ''' new version for bulk read/write'''
# def EconConsensus(LetterList, AnglesList):
# ## LetterList = list of angles; CirList = circular list of agents; Current Angles list = bulk read list
# ##calulate error list(of lists) for neighborhood of agent.next
#     #first assign each angle to the corresponding agent in order to utilize the circular list
#     for agent in AgentList:
#         agent.angle = AnglesList[AgentList.index(agent)]

#     #then find error for each neighborhood(neighborhhod of nextAgent) for each orientation
#     curr_node = CircularAgentList.head
#     while curr_node.next:
#         agent = curr_node.data
#         nextAgent = curr_node.next.data
#         nextnextAgent = curr_node.next.next.data
#         nextAgent.errorList = []
#         for i in range(len(LetterList)):
#             leftError = agent.angle - LetterList(i-1)
#             selfError = nextAgent.angle - LetterList(i)
#             rightError = nextnextAgent.angle - LetterList(i+1)
#             CurrentErrorList = [leftError, selfError, rightError]
#             nextAgent.errorList.append(CurrentErrorList)

#         curr_node = curr_node.next
#         if curr_node == CircularAgentList.head:
#             break

#         #now assign movements based on these errors
#         curr_node = CircularAgentList.head
#         while curr_node.next:
#             agent = curr_node.data
#             nextAgent = curr_node.next.data
#             NeighborhoodIndex = AgentList.index(nextAgent)
#             nextnextAgent = curr_node.next.next.data
#             NeighborhoodBeliefsList = [min(agentErrorSums(agent)),min(agentErrorSums(nextAgent)),min(agentErrorSums(nextnextAgent))]
#             MiddleMoveStep = nextAgent.errorList[agentErrorSums(nextAgent).index(min(agentErrorSums(nextAgent)))][1]  # the error of middle agent w/ belief
#             if NeighborhoodBeliefsList.index(max(NeighborhoodBeliefsList)) == 1:
#                 pass #no movement this timestep if middle agent has most error (let it be moved by other neighborhoods)
#             elif MiddleMoveStep == 0:
#                 #move neighbor with least error with your belief to goal and other neighbor +/-
#                 MiddleBelief = nextAgent.errorList[agentErrorSums(nextAgent).index(min(agentErrorSums(nextAgent)))]
#                 if max(MiddleBelief) == 0:
#                     MoveStep = nextAgent.errorList[agentErrorSums(nextAgent).index(min(agentErrorSums(nextAgent)))][2]
#                     agent.desired_angle = agent.get_present_angle + MoveStep
#                     nextnextAgent.desired_angle = nextnextAgent.get_present_angle - MoveStep
#                 elif max(MiddleBelief) == 2:
#                     MoveStep = nextAgent.errorList[agentErrorSums(nextAgent).index(min(agentErrorSums(nextAgent)))][0]
#                     agent.desired_angle = agent.get_present_angle - MoveStep
#                     nextnextAgent.desired_angle = nextnextAgent.get_present_angle + MoveStep
#             else:
#                 #middle agent moves to belief angle, neighbor with belief with most error moves opposite                
#                 nextAgent.desired_angle = nextAgent.get_present_angle - MiddleMoveStep
#                 if NeighborhoodBeliefsList.index(max(NeighborhoodBeliefsList)) == 0:
#                     agent.desired_angle = agent.get_present_angle + MiddleMoveStep
#                 elif NeighborhoodBeliefsList.index(max(NeighborhoodBeliefsList)) == 2:
#                     nextnextAgent.desired_angle = nextnextAgent.get_present_angle + MiddleMoveStep
#                 curr_node = curr_node.next
#                 return GoalAngles()
#                 ##remove below 2 lines to run continuously, porbably should also add a delay
#             if curr_node == CircularAgentList.head:
#                     break
##

###Circular List###
class Node(object):
    def __init__(self, data = None, next = None ):
        self.data = data
        self.next = next
    def set_next(self, new_next):
        self.next = new_next

class CircularList(object):
    def __init__(self, head = None, tail = None):
        self.head = head
        self.tail = tail

    def traverse(self):
        curr_node = self.head
        while curr_node.next:
            print(curr_node.data.name)
            curr_node = curr_node.next
            if curr_node == self.head:
                break

    def insert_end(self, data):
        new_node = Node(data)
        if self.head == None:
            self.head = new_node
            self.head.next = new_node
            self.tail = new_node
            return
        else:
            self.tail.next = new_node
            new_node.next = self.head
            self.tail = new_node
            return

CircularAgentList = CircularList()
for agent in loopy.agents:
    CircularAgentList.insert_end(agent)

    

#######


# def update_labels():

#     create_load_labels()
#     create_goal_angle_labels()
#     create_current_angle_labels()

#     while True:
#         update_load_labels()
#         update_goal_angle_labels()
#         update_current_angle_labels()
#         sleep(.2)


'''
Below: the buttons in the top half of the gui are made & 'gridded'/ shown
'''
###Save Shape Buttons Group (left)

def store_shape():
    loopy.store_current_shape("L")

SaveShapeBtn = tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=10, height=1, text='Store Shape',command=store_shape)
SaveShapeBtn.grid(column = 2, row = 1, columnspan=4)

ShapeNameLabel= tk.Label(text = 'Enter Shape Name:', background = 'light blue')
ShapeNameLabel.grid(column=0, row=0, columnspan=4)

ShapeChosen = tk.StringVar()   
ShapeNameEntry = tk.Entry(window, textvariable=ShapeChosen, width=5)
ShapeNameEntry.grid(column = 4, row = 0, columnspan=1)


###Consensus Buttons group (middle)

ControlBtn= tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=6, height=1, text='Control', command=AveCon)
ControlBtn.grid(column = 12, row = 1, columnspan=4)

ChooseShapeLabel = tk.Label(window, text = 'Choose Shape:', background= 'light blue')
ChooseShapeLabel.grid(column=10, row=0, columnspan=4)

LetterOptions = dataSender.supported_shapes_with_letters
LetterClicked = tk.StringVar()
LetterClicked.set(dataSender.supported_shapes_with_letters[0])
LetterDrop = tk.OptionMenu(window, LetterClicked, *LetterOptions)
LetterDrop.grid(column = 14, row = 0, columnspan=4)


# new Loopy move for bulk write:

def LoopyMove():
    # try:
        dataSender.torque_control(dataSender.TORQUE_ENABLE)
        sleep(1)
        dataSender.set_positions(GoalAngles()) 
        sleep(2)
        dataSender.torque_control(dataSender.TORQUE_DISABLE)
    # except Exception:
    #     LoopyMove()




# ## Old Loopy Move:
# def LoopyMove():
#     curr_node = CircularAgentList.head
#     while curr_node.next:
#         present_angle = curr_node.data.get_present_angle()
#         if (present_angle - int(curr_node.data.desired_angle)) <= -16:
#             present_angle += 16
#         elif (present_angle - int(curr_node.data.desired_angle)) >= 16:
#             present_angle -= 16
#         else:
#             present_angle -= present_angle - int(curr_node.data.desired_angle)
#         curr_node.data.set_goal_angle(present_angle)
#         curr_node = curr_node.next
#         if curr_node == CircularAgentList.head:
#             break
# 

MoveBtn = tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=6, height=1, text='Move',command=LoopyMove)
MoveBtn.grid(row=2, column=12, columnspan=4)


###Manual Control Buttons Group (right)
    #agent selection
AgentOptions = range(36)
        # datatype of menu text
AgentClicked = tk.IntVar()
        # initial menu text
AgentClicked.set(0)
        # Create Dropdown menu
AgentDrop = tk.OptionMenu(window, AgentClicked, *AgentOptions)
AgentDrop.grid(column=25, row=0, columnspan=2)
        
    #angle selection
AngleChosen = tk.IntVar()
    # initial menu text
AngleChosen.set(0)
    # Create Text Entry
AngleEntry = tk.Entry(window, textvariable=AngleChosen, width=5)
AngleEntry.grid(column=25, row=1, columnspan=2)
    # Create button, it will change label text

    #Set Angle to Agent
def SetAngleToAgent():
    loopy.agents[AgentClicked.get()].desired_angle = AngleChosen.get()
    loopy.agents[AgentClicked.get()].set_goal_angle(AngleChosen.get())
    AngleChosen.set(0)
    AgentClicked.set(0)   
SetButton = tk.Button(window,text="Set Goal Angle", activebackground='navy blue', bg='#4863A0', fg='white', disabledforeground='#4863A0', command= SetAngleToAgent)
SetButton.grid(column=24, row=2, columnspan=4, pady=10)


###Torque Buttons Group (bottom middle)

def torque_off():
    loopy.torque_off_all_agents()
    update_lights()
def torque_on():
    loopy.torque_on_all_agents()
    update_lights()

torque_on_btn= tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=8, height=1, text='Torque On')
torque_on_btn.grid(column=10, row=5, columnspan=4)

torque_off_btn = tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=8, height=1, text='Torque Off')
torque_off_btn.grid(column = 14, row = 5, columnspan=4)

# update_labels_thread = Thread(target= update_labels)
# update_labels_thread.start()

# window.protocol( "WM_DELETE_WINDOW", loopy.torque_off_all_agents() )
window.mainloop()


