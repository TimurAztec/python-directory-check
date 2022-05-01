from utils import *
from state import State
import os
import shutil
from prompt_toolkit import *
from prompt_toolkit.completion import NestedCompleter


def cd(input):
    input.pop(0)
    if input:
        input = " ".join(input)
        if os.path.isdir(input):
            os.chdir(input)
        else:
            if os.path.isfile(input):
                prompt("This is file, you can`t go inside it!")
            else:
                prompt("Can`t find folder.")
    else:
        prompt("Wrong amount of arguments. Type 'cd <foldername>'")


def remove(input):
    input.pop(0)
    if input:
        input = " ".join(input)
        if os.path.isdir(input):
            shutil.rmtree(input)
        else:
            if os.path.isfile(input):
                os.remove(input)
            else:
                prompt("Can`t find.")
    else:
        prompt("Wrong amount of arguments. Type 'rm <filename>'")


class CLI:

    def __init__(self, state):
        self.__end = False
        self.__session = PromptSession()
        self.state = state

    def __draw_file_sys(self):
        files = get_files_names(scan_current_directory(self.state.division_value, self.state.division_type))
        folders = [".."] + get_folders(files)
        return NestedCompleter.from_nested_dict({
            'goto': {item: None for item in folders},
            'remove': {item: None for item in files},
            'format': {
                'gb': None,
                'mb': None,
                'kb': None,
                'b': None,
            },
            'cd': {item: None for item in folders},
            'rm': {item: None for item in files},
            'exit': None,
        })

    def __change_format(self, input):
        input.pop(0)
        if input:
            self.state = State(input[0].upper())
        else:
            prompt("Wrong amount of arguments. Type 'format <datasizeformat>'")

    def cli_cycle(self):
        while not self.__end:
            completer = self.__draw_file_sys()

            input = self.__session.prompt("> ", vi_mode=True, completer=completer,
                                          bottom_toolbar=HTML(
                                              "<asciblack>{}</asciblack><asciorange>    [HELP] -> Use 'TAB' button to "
                                              "see available commands!</asciorange>".format(
                                                  os.getcwd())), mouse_support=True).split(" ")
            if input[0]:
                if input[0] == "exit":
                    self.__end = True
                elif input[0] == "rm" or input[0] == "remove":
                    remove(input)
                elif input[0] == "cd" or input[0] == "goto":
                    cd(input)
                elif input[0] == "format":
                    self.__change_format(input)
                else:
                    os.system(" ".join(input))
