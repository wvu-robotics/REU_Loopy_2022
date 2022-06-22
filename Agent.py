from dynamixel_sdk import *


BAUDRATE = 57600
DEVICE_NAME0 = "COM3" # Linux: /dev/ttyUSB*
DEVICE_NAME1 = "COM4" # Linux: /dev/ttyUSB*


port_handler0 = PortHandler(DEVICE_NAME0)
port_handler1 = PortHandler(DEVICE_NAME1)
packet_handler = Protocol2PacketHandler()


TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
ADDR_TORQUE_ENABLE = 64


ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132 
DXL_MINIMUM_POSITION_VALUE  = 695       
DXL_MAXIMUM_POSITION_VALUE  = 3405 


class Agent:


    def __init__(self, id):
        self.name = "agent" + str(id)
        self.id = id
        self.packet_handler = Protocol2PacketHandler()
        self.port_handler = self.get_port(); self.open_port()


    def __str__(self):
        """
        Overrides Python's print function for objects

        Parameters:
            None
        Returns:
            string - special print message for Agent class 
        """
        return "Name: " + self.name + " Present Position: " + str(self.get_present_position())


    def get_port(self):
        """
        Returns the port handler for an Agent based off of it's id number 

        Parameters:
            None
        Returns:
            port_handler - the port handler for the given device
        """
        if self.id >= 0 and self.id <= 17:
            return port_handler0
        elif self.id >= 18 and self.id <= 35:
            return port_handler1
        else:
            print("Error: invalid agent id")


    def open_port(self):
        """
        Opens the port for an Agent's dynamixel and sets the baudrate  

        Parameters:
            None
        Returns:
            True/False - True if the port was able to be opened, False otherwise
        """
        if self.port_handler.openPort() and self.port_handler.setBaudRate(BAUDRATE):
            print("Opened the USB Port \"" + self.port_handler.port_name + "\" and set the baudrate")
            return True
        else:  
            return False


    def close_port(self):
        """
        Closes the port for an Agent's dynamixel   

        Parameters:
            None
        Returns:
            True/False - True if the port was able to be closed, False otherwise
        """
        if self.port_handler.closePort:
            print("Closed the USB Port \"" + self.port_handler.port_name + "\"")
            return True
        else:  
            return False


    def set_goal_position( self, position ):
        """
        Sets the position of an Agent to a given goal position   

        Parameters:
            position - the goal position of the Agent's dynamixel
        Returns:
            None
        """
        print("Setting Goal Positon of " + self.name + " to " + str(position))
        packet_handler.write4ByteTxRx( self.port_handler, self.id, ADDR_GOAL_POSITION, position)


    def convert_to_position(self, goal_angle):
        """
        Converts the target angle (from degrees) to positions for the Agent's dynamixel   

        Parameters:
            goal_angle - the goal angle for the Agent
        Returns:
            goal_position - the goal position for the Agent after having been converted
        Notes:
            180 degrees is 2048 (flat)
            90 degrees is 1024
            (positions are measured by the dynamixels counterclockwise with left being position 0)
        """
        return float(int(goal_angle)) * DXL_MAXIMUM_POSITION_VALUE / float(int(360))


    def set_goal_angle( self, angle_in_degrees ):
        """
        Sets the angle of a given Agent to a given angle value in degrees    

        Parameters:
            angle_in_degrees - the goal angle for the dynamixel 
        Returns:
            None
        """
        print("Setting Goal Angle of " + self.name + " to " + str(angle_in_degrees))
        packet_handler.write4ByteTxRx( self.port_handler, self.id, ADDR_GOAL_POSITION, self.convert_to_position(angle_in_degrees))


    def torque_control(self, state):
        """
        Turns the torque on for an Agent when passed "on" and off then passed "off"   

        Parameters:
            state - selects on or off 
        Returns:
            None
        """
        if state == "on":
            print("Enabling Torque for: " + self.name)
            packet_handler.write1ByteTxRx( self.port_handler , self.id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
        elif state == "off":
            print("Disabling Torque for: " + self.name)
            packet_handler.write1ByteTxRx( self.port_handler, self.id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        else:
            print("Error: Invalid torque state!")


    def get_present_position(self):
        """
        Gets the position of an Agent's dynamixel   

        Parameters:
            None
        Returns:
            position value for an agent's dynamixel
        """
        recieved_packet = self.packet_handler.read2ByteTxRx(self.port_handler, self.id, ADDR_PRESENT_POSITION)
        return int(recieved_packet[0])








        



        
    
