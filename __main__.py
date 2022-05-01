from state import State
from menu import CLI
import sys

if __name__ == '__main__':

    if len(sys.argv) == 2:
        state = State(sys.argv[1].upper())
    else:
        state = State("B")

    menu = CLI(state)
    menu.cli_cycle()