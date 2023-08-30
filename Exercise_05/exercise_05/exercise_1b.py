from debuggingbook.StatisticalDebugger import Collector
from types import FrameType
from typing import Any, Dict
import inspect

from predicate import Predicate

def ackermann(m, n):
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))


class PredicateCollector(Collector):
    
    def __init__(self) -> None:
        super().__init__()
        self.predicates: Dict[str, Predicate] = dict()

    def collect(self, frame: FrameType, event: str, arg: Any) -> None:
        if event == 'call':
            name = frame.f_code.co_name
            argvalues = inspect.getargvalues(frame)
            
            for arg_1 in argvalues.args:
                value_1 = argvalues.locals[arg_1]
                
                if isinstance(value_1, int) or isinstance(value_1, float):
                    # Add == 0, < 0, and > 0
                    for key, pred in (
                        (f'{name}({arg_1} == 0)', '__eq__'),
                        (f'{name}({arg_1} < 0)', '__lt__'),
                        (f'{name}({arg_1} > 0)', '__gt__')
                    ):
                        if key not in self.predicates:
                            self.predicates[key] = Predicate(key)
                            
                        if getattr(value_1, pred)(0):
                            self.predicates[key].true = 1
                        self.predicates[key].observed = 1
                        
                    for arg_2 in argvalues.args:
                        value_2 = argvalues.locals[arg_2]
                        
                        if arg_1 != arg_2 and (isinstance(value_2, int) or isinstance(value_2, float)):
                            for key, pred in (
                                (f'{name}({arg_1} == {arg_2})', '__eq__'),
                                (f'{name}({arg_1} < {arg_2})', '__lt__'),
                                (f'{name}({arg_1} > {arg_2})', '__gt__')
                            ):
                                if key not in self.predicates:
                                    self.predicates[key] = Predicate(key)
                                    
                                if getattr(value_1, pred)(value_2):
                                    self.predicates[key].true = 1
                                self.predicates[key].observed = 1



def test_collection():
    with PredicateCollector() as pc:
        ackermann(0, 1)
    results = {
        'ackermann(m == 0)': (1, 1),
        'ackermann(m < 0)': (0, 1),
        'ackermann(m > 0)': (0, 1),
        'ackermann(m < n)':  (1, 1),
        'ackermann(m > n)':  (0, 1),
        'ackermann(n == 0)': (0, 1),
        'ackermann(n < 0)': (0, 1),
        'ackermann(n > 0)': (1, 1),
        'ackermann(n < m)':  (0, 1),
        'ackermann(n > m)':  (1, 1),
        'ackermann(m == n)': (0, 1),
        'ackermann(n == m)': (0, 1),
    }
    for pred in results:
        pred = pc.predicates[pred]
        p, o = results[pred.rpr]
        assert pred.true == p, f'True for {pred} was wrong, expected {p}, was {pred.true}'
        assert pred.observed == o, f'Observed for {pred} was wrong, expected {o}, was {pred.observed}'
        assert pred.failing_observed == pred.successful_observed == pred.failing_true == pred.successful_true == 0


if __name__ == '__main__':
    test_collection()
    print('Successful')
