from time import sleep
from dynamixel_sdk import * 


AGENTS = 36 


DEVICE0 = "COM3" # closest to screen (lower agent indexes)
DEVICE1 = "COM4" # furthest from screen (higher agent indexes)
BAUDRATE = 57600


#TORQUE CONTROL VALUES
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
ADDR_TORQUE_CONTROL = 64
LEN_TORQUE_ENABLE = 1 # bytes


#LOAD VALUES
ADDR_PRESENT_LOAD = 126


#Goal Position Values 
ADDR_GOAL_POSITION = 116
LEN_GOAL_POSITION = 4 # bytes


#Present Position Values  
ADDR_PRESENT_POSITION = 132 
LEN_PRESENT_POSITION = 4 # bytes


DXL_MINIMUM_POSITION_VALUE  = 695       
DXL_MAXIMUM_POSITION_VALUE  = 3405 


port0 = PortHandler(DEVICE0); port0.openPort(); port0.setBaudRate(BAUDRATE)
port1 = PortHandler(DEVICE1); port1.openPort(); port1.setBaudRate(BAUDRATE)

pack0 = Protocol2PacketHandler()
pack1 = Protocol2PacketHandler()

group0_read = GroupSyncRead(port0, pack0, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
group1_read = GroupSyncRead(port1, pack1, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

group0_write = GroupSyncWrite(port0, pack0, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
group1_write = GroupSyncWrite(port1, pack1, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)


def torque_control(state):

    for n in range(AGENTS):
        if n < 18:
            port_hand = port0; packet_hand = pack0
        else:
            port_hand = port1; packet_hand = pack1

        comm_result, error_result = packet_hand.write1ByteTxRx(port_hand, n, ADDR_TORQUE_CONTROL, state)
        print( "Agent " + str(n) + " " + packet_hand.getTxRxResult(comm_result) + "Torque control: " + str(state))

        if error_result != 0:
            print( "Agent" + str(n) + " " + packet_hand.getRxPacketError(error_result))


def collect_positions():
    """
    Collects the current positions of the dynamixels and returns them in a list 

    Parameters:
        None
    Returns:
        None
    """
    for n in range(AGENTS):
        if n < 18:
            group0_read.removeParam(n)
            group0_read.addParam(n)
        else:
            group1_read.removeParam(n)
            group1_read.addParam(n)

    group0_read.txRxPacket()
    group1_read.txRxPacket()

    positions = []
    for n in range(AGENTS):
        if n < 18:
            positions.append( group0_read.getData(n, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION) )
        else:
            positions.append( group1_read.getData(n, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION) )
            
    return positions  


def set_positions(proposed_shape):
    """
    Sets the dynamixels to a proposed shape

    Parameters:
        proposed_shape - a list of positions that the dynamixels will go to 
    Returns:
        None
    """

    # present_position_sum = 0
    # present_shape = collect_positions()
    # for pos in range(len(present_shape)):
    #     present_position_sum += present_shape[pos]

    # proposed_position_sum = 0
    # for position in range(len(proposed_shape)):
    #     proposed_position_sum += proposed_shape[position]

    # if len(proposed_shape) != AGENTS:
    #     print("The proposed shape has too many positions!")
    #     return

    # if abs(present_position_sum - proposed_position_sum) > 36:
    #     print(str(present_position_sum))
    #     print(str(proposed_position_sum))
    #     print("The sum of the positions is too high!")
    #     return
    proposed_shape_param = [] 
    for pos in proposed_shape:
        proposed_shape_param.append( [DXL_LOBYTE(DXL_LOWORD(pos)), DXL_HIBYTE(DXL_LOWORD(pos)), DXL_LOBYTE(DXL_HIWORD(pos)), DXL_HIBYTE(DXL_HIWORD(pos))] )

    for n in range(AGENTS):
        if n < 18:
            group0_write.removeParam(n)
            group0_write.addParam(n, (proposed_shape_param[n]))
        else:
            group1_write.removeParam(n)
            group1_write.addParam(n, (proposed_shape_param[n]))

    group0_write.txPacket()
    group1_write.txPacket()


def create_shape_list_param(shape_name):
    """
    Loads a shape from a csv file and returns a list of position parameters for that shape 

    Parameters:
        saved_shape - shape saved in a csv file that will be loaded
    Returns:
        None
    """
    returned_shape = [] 
    # print("Loading shape: Loopy_" + str(shape_name) + ".csv" )
    loaded_shape = open( "Loopy_Shapes/Loopy_" + str(shape_name) + ".csv", "r")
   
    for id in range(AGENTS):
        current_line = loaded_shape.readline().split(",")
        position = int(current_line[1])
        param_position = [DXL_LOBYTE(DXL_LOWORD(position)), DXL_HIBYTE(DXL_LOWORD(position)), DXL_LOBYTE(DXL_HIWORD(position)), DXL_HIBYTE(DXL_HIWORD(position))]
        returned_shape.append( param_position )

    loaded_shape.close()
    # print("Loaded shape: Loopy_" + str(shape_name) + ".csv" )
    return returned_shape

def create_shape_list(shape_name):
    """
    Loads a shape from a csv file and returns a list of position parameters for that shape 

    Parameters:
        saved_shape - shape saved in a csv file that will be loaded
    Returns:
        None
    """
    returned_shape = [] 
    # print("Loading shape: Loopy_" + str(shape_name) + ".csv" )
    loaded_shape = open( "New_Loopy/Loopy_Shapes/Loopy_" + str(shape_name) + ".csv", "r")
   
    for id in range(AGENTS):
        current_line = loaded_shape.readline().split(",")
        position = int(current_line[1])
        returned_shape.append(position)

    loaded_shape.close()
    # print("Loaded shape: Loopy_" + str(shape_name) + ".csv" )
    return returned_shape


def save_current_shape(shape_name):
    """
    Stores the current shape of Loopy in a csv file   

    Parameters:
        shape_name - the name of the shape you are trying to store 
    Returns:
        None
    """
    print("Creating shape: Loopy_" + str(shape_name) + ".csv" )
    new_file = open( "Loopy_Shapes/Loopy_" + str(shape_name) + ".csv", "w")
    shape = collect_positions()

    for n in range(AGENTS):
        new_file.write( "agent" + str(n) + "," + str(shape[n]) + "\n")

    new_file.close()
    print("Created shape: Loopy_" + str(shape_name) + ".csv" )


supported_shapes = ["Circle", "Square", "Triangle"]
supported_shapes_with_letters = ["A","Among_Us","B","C","Circle","D","E","F","G","H","Heart","I","J","K","L","N","Q","R","S","Square","T","Triangle","U","V","W","Y"]
wvu = ['W','V','U']
nate = ['N','A','T','E']


def shape_selector():
    """
    Prompts the user for a supported shape and creates it on loopy

    Parameters:
        None
    Returns:
        None
    """
    while True:
    
        shape = input("Enter a shape name " + str(supported_shapes_with_letters) + " : \n")

        try:
            torque_control(TORQUE_ENABLE)
            set_positions(create_shape_list_param(shape))
            sleep(1)
            torque_control(TORQUE_DISABLE)
            exit()
        except FileNotFoundError:
            print("This is not a supported shape. Please enter a new shape")
            torque_control(TORQUE_DISABLE)

        
def shape_rotator(shape_list):
    """
    Prompts the user for a supported shape and creates it on loopy

    Parameters:
        None
    Returns:
        None
    """
    while True:
        
        torque_control(TORQUE_ENABLE)

        for shapes in shape_list:
            set_positions(create_shape_list_param(shapes))
            sleep(1)

        torque_control(TORQUE_DISABLE)

        if exit() == True:
            break 


def mass_shape_saving():
    """
    Allows for a user to create new shapes saved in the "Loopy_Shapes" folder

    Parameters:
        None
    Returns:
        None
    """
    while True:
        torque_control(TORQUE_DISABLE)
        letter = input("What character would you like to save? \n")
        save_current_shape( letter )


def exit():
    """
    Creates a simple exit prompt that returns True or False 

    Parameters:
        None
    Returns:
        True - want to exit
        False - do not want to exit 
    """
    chosen = input("Would you like to exit? Y/N \n")
    if chosen.upper() == "Y":
        print("Exiting current menu")
        return True
    elif chosen.upper() == "N":
        return False
    else:
        print("Please select a valid response")
        exit()



# mass_shape_saving()
# shape_selector()
# shape_rotator(supported_shapes)

 

# class InvalidPositionSumError(Exception):

#     def __init__(self, proposed_sum ):
#         self.proposed_position_sum = proposed_sum
#         self.message = "The sum of the positions is invalid"

#     def __str__(self):
#         return f"{self.proposed_position_sum} -- {self.message}"

# class InvalidPositionCountError(Exception):

#     def __init__(self, proposed_count):
#         self.proposed_position_count = proposed_count
#         self.message = "The number of positions is invalid!"

#     def __str__(self):
#         return f"{self.proposed_position_count} -- {self.message}"



"""
Future controls for loopy

using average consensus for slower movements and 

may need to include current and time in addition to position values 


"""
 





