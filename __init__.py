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

    print(files_count, dir_cout)
    return {'ts': total_size, 'ds': dir_cout, 'fs': files_count}


def scanCurDir():
    files = []
    sizes = []
    sumsize = 0
    for name in os.listdir():
        size = get_size(name)
        if division > 0:
            size['ts'] = size['ts'] / division
        print(size)
        sumsize += size['ts']
        sizes.append(size['ts'])
        files.append({'size': size, 'name': name})
    minsize = min(sizes)
    maxsize = max(sizes)
    avgsize = sumsize / len(files)

    screen.clear()
    screen.addstr("Files in directory: \n", curses.A_BOLD)

    def printFileString(item, stringDec = curses.A_COLOR):
        l_size = item['size']['ts']
        l_dirc = item['size']['ds']
        l_filec = item['size']['fs']
        ostr = "{} {}".format(round(l_size, 3), divisionType)
        screen.addstr(ostr + (" " * (10 - len(ostr))), stringDec)
        if l_dirc > 0 or l_filec > 0:
            screen.addstr(" |")
            if l_dirc > 0:
                screen.addstr(" {} folders".format(l_dirc), curses.A_BOLD)
            if l_filec > 0:
                screen.addstr(" {} files".format(l_filec), curses.A_BOLD)
            screen.addstr(" are inside.")
        screen.addstr("\n")

    for item in files:
        size = item['size']['ts']
        screen.addstr("    {}".format(item.get('name', 'Some file')) + (" " * (20 - len(item['name']))) + "| ")
        if size < (avgsize - maxsize):
            printFileString(item, curses.A_DIM)
        elif size > (maxsize - (avgsize / 3)) or size == maxsize:
            printFileString(item, curses.A_STANDOUT)
        elif size > (avgsize + (avgsize / 3)):
            printFileString(item, curses.A_BLINK)
        elif size > avgsize or size > (avgsize - (avgsize / 3)):
            printFileString(item, curses.A_BOLD)
        else:
            printFileString(item)
    screen.addstr("Total: {} {}".format(round(sumsize, 3), divisionType), curses.A_BOLD)


scanCurDir()

c = screen.getch()
curses.endwin()
