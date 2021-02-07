import sys
import os
from prompt_toolkit import *
from prompt_toolkit.completion import NestedCompleter

if len(sys.argv) == 2:
    if sys.argv[1].upper() == "GB":
        divisionType = "Gb"
        division = 1000000000
    elif sys.argv[1].upper() == "MB":
        divisionType = "Mb"
        division = 1000000
    elif sys.argv[1].upper() == "KB":
        divisionType = "Kb"
        division = 1000
    elif sys.argv[1].upper() == "B":
        divisionType = "Bytes"
        division = 0
    else:
        divisionType = "Bytes"
        division = 0
else:
    divisionType = "Bytes"
    division = 0


def get_size(start_path='.'):
    total_size = 0
    dir_cout = 0
    files_count = 0
    if os.path.isfile(start_path):
        total_size = os.path.getsize(start_path)
    else:
        for dirpath, dirnames, filenames in os.walk(start_path):
            for d in dirnames:
                dir_cout += 1
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    files_count += 1
                    total_size += os.path.getsize(fp)

    return {'ts': total_size, 'ds': dir_cout, 'fs': files_count}


def findPercent(value, findFrom):
    return (value / findFrom) * 100


def scanCurDir():
    files = []
    sizes = []
    sumsize = 0
    for name in os.listdir():
        size = get_size(name)
        if division > 0:
            size['ts'] = size['ts'] / division
        sumsize += size['ts']
        sizes.append(size['ts'])
        files.append({'size': size, 'name': name})
    minsize = min(sizes)
    maxsize = max(sizes)
    avgsize = sumsize / len(files)

    os.system("cls")
    print_formatted_text(HTML("\n<b>Files in directory: \n</b>"))

    def printFileString(item, stringDec="label"):
        l_size = item['size']['ts']
        l_dirc = item['size']['ds']
        l_filec = item['size']['fs']
        ostr = "{} {}".format(round(l_size, 3), divisionType)
        print_formatted_text(HTML("<" + stringDec + ">" + ostr + (" " * (10 - len(ostr))) + "</" + stringDec + ">"),
                             end="")
        if l_dirc > 0 or l_filec > 0:
            print_formatted_text(" |", end="")
            if l_dirc > 0:
                print_formatted_text(HTML("<b> {} folders</b>".format(l_dirc)), end="")
            if l_filec > 0:
                print_formatted_text(HTML("<b> {} files</b>".format(l_filec)), end="")
            print_formatted_text(" are inside.", end="")
        print_formatted_text(" ")

    for item in files:
        size = item['size']['ts']
        percent = findPercent(size, maxsize)
        print_formatted_text(
            HTML("    {}".format(item.get('name', 'Some file')) + (" " * (20 - len(item['name']))) + "| "), end="")
        if percent > 90 or size == maxsize:
            printFileString(item, "ansired")
        elif percent > 75:
            printFileString(item, "ansiorange")
        elif percent > 50:
            printFileString(item, "ansiyellow")
        elif percent > 25:
            printFileString(item, "ansigreen")
        elif percent > 10:
            printFileString(item, "ansiwhite")
        else:
            printFileString(item)
    print_formatted_text(HTML("\n<b>Total: {} {}</b>".format(round(sumsize, 3), divisionType)))
    return files


def getFilesNames(f):
    names = []
    for item in f:
        names.append(item['name'])
    return names


def getFolders(f):
    names = []
    for item in f:
        if os.path.isdir(item):
            names.append(item)
    return names


if __name__ == '__main__':
    end = False
    session = PromptSession()
    while not end:
        files = getFilesNames(scanCurDir())
        folders = [".."] + getFolders(files)

        completer = NestedCompleter.from_nested_dict({
            'cd': {item: None for item in folders},
            'rm': {item: None for item in files},
            'exit': None,
        })

        input = session.prompt("> ", vi_mode=True, completer=completer,
                               bottom_toolbar=HTML("<italic>{}</italic>".format(os.getcwd()))).split(" ")
        if input[0]:
            if input[0] == "exit":
                end = True
            elif input[0] == "rm":
                if input[1]:
                    os.remove(input[1])
                else:
                    prompt("Wrong amount of arguments. Type 'rm <filename>'")
            elif input[0] == "cd":
                if input[1]:
                    if os.path.isdir(input[1]):
                        os.chdir(input[1])
                    else:
                        if os.path.isfile(input[1]):
                            prompt("This is file, you can`t go inside it!")
                        else:
                            prompt("Can`t find folder.")
                else:
                    prompt("Wrong amount of arguments. Type 'cd <foldername>'")
            else:
                os.system("".join(input))