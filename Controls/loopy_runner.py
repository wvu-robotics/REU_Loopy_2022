from re import T
from time import sleep
from Controls.Loopy import *

NUMBER_OF_AGENTS = 36


loopy = Loopy(NUMBER_OF_AGENTS)


def main():

    loopy.store_current_shape("testing")

    sleep(5)

    loopy.torque_on_all_agents()
    loopy.recreate_saved_shape("testing")
    loopy.torque_off_all_agents()


def reset():

    loopy.torque_off_all_agents()


main()