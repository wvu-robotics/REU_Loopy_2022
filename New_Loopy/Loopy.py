"""
2022 WVU REU

Human Interaction with Loopy

Author: Nathan Adkins
"""

from Agent import *

class Loopy:

    def __init__(self, number_of_agents):
        self.initialized = False
        self.agent_count = number_of_agents 
        self.agents = self.initialize_all_agents()
        self.current_shape = None


    def initialize_all_agents(self):
        """
        Initializes all of the agents for a Loopy instance (called in the constructor )   

        Parameters:
                None
        Returns:
                current_agents - list of instances of Agents created based on given id values 
        """
        current_agents = []
        print("Start making agents")
        for id in range(self.agent_count):
            current_agents.append(Agent(id))
        print("End making agents")
            

        self.initialized = True
        return current_agents


    def torque_off_all_agents(self):
        """
        Turns the torque on for all of the Agents in a Loopy   

        Parameters:
            None
        Returns:
            None
        """
        for id in range(self.agent_count):
            self.agents[id].torque_control("off")


    def torque_on_all_agents(self):
        """
        Turns the torque on for all of the Agents in a Loopy   

        Parameters:
            None
        Returns:
            None
        """
        for id in range(self.agent_count):
            self.agents[id].torque_control("on")

   
    def store_current_shape(self, shape_name ):
        """
        Stores the current shape of Loopy in a csv file   

        Parameters:
            shape_name - 
        Returns:
            None
        """
        print("Creating shape: Loopy_" + str(shape_name) + ".csv" )
        new_file = open( "Loopy_Shapes/Loopy_" + str(shape_name) + ".csv", "w")

        for id in range(self.agent_count):
            new_file.write( self.agents[id].name + "," + str(self.agents[id].get_present_position()) + "\n")

        new_file.close()
        print("Created shape: Loopy_" + str(shape_name) + ".csv" )


    def recreate_saved_shape(self, saved_shape):
        """
        Loads a saved shape from a csv file and Loopy recreates it

        Parameters:
            saved_shape - shape saved in a csv file that will be loaded
        Returns:
            None
        """
        print("Loading shape: Loopy_" + str(saved_shape) + ".csv" )
        loaded_shape = open( "Loopy_Shapes/Loopy_" + str(saved_shape) + ".csv", "r")
        
        for id in range(self.agent_count):
            current_line = loaded_shape.readline().split(",")
            self.agents[id].set_goal_position(int(current_line[1]))

        loaded_shape.close()
        print("Loaded shape: Loopy_" + str(saved_shape) + ".csv" )
        
        
    #change pid gains:
    
    def set_loopy_p_gain(self, gain):
        for agent in self.agents:
            agent.set_p_gain(gain)
        print('p gain is now: ' + str(gain))

    def set_loopy_i_gain(self, gain):
        for agent in self.agents:
            agent.set_i_gain(gain)
        print('i gain is now: ' + str(gain))

    def set_loopy_d_gain(self, gain):
        for agent in self.agents:
            agent.set_d_gain(gain)
        print('d gain is now: ' + str(gain))
