import string

from debuggingbook.DynamicInvariants import InvariantAnnotator, INVARIANT_PROPERTIES
import random

def mystery(x, y):
    if len(y) > 0:
        return x * y
    else:
        raise ValueError('len(y) <= 0')
        

def test_mystery():
    mystery(1, 'test')
    mystery(-1, 'test')

def get_random_string(length: int):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

INVARIANT_PROPERTIES += ['len(Y) > 0', 'isinstance(Y,str)']

def run() -> InvariantAnnotator:
    with InvariantAnnotator(INVARIANT_PROPERTIES) as t:
        test_mystery()
    return t


if __name__ == '__main__':
    print(run().function_with_invariants('mystery'))
