import threading
from time import sleep, time
import tkinter as tk
import Loopy
import Experimental.data_handler as dataSender
import numpy as np
from scipy import signal

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


## agent load labels
load_labels = []
def create_load_labels():
    loads = dataSender.collect_loads()
    for i in range(loopy.agent_count):
        load_labels.append(tk.Label(window, text=str(loads[i]).zfill(3), background='light blue',borderwidth=3, relief='groove'))
        load_labels[i].grid(column=i, row= ROW_CIRCLE + 3)
        
def update_load_labels():
    print("Updating Load")
    loads = dataSender.collect_loads()
    for i in range(loopy.agent_count):
        a = loads[i]/10
        if a < 1 :
            a = 0
        elif a > 999:
            a = 999
        else:
            a = int(a)
        load_labels[i].config(text=str(a).zfill(3), background='light blue',borderwidth=3, relief='groove')


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


##agent current angle labels
current_angle_labels = [] 
def create_current_angle_labels():
    angles = dataSender.collect_positions()
    for i in range(loopy.agent_count):
        current_angle_labels.append(tk.Label(window, text=str(angles[i]).zfill(3), background='light blue',borderwidth=3, relief='groove'))
        current_angle_labels[i].grid(column=i, row= ROW_CIRCLE + 7)

def update_current_angle_labels():
    angles = dataSender.collect_positions()
    print("Updating Current Angles")
    for i in range(loopy.agent_count):
        current_angle_labels[i].config(text=str(angles[i]).zfill(3), background='light blue',borderwidth=3, relief='groove')


##Text above label rows
TorqueLabel = tk.Label(window, text='Agent Load:', background='light blue')
TorqueLabel.grid(columnspan=3, row= ROW_CIRCLE + 2 )

GoalAngleLabel = tk.Label(window, text='Goal Angle:', background='light blue')
GoalAngleLabel.grid(columnspan=3, row= ROW_CIRCLE + 4)

CurrentAngleLabel = tk.Label(window, text='Current Angle:', background='light blue')
CurrentAngleLabel.grid(columnspan=3, row= ROW_CIRCLE + 6)


