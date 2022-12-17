""" Global variables for the project. """

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
