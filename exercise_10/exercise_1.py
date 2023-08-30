import datetime
from typing import List, Dict, Tuple

"""
1. **(1 Point)** Order the following list of information a developer requires to fix a bug in descending order by their importance according to the study of [Bettenburg et al, 2008](https://dl.acm.org/doi/10.1145/1453101.1453146):
    - Test Cases
    - Stack Traces
    - Observed Behavior
    - Hardware
    - Expected Behavior
    - Version
    - Operating System
    - Steps to Reproduce
"""


answer_1 = [
    "Steps to Reproduce",      
    "Stack Traces",      
    "Test Cases",      
    "Observed Behavior",      
    "Expected Behavior",      
    "Version",      
    "Operating System",      
    "Hardware"
]


"""
2. **(1 Point)** List **five** aspects that will help developers to *effectively* and *efficiently* process issue reports.
"""

answer_2 = [
    "Have a concise summary.",      
    "Be clear and concise.",      
    "Do not assume context.",      
    "Do not assume mistakes.",      
    "One issue per report." 
]


"""
3. **(1 Point)** Name a popular bug-tracking system.
"""

answer_3 = "Redmine"


"""
4. **(1 Point)** List **four** severities that describe the impact of a bug.
"""

answer_4 = [
    "Blocker ",
    "Major",
    "Trivial",
    "Critical"
]


"""
5. **(2 Points)** Write a bug report for the **middle** project in `middle/` by filling the dictionary fields of `answer_5`. You can find all information in the project.
"""

answer_5 = {
    "Project": "middle",
    "Subject": "The middle function occasionally returns the wrong value",
    "Description": """
        Tests:
        1. `middle(2, 1, 3)`
        2. `middle(3, 2, 4)`
        3. `middle(2, 2, 3)`
        
        Steps to reproduce:
        1. Import the `middle` function.
        2. Call the middle function with `x`, `y`, and `z`.
        3. `y <= x < z` must hold for these parameters.
        
        How to fix:
        Replace the return statement in line 6 `return y` with `return x`.
    """,
    "Status": "new",
    "Priority": "important",
    "Assignee": "Marius Smytzek",
    "Start date": datetime.datetime(2023, 2, 13),
    "Due date": datetime.datetime(2023, 2, 26)
}



"""
6. **(2 Points)** Report the **four** most changed files of [PySnooper](https://github.com/cool-RR/PySnooper) with the `ChangeCounter`.
"""

answer_6 = [
    [["pysnooper", "tracer.py"], 109],
    [["tests", "test_pysnooper.py"], 82],
    [["README.md"], 56],
    [["pysnooper", "__init__.py"], 50]
]


"""
7. **(1 Point)** Report all commit messages for the single most changed file of [PySnooper](https://github.com/cool-RR/PySnooper) with the `ChangeCounter`.
"""

