#!/usr/bin/python3
import sys
sys.setrecursionlimit(10 ** 8)

""" All functions for checking stack conditions """
import methods as meths

""" Main project logic """
from globals import *
from utils import *

# Flags functions
def debugMode():
    """ Turning on the debug mode """
    global debug
    global ignoreDebugMessage

    if not ignoreDebugMessage:
        print("DEBUG MODE")
        print("FORMAT: line_number: stack_condition")

    debug = True

def flatten(array):
    result = []

    for item in array:
        if type(item) == list:
            result.extend(flatten(item))
        else:
            result.append(item)

    return result

def ignoreDebugMessages():
    global ignoreDebugMessage

    ignoreDebugMessage = True


def main(path):
    # Checking for the right file extension
    filename = path.split('/')[-1]
    if filename.split('.')[1] != "nn":
        print("Invalid file extension")
        usage()

    global document, stacks, macros  # Some basic structures
    global current_stack
    global line_index

    document = open(path).readlines()

    while line_index < len(document):
        line = ignoreComments(document[line_index])

        if len(line.strip()) != 0:
            execLine(line, line_index)

        line_index += 1

def usage():
    print("Usage: python3 niny.py [-d | --debug] [filename]")
    print("Some arguments:")
    print("-d, --debug\tTo turn on debug mode, after this you will see stack condition after almost each operation, that affects stack.")
    print("-ndms, --ignoredebugmsgs\tTo turn off the debug startup message.")

    exit()

if __name__ == "__main__":
    args = sys.argv
    args.pop(0)  # Removing python file

    global debug
    global ignoreDebugMessage

    # Going through the launch arguments
    index = 0

    while index < len(args):
        arg = args[index]
        if arg in flags:
            eval(flags[arg])

            args.pop(index)
            index -= 1

        index += 1

    if len(args) != 1:  # Must contain only name of file, but I think I will remove this dumb check in future
        print("Invalid flags")
        usage()

    main(args[0])

    exit()
