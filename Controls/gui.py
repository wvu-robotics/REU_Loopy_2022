# import random 
import tkinter as tk

from matplotlib.pyplot import title
import PlotFrame 
import math
# import cmath
import Loopy


NUMBER_OF_AGENTS = 36
LOAD_WARNING_THRESHOLD = 700 # 70%


loopy = Loopy.Loopy(NUMBER_OF_AGENTS)
loopy.torque_off_all_agents()


window = tk.Tk()
window.title = "Loopy GUI"
window.geometry = "1080x600"
window.configure(bg="light blue")

CurrentAngleList = [0]
def UpdateCurrentAngleList():
    for i in loopy.agents:
        CurrentAngleList.append(i.get_present_position() * 360 / 4096 )
UpdateCurrentAngleList()

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


PlotsFrame = PlotFrame.PlotFrame(window, points_from_angles(CurrentAngleList).__getitem__(0),points_from_angles(CurrentAngleList).__getitem__(1))


##agent status lights/angles
    ##read Agent State
def AgentTorque(i):
    if loopy.agents[i].get_present_load() == 0:
        return 'off'
    elif abs(loopy.agents[i].get_present_load()) < LOAD_WARNING_THRESHOLD:
        return 'good'
    else:
        return 'high'

# Display Agent Status 'Lights'
def UpdateLights():
    for i in range(36):
        light_canvas = tk.Canvas(window, width=30, height=30, background='light blue', highlightthickness=0)
        my_oval = light_canvas.create_oval(13, 13, 26, 26)  # Create a circle on the Canvas
        # lights on/off
        if AgentTorque(i) == 'good':
            light_canvas.itemconfig(my_oval, fill='light green')
        elif AgentTorque(i) == 'off':
            light_canvas.itemconfig(my_oval, fill='light grey')
        elif AgentTorque(i) == 'high':
            light_canvas.itemconfig(my_oval, fill='red')
        light_canvas.grid(column=i, row=26)
UpdateLights()

##Create light number labels
for i in range(36):
    my_NumberLabel = tk.Label(window, text=str(i), background='light blue')
    my_NumberLabel.grid(column=i, row=27)

 ##Display Agent Torque Labels
def UpdateTorqueLabels():
    for i in range(36):
        TorqueLabel = tk.Label(window, text=str(loopy.agents[i].get_present_load()).zfill(3), background='light blue',borderwidth=3, relief='groove')
        TorqueLabel.grid(column=i, row=29)
UpdateTorqueLabels()

##Display Goal Angles
def UpdateGoalAngles():
    for i in range(36):
        g = loopy.agents[i].desired_angle
        my_GoalLabel = tk.Label(window, text=str(g).zfill(3), background='light blue', borderwidth=3,
                                relief='groove')
        my_GoalLabel.grid(column=i, row=32)
UpdateGoalAngles()

##Display Current Angles
def UpdateCurrentAngles():
    for i in range(36):
        a = loopy.agents[i].get_present_position() * 360 / 4096
        my_AngleLabel = tk.Label(window, text=str(int(a)).zfill(3), background='light blue', borderwidth=3, relief='groove')
        my_AngleLabel.grid(column=i, row=34)
UpdateCurrentAngles()

#Row Labels:
    ##label: 'Current Angle'
CurrentAngleLabel = tk.Label(window, text='Current Angle:', background='light blue')
CurrentAngleLabel.grid(columnspan=3, row=33)
    ##label: 'Goal Angle'
GoalAngleLabel = tk.Label(window, text='Goal Angle:', background='light blue')
GoalAngleLabel.grid(columnspan=3, row=30)
    ##label: 'Agent Torque'
TorqueLabel = tk.Label(window, text='Agent Torque:', background='light blue')
TorqueLabel.grid(columnspan=3, row=28)

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
    PlotsFrame.UpdateGoalPlot( LetterClicked.get())
ControlBtn= tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=6, height=1, text='Control', command=control)
ControlBtn.grid(row=2, column=0, columnspan=4)

##Reboot Button
def reboot():
    loopy.torque_on_all_agents()
    UpdateTorqueLabels()
    UpdateLights()
RebootBtn= tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=6, height=1, text='Reboot', command=reboot)
RebootBtn.grid(row=2, column=2, columnspan=4)

##Flexible Mode Button
'''
Loopy must be in flexible mode to recieve physical human input (to allow human to move it, changing the measurable load)
'''
FlexibleBtn = tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=6, height=1, text='Go Flexible', command=loopy.torque_off_all_agents)
FlexibleBtn.grid(row=3, column=2, columnspan=4)

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
    UpdateGoalAngles()
    AngleChosen.set(0)
    AgentClicked.set(0)
    showAgent()
    showAngle()
SetButton = tk.Button(window,text="Set Goal Angle", activebackground='navy blue', bg='#4863A0', fg='white', disabledforeground='#4863A0', command= SetAngleToAgent)
SetButton.grid(column=24, row=4, columnspan=4, pady=10)


######Ave Consensus
        ##L shape
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
        LetterList = LetterListL
    elif LetterClicked.get() == 'O':
        LetterList = LetterListO

    #make an initial error list for each of 36 goals for each of 36 agents
    def error(CirList):
        curr_node = CirList.head
        while curr_node.next:
           curr_node.data.ErrorList = []
           for j in LetterList:
               error = abs(curr_node.data.angle - j)
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
            curr_node.data.goal = LetterList.__getitem__(my_orientation)
            curr_node = curr_node.next
            if curr_node == CirList.head:
                break
        UpdateGoalAngles()
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
        if (curr_node.data.angle-curr_node.data.goal) <= -8:
            curr_node.data.angle = curr_node.data.angle + 8 ##needs to also write to servo to actually move
        elif (curr_node.data.angle-curr_node.data.goal) >= 8:
            curr_node.data.angle = curr_node.data.angle - 8 ##needs to also write to servo to move
        else:
            curr_node.data.angle = curr_node.data.angle - (curr_node.data.angle - curr_node.data.goal) ##needs to also write to servo to move
        curr_node = curr_node.next
        if curr_node == CircularAgentList.head:
            break
    UpdateCurrentAngles()
    UpdateCurrentAngleList()
    # PlotsFrame.canvas.delete()
    PlotsFrame2 = PlotFrame.PlotFrame(window, points_from_angles(CurrentAngleList).__getitem__(0),
                                     points_from_angles(CurrentAngleList).__getitem__(1))


MoveBtn = tk.Button(window,activebackground='navy blue', bg='#4863A0', fg='white', width=6, height=1, text='Move',command=LoopyMove)
MoveBtn.grid(row=4, column=0, columnspan=4)



window.after(100, UpdateCurrentAngles)
window.after( 100, UpdateTorqueLabels)
#######
window.mainloop()


