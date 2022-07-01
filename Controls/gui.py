from time import sleep
import tkinter as tk
from threading import Thread
import Loopy
import random

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
       
def create_letter_l():
    LetterList_NewL = []
    loaded_shape = open("Loopy_Shapes/Loopy_" + str("L") + ".csv", "r")

    for id in range(loopy.agent_count):
        current_line = loaded_shape.readline().split(",")
        LetterList_NewL.append(int(int(current_line[1]) / 4096 * 360 ))

    return LetterList_NewL

        ##O shape
LetterListO = [170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170]

def AveCon():
    LetterList = []
    if LetterClicked.get() == 'L':
        LetterList = create_letter_l()
    elif LetterClicked.get() == 'O':
        LetterList = LetterListO

    #make an initial error list for each of 36 goals for each of 36 agents
    def error(CirList):
        curr_node = CirList.head
        while curr_node.next:
           curr_node.data.ErrorList = []
           for j in LetterList:
               error = abs(curr_node.data.get_present_angle() - j)
               curr_node.data.ErrorList.append(error)
           curr_node = curr_node.next
           if curr_node == CirList.head:
               break
    error(CircularAgentList)

    #average the agent's error list values
    def LocalAveError(CirList):
        curr_node = CirList.head
        while curr_node.next:
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


    for i in range(500):
        LocalAveError(CircularAgentList)


    def AssignOrientation(CirList): ##assign chosen orientation to all agents
        curr_node = CirList.head
        while curr_node.next:
            index = curr_node.data.name
            my_orientation = curr_node.data.ErrorList.index(min(curr_node.data.ErrorList))
            #print (str(index) + 'goal orient' + str(my_orientation))
            curr_node.data.desired_angle = LetterList.__getitem__(my_orientation)
            curr_node = curr_node.next
            if curr_node == CirList.head:
                break
    AssignOrientation(CircularAgentList)

###Economic Consensus
def agentErrorSums(agent):
    # returns errorList of sums (of len3 error lists' abs)
    agentSumList = []
    for list in agent.errorList:
        agentSumList.append(sum(map(abs, list)))
    return agentSumList

def EconConsensus(LetterList):
    ## LetterList = list of angles
##calulate error list(of lists) for neighborhood of agent.next
    curr_node = CircularAgentList.head
    while curr_node.next:
        agent = curr_node.data
        nextAgent = curr_node.next.data
        nextnextAgent = curr_node.next.next.data
        nextAgent.errorList = []
        for goal in LetterList:
            index = index(goal)
            leftError = agent.angle - LetterList(index-1)
            selfError = nextAgent.angle - LetterList(index)
            rightError = nextnextAgent.angle - LetterList(index+1)
            CurrentErrorList = [leftError, selfError, rightError]
            nextAgent.errorList.append(CurrentErrorList)
        curr_node = curr_node.next
        if curr_node == CircularAgentList.head:
            break
            
## assign movements
        curr_node = CircularAgentList.head
        while curr_node.next:
            agent = curr_node.data
            nextAgent = curr_node.next.data
            nextnextAgent = curr_node.next.next.data
            nextAgentBeliefIndex = agentErrorSums(nextAgent).index(min(agentErrorSums(nextAgent)))
            NeighborhoodBeliefsList = [min(agentErrorSums(agent)),min(agentErrorSums(nextAgent)),min(agentErrorSums(nextnextAgent))]
            if NeighborhoodBeliefsList.index(max(NeighborhoodBeliefsList)) == 1:
                pass #no movement this timestep if middle agent has most error (let it be moved by other neighborhoods)
            else:
                #middle agent moves to belief angle, neighbor with belief with most error moves opposite
                MoveStep = nextAgent.errorList[nextAgentBeliefIndex][1]
                nextAgent.set_goal_angle(nextAgent.get_present_angle + MoveStep)
                if NeighborhoodBeliefsList.index(max(NeighborhoodBeliefsList)) == 0:
                    agent.set_goal_angle(agent.get_present_angle - MoveStep)
                elif NeighborhoodBeliefsList.index(max(NeighborhoodBeliefsList)) == 2:
                    nextnextAgent.set_goal_angle(nextnextAgent.get_present_angle - MoveStep)
                curr_node = curr_node.next
                ##remove below 2 lines to run continuously, porbably should also add a delay
                if curr_node == CircularAgentList.head:
                    break
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


def update_labels():

    create_load_labels()
    create_goal_angle_labels()
    create_current_angle_labels()

    while True:
        update_load_labels()
        update_goal_angle_labels()
        update_current_angle_labels()
        sleep(.2)


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

LetterOptions = ['L', 'O']
LetterClicked = tk.StringVar()
LetterClicked.set('L')
LetterDrop = tk.OptionMenu(window, LetterClicked, *LetterOptions)
LetterDrop.grid(column = 14, row = 0, columnspan=4)

def LoopyMove():
    curr_node = CircularAgentList.head
    while curr_node.next:
        present_angle = curr_node.data.get_present_angle()
        if (present_angle - int(curr_node.data.desired_angle)) <= -16:
            present_angle += 16
        elif (present_angle - int(curr_node.data.desired_angle)) >= 16:
            present_angle -= 16
        else:
            present_angle -= present_angle - int(curr_node.data.desired_angle)
        curr_node.data.set_goal_angle(present_angle)
        curr_node = curr_node.next
        if curr_node == CircularAgentList.head:
            break
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

torque_on_btn= tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=8, height=1, text='Torque On', command=torque_on)
torque_on_btn.grid(column=10, row=5, columnspan=4)

torque_off_btn = tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=8, height=1, text='Torque Off', command=torque_off)
torque_off_btn.grid(column = 14, row = 5, columnspan=4)

update_labels_thread = Thread(target= update_labels)
update_labels_thread.start()

window.protocol( "WM_DELETE_WINDOW", loopy.torque_off_all_agents() )
window.mainloop()


