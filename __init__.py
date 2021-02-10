from state import State
from menu import CLI
import sys

from prompt_toolkit import prompt
from prompt_toolkit.application.current import get_app
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding import KeyBindings

if __name__ == '__main__':

    if len(sys.argv) == 2:
        state = State(sys.argv[1].upper())
    else:
        state = State("B")

    menu = CLI(state)
    menu.cli_cycle()