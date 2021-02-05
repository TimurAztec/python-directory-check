import sys
import os
import curses

screen = curses.initscr()
curses.start_color()

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
    if os.path.isfile(start_path):
        total_size = os.path.getsize(start_path)
    else:
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

    return total_size


screen.clear()
with os.scandir() as dir_entries:
    files = []
    sizes = []
    sumSize = 0
    for dir_entry, name in zip(dir_entries, os.listdir()):
        if division > 0:
            size = get_size(name) / division
        else:
            size = get_size(name)
        sumSize += size
        sizes.append(size)
        files.append({'size': size, 'name': name})
    minSize = min(sizes)
    maxSize = max(sizes)
    avgSize = sumSize / len(files)
    screen.addstr("Files in directory: \n", curses.A_BOLD)
    for item in files:
        screen.addstr("    {}".format(item.get('name', 'Some file')) + (" " * (20 - len(item['name']))) + "| ")
        if item.get('size') < (avgSize - maxSize):
            screen.addstr("{} {}".format(item.get('size', 'can`t get size'), divisionType) + "\n", curses.A_DIM)
        elif item.get('size') > (maxSize - (avgSize / 3)) or item.get('size') == maxSize:
            screen.addstr("{} {}".format(item.get('size', 'can`t get size'), divisionType) + "\n", curses.A_STANDOUT)
        elif item.get('size') > (avgSize + (avgSize / 3)):
            screen.addstr("{} {}".format(item.get('size', 'can`t get size'), divisionType) + "\n", curses.A_BLINK)
        elif item.get('size') > avgSize or item.get('size') > (avgSize - (avgSize / 3)):
            screen.addstr("{} {}".format(item.get('size', 'can`t get size'), divisionType) + "\n", curses.A_BOLD)
        else:
            screen.addstr("{} {}".format(item.get('size', 'can`t get size'), divisionType) + "\n")
    screen.addstr("Total: {} {}".format(sumSize, divisionType), curses.A_BOLD)

c = screen.getch()
curses.endwin()
