from globals import *

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
    global commands

    if command_name in commands:
        eval(commands[command_name])
    elif command_name in macros:
        runMacro(command_name, line)
    else:
        errorWithLine("Invalid command", line, index)
