import os
import inspect

PRINT_FORMAT = '{:<50}{}'
CORRECT_STATE = 'OK'
WRONG_STATE = 'NOT OK'

files_to_verify = [
    os.path.join('verify.py'),
    os.path.join('predicate.py'),
    os.path.join('exercise_1a.py'),
    os.path.join('exercise_1b.py'),
    os.path.join('exercise_1c.py'),
    # path to file
]

variables_to_verify = [
    ('predicate', 'Predicate'),
    ('exercise_1b', 'PredicateCollector'),
    ('exercise_1c', 'PredicateDebugger'),
    # tuple of (package, var name)
]

functions_to_verify = [
    # tuple of (package, function name, number of args)
    ('predicate', 'Predicate.__init__', 8),
    ('predicate', 'Predicate.__repr__', 1),
    ('predicate', 'Predicate.__str__', 1),
    ('predicate', 'Predicate.__hash__', 1),
    ('predicate', 'Predicate.__eq__', 2),
    ('exercise_1a', 'failure', 1),
    ('exercise_1a', 'context', 1),
    ('exercise_1a', 'increase', 1),
    ('exercise_1a', 'test_metrics', 0),
    ('exercise_1b', 'ackermann', 2),
    ('exercise_1b', 'PredicateCollector.__init__', 1),
    ('exercise_1b', 'PredicateCollector.collect', 4),
    ('exercise_1b', 'test_collection', 0),
    ('exercise_1c', 'PredicateDebugger.__init__', 2),
    ('exercise_1c', 'PredicateDebugger.all_predicates', 1),
    ('exercise_1c', 'test_debugger', 0),
]

def verify_files():
    missing_files = list()
    for path in files_to_verify:
        if os.path.exists(path):
            state = CORRECT_STATE
        else:
            missing_files.append(path)
            state = WRONG_STATE
        print(PRINT_FORMAT.format(path, state))
    print()
    return missing_files

def verify_variables():
    missing_variables = list()
    current_package = None
    for package, variable in variables_to_verify:
        if current_package is None or current_package.__name__ != package:
            current_package = __import__(package)
        varaible_repr = f'{package}.{variable}'
        if variable in dir(current_package):
            state = CORRECT_STATE
        else:
            missing_variables.append(varaible_repr)
            state = WRONG_STATE
        print(PRINT_FORMAT.format(varaible_repr, state))
    print()
    return missing_variables

def verify_functions():
    missing_functions = list()
    wrong_functions = list()
    current_package = None
    for package, function, args in functions_to_verify:
        if current_package is None or current_package.__name__ != package:
            current_package = __import__(package)
        fs = function.split('.')
        function_repr = f'{package}.{function}'
        if fs[0] in dir(current_package):
            f = getattr(current_package, fs[0])
            for i in fs[1:]:
                f = getattr(f, i)
            specs = inspect.getfullargspec(f)
            if len(specs[0]) == args:
                state = CORRECT_STATE
            else:
                wrong_functions.append(function_repr)
                state = WRONG_STATE
        else:
            missing_functions.append(function_repr)
            state = WRONG_STATE
        print(PRINT_FORMAT.format(function_repr, state))
    print()
    return missing_functions, wrong_functions

class VerificationError(ValueError):
    pass

if __name__ == '__main__':
    missing_files = verify_files()
    missing_variables = verify_variables()
    missing_functions, wrong_functions = verify_functions()
    for l, m in [(missing_files, 'Missing file'), (missing_variables, 'Missing variable'), 
                 (missing_functions, 'Missing functions'), (wrong_functions, 'Wrong function pattern')]:
        for v in l:
            print(f'{m}: {v}')
        if l:
            print()
    if missing_files or missing_variables:
        raise VerificationError()