answer_7 = [
    "Work feverishly",
    "Convert to single Python 2/3 codebase",
    "Add prefix feature",
    "Remove trailing whitespace",
    "Fix #14",
    "Add MAX_VARIABLE_LENGTH constant",
    "Add \"and collaborators\" everywhere",
    "When tracing 'call' events, skip lines containing decorators to print actual function",
    "Be safe and check that a function definition is found",
    "Rework code to find a function definition in case of decorated source lines",
    "Refactor detecting misplaced def lines",
    "python2 collections",
    "Refactor",
    "Show function return value. Resolves #32",
    "Refactor showing return values, repr, tests",
    "Remove any newlines from variables",
    "Canonicalize variable order #21",
    "Fail gracefully when can't find code",
    "Implement IPython code fetching",
    "Bundling decorator and six, look ma no dependencies!",
    "Remove need for conditional .decode() call which gives warning",
    "Argument to overwrite file #5",
    "Basic fixes for linters: remove unused variables and imports, plus whitespace and others",
    "Remove more calls to decode using u prefix",
    "Allow tracking arbitrary expressions in 'variables' using eval",
    "Massaging some code",
    "Use reprlib",
    "reprlib already handles both truncation and exceptions",
    "PR feedback: Swap imports, Raise maxother locally, Demo long variable output",
    "More informative repr for exceptions. Forgot to use repr_instance",
    "Fixes for Python 2",
    "IronPython doesn't always have frame.f_globals, fix #75",
    "Catch ValueError because IronPython raises it on bad filename #75",
    "Workaround for Unicode display on Py2.7, fix #67",
    "Add classes to automatically track attributes, keys, etc. of variables",
    "Add automatic exploded_variables",
    "Prefer dotted import",
    "Rename for coolness",
    "Make Tracer a class based decorator",
    "Allow using snoop as context manager",
    "Add back get_write_and_truncate_functions",
    "Improve checks for tracing, add tests for with blocks",
    "Optimisation: return None when not tracing frame to avoid line events",
    "Inline _should_trace_frame",
    "Document with block usage",
    "More reliable _is_internal_frame",
    "Cache source by both module name and filename. Fixes #101",
    "Keep proper track of previous tracing functions",
    "Add support for thread identifiers",
    "Delete frames when exiting to free up memory",
    "Remove decorator module, use functools.wraps",
    "Indent based on how many calls are currently being traced",
    "Store depth globally to indent correctly in all cases",
    "Log exceptions nicely",
    "Fix opcode lookup in Python 2",
    "Preserve the local variables order in the output.",
    "Make predictable order of items if we don't know the proper order.",
    "Simplify the new and modified values reporting.",
    "Restore cell vars support in the ordered printing.",
    "Rewrite get_local_reprs to use sort explicitly",
    "Make frame_to_local_reprs a dict",
    "Simplify parameters sorting",
    "Move one string of code down in get_local_reprs",
    "Don't always place new variables before the modified ones",
    "Join two lines in get_local_reprs",
    "Make vars_order line a bit shorter",
    "Move docstring to class",
    "Formatting",
    "Support generators",
    "Handle overwriting in FileWriter instead of Tracer",
    "Get rid from six module",
    "Move the type difference declaration to pycompat",
    "Fix unicode issues and add test, fix #124",
    "Add support for custom repr",
    "Changes according to review",
    "Support activate and deactivate snooper by environment variable and setup snooper globally",
    "Remove setup function and description",
    "Massaging some code",
    "Improve ensure_tuple",
    "Support single tuple to `custom_repr`, fix #144",
    "Show source path, especially when multiple files",
    "Fix bug with empty source",
    "Add support for wrapping classes",
    "Avoid snooping on the base class",
    "Use .items() to get rid of a call to getattr",
    "Bugfix: don't try to snoop on coroutines",
    "Reject coroutine functions and async generator functions #152",
    "Force time.isoformat to show microseconds every time, fix #158",
    "Add truncate option support",
    "Massaging some code",
    "Add normalize flag to remove machine-specific data",
    "Add total elapsed time",
    "Add relative_time format",
    "Add timedelta_isoformat",
    "Add depth case",
    "Rename relative_time to elapsed_time",
    "Enable multi-call",
    "Add indent of elapsed time",
    "Fixed elapsed_time",
    "Delete default value of timedelta_isoformat",
    "Refactor the timedelta_isoformat",
    "Fixed multi-thread case of elapsed_time",
    "Fixed timedelta_isoformat",
    "Massaging some code",
    "Add testing for exceptions",
    "Fix #195: Fix '_thread._local' object has no attribute 'depth' raised by snooper incompatibility",
    "Show colored output",
    "Add support for Ansible zipped source files",
    "Add support for Ansible zipped source files (#226)"
]




"""
8. **(1 Point)** Report the current size of the single most changed file of [PySnooper](https://github.com/cool-RR/PySnooper) with the `ChangeCounter`.
"""

answer_8 = 22709


print(len(answer_6), type(answer_6))
#### UTILS ####

if __name__ == '__main__':
    assert (
        isinstance(answer_1, List) 
        and len(answer_1) == 8 
        and all(isinstance(x, str) for x in answer_1)
    )
    assert (
        isinstance(answer_2, List) 
        and len(answer_2) == 5 
        and all(isinstance(x, str) for x in answer_2)
    )
    assert isinstance(answer_3, str)
    assert (
        isinstance(answer_4, List) 
        and len(answer_4) == 4
        and all(isinstance(x, str) for x in answer_4)
    )
    assert (
        isinstance(answer_5, Dict)
        and len(answer_5) == 8 
        and all(x in answer_5 for x in ["Project", "Subject", "Description", "Status", 
                                        "Priority", "Assignee", "Start date", "Due date"])
        and all(isinstance(x, str) or isinstance(x, datetime.datetime) for x in answer_5.values())
    )
    assert (
        isinstance(answer_6, List) 
        and len(answer_6) == 4
        and all(
            isinstance(x, Tuple) 
            and len(x) == 2 
            and isinstance(x[0], Tuple) 
            and all(isinstance(x, str) for x in x[0])
            and isinstance(x[1], int)
            for x in answer_6
        )
    )
    assert (
        isinstance(answer_7, List)   
        and all(isinstance(x, str) for x in answer_7)
    )
    assert isinstance(answer_8, int)
