# import random 
from time import sleep
import tkinter as tk
from threading import Thread
from matplotlib.pyplot import title
import PlotFrame 
import math
# import cmath
import Loopy

NUMBER_OF_AGENTS = 36
LOAD_WARNING_THRESHOLD = 700 # 70%
UPDATE_LABELS_TIME = 100 # ms 

ROW_CIRCLE = 26

loopy = Loopy.Loopy(NUMBER_OF_AGENTS)


window = tk.Tk()
window.title = "Loopy GUI"
window.geometry = "1080x600"
window.configure(bg="light blue")

CurrentAngleList = [0]
def update_current_angle_list():
    for i in loopy.agents:
        CurrentAngleList.append(i.get_present_position() * 360 / 4096 )
update_current_angle_list()

def points_from_angles(AngleList):
    #anglelist - list of angles
    #length - length of the line per point
    Xpoints = [0]
    Ypoints = [0]
    length = 5
    for angle in AngleList:
        index = AngleList.index(angle)
        nexty = Ypoints.__getitem__(index) + length * math.sin(math.radians(angle + AngleList.__getitem__(index-1)))
        nextx = length * math.cos(math.radians(angle + AngleList.__getitem__(index-1)))
        Xpoints.append(nextx)
        Ypoints.append(nexty)
    return [Xpoints, Ypoints]


PlotsFrame = PlotFrame.PlotFrame(window, points_from_angles(CurrentAngleList)[0], points_from_angles(CurrentAngleList)[0])

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


TorqueLabel = tk.Label(window, text='Agent Load:', background='light blue')
TorqueLabel.grid(columnspan=3, row= ROW_CIRCLE + 2 )


GoalAngleLabel = tk.Label(window, text='Goal Angle:', background='light blue')
GoalAngleLabel.grid(columnspan=3, row= ROW_CIRCLE + 4)


CurrentAngleLabel = tk.Label(window, text='Current Angle:', background='light blue')
CurrentAngleLabel.grid(columnspan=3, row= ROW_CIRCLE + 6)


##Button: Toggle Manual Agent Control/ Consensus Algorithm
ControlLabel = tk.Label(text='Manual', bg='light blue', fg='#4863A0', width=7, height=1, highlightthickness=2)
ControlLabel.grid(row=3, column=0, columnspan=4)


def control():
    if ControlLabel.config('text')[-1] == 'Manual':
        ControlLabel.config(text= 'Algorithm')
        SetButton['state'] = tk.DISABLED
        AveCon()
    else:
        ControlLabel.config(text= 'Manual')
        SetButton['state'] = tk.NORMAL
    # PlotsFrame.UpdateGoalPlot( LetterClicked.get())


ControlBtn= tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=6, height=1, text='Control', command=control)
ControlBtn.grid(row=2, column=0, columnspan=4)

def torque_off():
    loopy.torque_off_all_agents()
    update_lights()

##Reboot Button
def torque_on():
    loopy.torque_on_all_agents()
    update_lights()

torque_on_btn= tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=8, height=1, text='Torque On', command=torque_on)
torque_on_btn.grid(row=2, column=2, columnspan=4)

##Flexible Mode Button
'''
Loopy must be in flexible mode to recieve physical human input (to allow human to move it, changing the measurable load)
'''
torque_off_btn = tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=8, height=1, text='Go Flexible', command=torque_off)
torque_off_btn.grid(row=2, column=4, columnspan=4)

##Manual Control of Goal Angles
#Agent Dropdown Selection
        # Change the label text
def showAgent():
        SetAgentLabel.config(text=str(AgentClicked.get()))
        # Agent Dropdown menu options
AgentOptions = range(36)
        # datatype of menu text
AgentClicked = tk.IntVar()
        # initial menu text
AgentClicked.set(0)
        # Create Dropdown menu
AgentDrop = tk.OptionMenu(window, AgentClicked, *AgentOptions)
AgentDrop.grid(column=20, row=2, columnspan=2)
        # Create button, it will change label text
SetAgentbutton = tk.Button(window, text="Select Agent", disabledforeground='#4863A0', activebackground='navy blue', bg='#4863A0', fg='white',command=showAgent).grid(column=24, row=2, columnspan=4)
        # Create Label