def findOrientationArray(initErrorList):
        """    
        Returns a array corrisponding to the oriention based on consesus

        Parameters:
            goalList(List) - Desired list of angles to move to 
            currentList(List) - Current List of Angles that the agents are in
        Returns:
            OrientationArray - The ouput array to act on based on consesus
        """
        N = len(initErrorList)
        kernal = [[1, 0, 0],[0, 1, 0],[0, 0, 1]]
        errorList = [[[0 for j in range(N)] for j in range(N)] for n in range(3)]
        errorList[1] = initErrorList
        errorList[2] = signal.convolve2d(errorList[1],kernal,"same","wrap")
        for n in range(1,N//2): 
            errorList[0] = errorList[1]
            errorList[1] = errorList[2]
            errorList[2] = signal.convolve2d(errorList[1],kernal,"same","wrap") - np.add(errorList[1],errorList[0])
        if (N%2 == 0):
            errorList[2] -= np.subtract(errorList[2], errorList[1])//2
            
        return errorList[2]

######Ave Consensus
def AveCon():
   
    start_time = time()
    # current_shape = dataSender.read_from_address(dataSender.ADDR_PRESENT_POSITION, dataSender.LEN_PRESENT_POSITION)
    current_shape = dataSender.collect_positions()

    chosen_shape = LetterClicked.get()

    LetterList = dataSender.create_shape_list(chosen_shape)
    # # LetterList = [2064,2030,2091,2851,2139,2839,2118,2080,2053,1186,1974,2080,943,1903,1967,2055,2047,2003,2063,1969,2070,1967,995,1941,2036,2041,2029,2042,2074,2080,1959,1958,878,2040,2063,1170]


    #make an initial error list for each of 36 goals for each of 36 agents
    def error():
        for agent in loopy.agents:
            agent.ErrorList = []
            for j in LetterList:
                    error = abs(current_shape[agent.id] - j)
                    agent.ErrorList.append(error)
    error()

    # #average the agent's error list values
    # def LocalAveError(CirList):
    #     curr_node = CirList.head
    #     while curr_node.next:
    #         print("Calculating average local error for: " + curr_node.next.data.name)
    #         for j in curr_node.next.data.ErrorList:
    #             my_error_index = curr_node.next.data.ErrorList.index(j)
    #             if my_error_index == 0:
    #                 average = (curr_node.data.ErrorList[35] + curr_node.next.data.ErrorList[my_error_index] +
    #                            curr_node.next.next.data.ErrorList[my_error_index + 1]) / 3
    #             elif my_error_index == 35:
    #                 average = (curr_node.data.ErrorList[my_error_index - 1] + curr_node.next.data.ErrorList[my_error_index] +
    #                            curr_node.next.next.data.ErrorList[0]) / 3
    #             elif my_error_index >0 and my_error_index <35:
    #                 average = (curr_node.data.ErrorList[my_error_index-1] + curr_node.next.data.ErrorList[my_error_index] + curr_node.next.next.data.ErrorList[my_error_index+1]) / 3
    #             curr_node.next.data.ErrorList[my_error_index] = average
    #         curr_node = curr_node.next
    #         if curr_node == CirList.head:
    #             break


    # for i in range(AVE_CONSENSUS_ITERATIONS):
    #     LocalAveError(CircularAgentList)
    # print("\nconsensus has been reached\n")


    # def AssignOrientation(CirList): # assign chosen orientation to all agents
    #     curr_node = CirList.head
    #     while curr_node.next:
    #         print("Assinging an orientation for: " + curr_node.next.data.name)
    #         index = curr_node.data.name
    #         my_orientation = curr_node.data.ErrorList.index(min(curr_node.data.ErrorList))
    #         #print (str(index) + 'goal orient' + str(my_orientation))
    #         curr_node.data.desired_angle = LetterList[my_orientation]
    #         curr_node = curr_node.next
    #         if curr_node == CirList.head:
    #             break
    # AssignOrientation(CircularAgentList)


# matrix consensus:
###below is for matrix:

    # make an initial error list for each of 36 goals for each of 36 agents
    # def errorM():
    #     # agents error lists are error for each orientation (where their goal for orientation i is (i + id))
    #     for agent in loopy.agents:
    #         agent.ErrorList = []
    #         for i in range(len(LetterList)): # i is orientation, j is goal for that orientation
    #             j = i+agent.id
    #             if j > 35:
    #                 error = abs(current_shape[agent.id] - LetterList[j-36])
    #             else:
    #                 error = abs(current_shape[agent.id] - LetterList[j])
    #             agent.ErrorList.append(error)
    # errorM()

    ##make matrix of each agent' error list (each error list is a row): (36 agents x 36 orientations)
    agents = loopy.agents

    
    
    errorList =[[] for i in range(36)]
    for i in range(36):
        errorList[i] = agents[i].ErrorList
    A = findOrientationArray(errorList)


    # A = np.array([[agents[0].ErrorList],[agents[1].ErrorList],[agents[2].ErrorList],[agents[3].ErrorList],[agents[4].ErrorList],
    #             [agents[5].ErrorList],[agents[6].ErrorList],[agents[7].ErrorList],[agents[8].ErrorList],[agents[9].ErrorList],
    #             [agents[10].ErrorList],[agents[11].ErrorList],[agents[12].ErrorList],[agents[13].ErrorList],[agents[14].ErrorList],
    #             [agents[15].ErrorList],[agents[16].ErrorList],[agents[17].ErrorList],[agents[18].ErrorList],[agents[19].ErrorList],
    #             [agents[20].ErrorList],[agents[21].ErrorList],[agents[22].ErrorList],[agents[23].ErrorList],[agents[24].ErrorList],
    #             [agents[25].ErrorList],[agents[26].ErrorList],[agents[27].ErrorList],[agents[28].ErrorList],[agents[29].ErrorList],
    #             [agents[30].ErrorList],[agents[31].ErrorList],[agents[32].ErrorList],[agents[33].ErrorList],[agents[34].ErrorList],
    #             [agents[35].ErrorList]], dtype=int)
    # # average the agent's error list values
    # #for each agent (each row), average with rows above/below (shifted by +/- 1) !!!!PROBLEM!!!
    # def average():
    #     for i in range(len(A)):
    #         if i == 0:
    #             prevRow = A[-1 ].tolist()
    #             currRow = A[i ].tolist()
    #             nextRow = A[i + 1 ].tolist()
    #         elif i == 35:
    #             prevRow = A[i - 1 ].tolist()
    #             currRow = A[i ].tolist()
    #             nextRow = A[0 ].tolist()
    #         else:
    #             prevRow  = A[i-1].tolist()
    #             currRow = A[i].tolist()
    #             nextRow = A[i+1].tolist()
    #         #print(str(currRow))
    #         temp = np.array([prevRow, currRow, nextRow], dtype=int)
    #         temp = temp.sum(axis=0)
    #         temp = temp/3
    #         A[i] = temp
    

    # for i in range(500):
    #     average()
    # print("consensus has been reached")

#print/ assign chosen orientation for each agent
    for i in range(loopy.agent_count):
        row = A[i].tolist()
        Ochoice = row.index(np.amin(row))
        print( loopy.agents[i].name + " goal is " + str((Ochoice)) + " with position value: ")
        goal = Ochoice
        if goal > 35:
            goal = goal - 36
        agents[i].desired_angle = LetterList[goal]
        print( str(loopy.agents[i].desired_angle) + "\n")

    end_time = time()
    print("Alg time: \n")
    print(end_time - start_time)
    print(GoalAngles())
    print(A)
    #LoopyMove()


    
#returns list to be bulk written
def GoalAngles():
    GoalAngles  = []
    for agent in loopy.agents:
        print("adding goal positions to a list")
        GoalAngles.append(agent.desired_angle)
    print("returning the new goal list")

    return GoalAngles



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
Below: the buttons in the top half of the gui are made & 'gridded'(shown)
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

ControlBtn= tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white',width=20, height=1, text='Average Consensus', command=AveCon)
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
        # sleep(1)
        # dataSender.torque_control(dataSender.TORQUE_DISABLE)
    # except Exception:
    #     LoopyMove()

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
    #update_lights()
def torque_on():
    loopy.torque_on_all_agents()
    #update_lights()

torque_on_btn= tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=8, height=1, text='Torque On')
torque_on_btn.grid(column=10, row=5, columnspan=4)

torque_off_btn = tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=8, height=1, text='Torque Off')
torque_off_btn.grid(column = 14, row = 5, columnspan=4)

###
#update_labels_thread = threading.Thread(target= update_labels)
#update_labels_thread.start()

###
window.mainloop()


