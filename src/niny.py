#!/usr/bin/python3
import sys
sys.setrecursionlimit(10 ** 8)

""" All functions for checking stack conditions """
import methods as meths

""" Global variables for the project. """
from globals import *

commands = {
    # Basic commands for working with stack
    "full": meths.full, # @params: index
    "push": meths.push, # @params: line, index
    "dump": meths.dump, # @params: line, index
    "dup": meths.duplicateItemInStack, # @params: line, index
    "pop": meths.popFromStack, # @params: line, index
    "swp": meths.swapElsInStack, # @params: line, index
    "change": meths.changePlaces, # @params: line, index
    "rev": meths.reverseStack, # @params: index
    "len": meths.stackLength,
    "memory": meths.changeStack, # @params: line, index

    # Arithmetic commands
    "add": meths.arithmeticAddition, # @params: line, index
    "sub": meths.arithmeticSubstraction, # @params: line, index
    "mult": meths.arithmeticMultiplication, # @params: line, index
    "div": meths.arithmeticDivision, # @params: line, index
    "pow": meths.arithmeticExponentiation, # @params: line, index
    "root": meths.arithmeticRoot, # @params: line, index
    "divmod": meths.arithmeticRemainderDivision, # @params: line, index

    # Logic commands
    "if": meths.logicIf, # @params: line, index
    "or": meths.logicOr, # @params: line, index
    "and": meths.logicAnd, # @params: line, index
    "not": meths.logicNot, # @params: line, index
    "==": meths.logicEquals, # @params: line, index
    '<': meths.logicGreaterThan, # @params: line, index
    '>': meths.logicLessThan, # @params: line, index

    # Typecasting commands
    "type": meths.getType, # @params: line, index
    "int": meths.typecastToInt, # @params: index
    "bool": meths.typecastToBool, # @params: line, index
    "float": meths.typecastToFloat, # @params: line, index
    "string": meths.typecastToString, # @params: line, index
    "list": meths.typecastToList, # @params: line, index

    # Commands for working with arrays
    "append": meths.appendTo, # @params: line, index
    "insert": meths.insertTo, # @params: line, index
    "id": meths.getIndex, # @params: line, index
    "flat": meths.flatList, # @params: line, index

    # Other commands
    "inp": meths.getInput,
    "get": meths.getItem, # @params: line, index

    # Commands for operations with macros
    "macro": meths.createMacro, # @params: line, index
    "del": meths.deleteMacro, # @params: line, index
}

flags = {
    "-d": "debugMode()",
    "--debug": "debugMode()",
    "-ndms": "ignoreDebugMessages()",
    "--ignoredebugmsgs": "ignoreDebugMessages()",
}

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


# Basic functions
def checkStack(length, line, index):
    """ Basic function for checking amount of items in stack """
    global stacks
    global current_stack

    if len(stacks[current_stack]) < length:
        errorWithLine("Not enough elements in stack", line, index)
        exit()


def ignoreComments(line):
    return line if '$' not in line else line[:line.index('$')]


def errorWithLine(message, line, index):
    """ Basic function for throwing errors """
    print(message)
    print(f"Line {index + 1}\n-> ", end='')
    print(line, end='')

    exit()

def runMacro(name, line):
    global debug
    global macros, document

    if debug:
        print(f"Running macro {name}")

    if name not in macros:
        errorWithLine("Undefined macro", line, index)

    start_index, stop_index = macros[name]

    while start_index <= stop_index:
        m_line = ignoreComments(document[start_index])

        if len(m_line.strip()) != 0:
            execLine(m_line, start_index)

        start_index += 1

    if debug:
        full(index)

def execLine(line, index):
    """ Main line computing func """
    command_name = line.strip().split(' ')[0]  # Getting main command through extra spaces

    global debug

    if command_name in commands:
        commands[command_name](line, index, debug)
    elif command_name in macros:
        runMacro(command_name, line)
    else:
        errorWithLine("Invalid command", line, index)


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
