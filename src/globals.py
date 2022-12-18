""" Global variables for the project. """

import methods as meths

global debug
debug = False

global ignoreDebugMessage
ignoreDebugMessage = True

global stacks
stacks = {"main": []}

global document
document = None

global macros
macros = {}  # Pattern - {"macro_name": (header_index, end_index)}

global current_stack
current_stack = "main"

global line_index
line_index = 0

global commands
commands = {
    # Basic commands for working with stack
    "full": "meths.full(index)",
    "push": "meths.push(line, index)",
    "dump": "meths.dump(line, index)",
    "dup": "meths.duplicateItemInStack(line, index)",
    "pop": "meths.popFromStack(line, index)",
    "swp": "meths.swapElsInStack(line, index)",
    "change": "meths.changePlaces(line, index)",
    "rev": "meths.reverseStack(index)",
    "len": "meths.stackLength()",
    "memory": "meths.changeStack(line, index)",

    # Arithmetic commands
    "add": "meths.arithmeticAddition(line, index)",
    "sub": "meths.arithmeticSubstraction(line, index)",
    "mult": "meths.arithmeticMultiplication(line, index)",
    "div": "meths.arithmeticDivision(line, index)",
    "pow": "meths.arithmeticExponentiation(line, index)",
    "root": "meths.arithmeticRoot(line, index)",
    "divmod": "meths.arithmeticRemainderDivision(line, index)",

    # Logic commands
    "if": "meths.logicIf(line, index)",
    "or": "meths.logicOr(line, index)",
    "and": "meths.logicAnd(line, index)",
    "not": "meths.logicNot(line, index)",
    "==": "meths.logicEquals(line, index)",
    '<': "meths.logicGreaterThan(line, index)",
    '>': "meths.logicLessThan(line, index)",

    # Typecasting commands
    "type": "meths.getType(line, index)",
    "int": "meths.typecastToInt(index)",
    "bool": "meths.typecastToBool(line, index)",
    "float": "meths.typecastToFloat(line, index)",
    "string": "meths.typecastToString(line, index)",
    "list": "meths.typecastToList(line, index)",

    # Commands for working with arrays
    "append": "meths.appendTo(line, index)",
    "insert": "meths.insertTo(line, index)",
    "id": "meths.getIndex(line, index)",
    "flat": "meths.flatList(line, index)",

    # Other commands
    "inp": "meths.getInput()",
    "get": "meths.getItem(line, index)",

    # Commands for operations with macros
    "macro": "meths.createMacro(line, index)",
    "del": "meths.deleteMacro(line, index)",
}

global flags
flags = {
    "-d": "debugMode()",
    "--debug": "debugMode()",
    "-ndms": "ignoreDebugMessages()",
    "--ignoredebugmsgs": "ignoreDebugMessages()",
}
