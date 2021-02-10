import os
from prompt_toolkit import *

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


def find_percent(value, findFrom):
    return (value / findFrom) * 100


def scan_current_directory(division, divisionType):
    try:
        os.system("cls")
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
        if len(sizes) <= 0:
            ex = ValueError()
            ex.strerror = "Folder is empty!"
            raise ex
        minsize = min(sizes)
        maxsize = max(sizes)
        avgsize = sumsize / len(files)

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
            percent = find_percent(size, maxsize)
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
    except ValueError as e:
        print_formatted_text(HTML("<ansired><b>{}</b></ansired>").format(e.strerror))
        os.chdir("..")
    except:
        print_formatted_text(HTML("<ansired><b>ERROR OCCURED!</b></ansired>"))
        prompt()
    finally:
        return files


def get_files_names(f):
    names = []
    for item in f:
        names.append(item['name'])
    return names


def get_folders(f):
    names = []
    for item in f:
        if os.path.isdir(item):
            names.append(item)
    return names
