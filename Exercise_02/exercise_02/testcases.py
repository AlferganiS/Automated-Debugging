# reference implementation
from idb import Debugger

# test function
from test import debug_main

# (test#id, commands before `quit`)
command_groups = [
    (1, ['break hi', 'delete hi']),
        # check points: both
    (2, ['break 4', 'break 10', 'break 14', 'delete 10']),
        # check points: the last two
    (3, ['step', 'step', 'step', 'assign @macro = 0', 'assign m = 0', 'step', 'print m']),
        # check points: assign @macro = 0, print m
    (4, ['step', 'step', 'assign m = 10', 'print m', 'step', 'print m']),
        # check points: assign m = 10, the last print m
    (5, ['where', 'step', 'step', 'step', 'where']),
        # check points: the two where
    (6, ['step', 'step', 'step', 'finish', 'step', 'finish']),
        # check points: the two finish
    (7, ['next', 'next', 'next', 'next']),
        # check points: the 2nd and 4th next
    (8, ['next', 'next', 'next', 'step', 'finish', 'step']),
        # check points: the last two
    (9, ['step', 'step', 'step', 'step', 'step', 'step', 'step', 'where', 'finish', 'where']),
        # check points: the two where
    (10, ['break 8', 'continue', 'where', 'continue', 'finish'])
        # check points: where, finish
]

# Run this to obtain the expected outputs of each testcase
if __name__ == '__main__':
    from debuggingbook.bookutils import next_inputs

    for group in command_groups:
        print(f'--- test#{group[0]} ---')
        next_inputs(group[1] + ['quit'])
        with Debugger():
            debug_main()

