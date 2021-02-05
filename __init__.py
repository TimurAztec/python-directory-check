import sys
import os
import curses

screen = curses.initscr()
curses.start_color()

if sys.argv[1]:
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

screen.clear()
with os.scandir() as dir_entries:
    files = []
    sizes = []
    sumSize = 0
    for dir_entry, name in zip(dir_entries, os.listdir()):
        if division > 0:
            size = dir_entry.stat().st_size / division
        else:
            size = dir_entry.stat().st_size
        sumSize += size
        sizes.append(size)
        files.append({'size': size, 'name': name})
    minSize = min(sizes)
    maxSize = max(sizes)
    avgSize = sumSize / len(files)
    screen.addstr("Files in directory: \n", curses.A_BOLD)
    for item in files:
        screen.addstr("    {}".format(item.get('name', 'Some file')) + (" " * (20 - len(item['name']))))
        if item.get('size') < avgSize:
            screen.addstr("| {} {}".format(item.get('size', 'can`t get size'), divisionType)+"\n", curses.A_DIM)
        elif item.get('size') > avgSize:
            screen.addstr("| {} {}".format(item.get('size', 'can`t get size'), divisionType)+"\n", curses.A_BOLD)
        elif item.get('size') > (maxSize - avgSize):
            screen.addstr("| {} {}".format(item.get('size', 'can`t get size'), divisionType) + "\n", curses.A_STANDOUT)
        else:
            screen.addstr("| {} {}".format(item.get('size', 'can`t get size'), divisionType) + "\n")
    screen.addstr("Total: {} {}".format(sumSize, divisionType), curses.A_BOLD)

c = screen.getch()
curses.endwin()