SetAgentLabel = tk.Label(window, text=" ", background='light blue', relief='groove')
SetAgentLabel.grid(column=28, row=2, columnspan=4)

#Angle Selection
def showAngle():
    SetAngleLabel.config(text=str(AngleChosen.get()))
    # datatype of menu text
AngleChosen = tk.IntVar()
    # initial menu text
AngleChosen.set(0)
    # Create Text Entry
AngleEntry = tk.Entry(window, textvariable=AngleChosen, width=5)
AngleEntry.grid(column=20, row=3, columnspan=2)
    # Create button, it will change label text
SetAnglebutton = tk.Button(window, text="Select Angle",disabledforeground='#4863A0', activebackground='navy blue', bg='#4863A0', fg='white',command= showAngle).grid(column=24, row=3, columnspan=4)
    # Create Label
SetAngleLabel = tk.Label(window, text=" ", background='light blue', relief='groove')
SetAngleLabel.grid(column=28, row=3, columnspan=4)

#Set Angle to Agent
def SetAngleToAgent():
    loopy.agents[AgentClicked.get()].desired_angle = AngleChosen.get()
    loopy.agents[AgentClicked.get()].set_goal_angle(AngleChosen.get())
    AngleChosen.set(0)
    AgentClicked.set(0)
    showAgent()
    showAngle()
SetButton = tk.Button(window,text="Set Goal Angle", activebackground='navy blue', bg='#4863A0', fg='white', disabledforeground='#4863A0', command= SetAngleToAgent)
SetButton.grid(column=24, row=4, columnspan=4, pady=10)


######Ave Consensus
        ##L shape

def create_letter_l():
    LetterList_NewL = []
    loaded_shape = open("Loopy_Shapes/Loopy_" + str("L") + ".csv", "r")

    for id in range(loopy.agent_count):
        current_line = loaded_shape.readline().split(",")
        LetterList_NewL.append(int(int(current_line[1]) / 4096 * 360 ))

    return LetterList_NewL

LetterListL = [90,180,180,90,180,180,180,180,180,180,180,270,180,180,180,180,90,180,180,90,180,180,180,180,180,180,90,180,180,180,180,180,180,180,180,180]
        ##O shape
LetterListO = [170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170,170]

LetterOptions = ['L', 'O']
        # datatype of menu text
LetterClicked = tk.StringVar()
        # initial menu text
LetterClicked.set('L')
        # Create Dropdown menu
LetterDrop = tk.OptionMenu(window, LetterClicked, *LetterOptions)
LetterDrop.grid(column=4, row=3, columnspan=2)


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
##


##Move to Formation##
def LoopyMove():
    curr_node = CircularAgentList.head

    while curr_node.next:
        present_angle = curr_node.data.get_present_angle()

        if (present_angle - int(curr_node.data.desired_angle)) <= -16:
            present_angle += 16

        elif (present_angle - int(curr_node.data.desired_angle)) >= 16:
            present_angle -= 16

        else:
            present_angle -= present_angle - int(curr_node.data.desired_angle) ##needs to also write to servo to move

        curr_node.data.set_goal_angle(present_angle)

        curr_node = curr_node.next
        if curr_node == CircularAgentList.head:
            break
        
    
    # update_current_angle_list()
    # PlotsFrame.canvas.delete()
    # PlotsFrame2 = PlotFrame.PlotFrame(window, points_from_angles(CurrentAngleList)[0], points_from_angles(CurrentAngleList)[1])


def store_shape():
    loopy.store_current_shape("L")


MoveBtn = tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=6, height=1, text='Move',command=LoopyMove)
MoveBtn.grid(row=4, column=0, columnspan=4)


store_shape_btn = tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=10, height=1, text='Store Shape',command=store_shape)
store_shape_btn.grid(row= 4, column= 5, columnspan=4)


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


update_labels_thread = Thread(target= update_labels)
update_labels_thread.start()

window.protocol( "WM_DELETE_WINDOW", loopy.torque_off_all_agents() )
window.mainloop()


