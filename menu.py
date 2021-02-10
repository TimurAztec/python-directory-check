from file_operations import *
import os
import shutil
from prompt_toolkit import *
from prompt_toolkit.completion import NestedCompleter


class CLI:

    def __init__(self, state):
        self.end = False
        self.session = PromptSession()
        self.state = state

    def cli_cycle(self):
        while not self.end:
            files = get_files_names(scan_current_directory(self.state.division_value, self.state.division_type))
            folders = [".."] + get_folders(files)

            completer = NestedCompleter.from_nested_dict({
                'cd': {item: None for item in folders},
                'rm': {item: None for item in files},
                'exit': None,
            })

            input = self.session.prompt("> ", vi_mode=True, completer=completer,
                                   bottom_toolbar=HTML(
                                       "<italic>{}</italic> <b><asciblack>[F1] Help</asciblack></b> <b><asciblack>[F2] Change Format</asciblack></b>".format(
                                           os.getcwd()))).split(" ")
            if input[0]:
                if input[0] == "exit":
                    end = True
                elif input[0] == "rm":
                    input.pop(0)
                    if input[0]:
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
                elif input[0] == "cd":
                    input.pop(0)
                    if input[0]:
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
                else:
                    os.system(" ".join(input))