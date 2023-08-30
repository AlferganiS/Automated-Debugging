import ast
import random
import time
from types import FrameType, TracebackType
from typing import Any, Optional, Type
from debuggingbook.PerformanceDebugger import HitCollector, PerformanceDebugger

class HitCollector(HitCollector):
    def __init__(self, limit: int = 100000) -> None:
        super().__init__()
        self.limit = limit
 # YOUR CODE HERE

    def collect(self, frame: FrameType, event: str, arg: Any) -> None:
        super().collect(frame, event, arg)
        self.limit -= 1
        if self.limit == 0:
            raise OverflowError
# YOUR CODE HERE

# OTHER CODE if necessary

class PerformanceDebugger(PerformanceDebugger):
    def is_overflow(self) -> bool:
        if self.collector.limit == 0:
            return True
        else:
            return False
# YOUR CODE HERE

    def __exit__(self, exc_tp: Type, exc_value: BaseException, exc_traceback: TracebackType) -> Optional[bool]:
        if exc_tp == OverflowError:
            if exc_tp is None:
                outcome = self.PASS
            else:
                outcome = self.FAIL

            self.add_collector(outcome, self.collector)
            return True
        else:
            return super().__exit__(exc_tp, exc_value, exc_traceback)
# YOUR CODE HERE

# OTHER CODE if necessary
# random.seed(time.time())
# ran = random.randint(1, 999)
# ran2 = random.randint(1, 999)
if __name__ == '__main__':
    def loop(x: int):
        x = x + 1
        while x > 0:
            pass

    # def ex_1(i: int):
    #     while i < 0:
    #         i = i + 1

    # def ex_2(i: int):
    #     while i != 1 and i != 0:
    #         i = i - 2

    # def ex_3(i: int, j: int):
    #     while i != j:
    #         i = i - 1
    #         j = j + 1

    # def ex_4(i: int):
    #     while i >= -5 and i <= 5:
    #         if i > 0:
    #             i = i - 1
    #         if i < 0:
    #             i = i + 1

    # def ex_5(i: int):
    #     while i < 10:
    #         j = i
    #         while j > 0:
    #             j = j + 1
    #         i = i + 1

    # def ex_6(i: int):
    #     c = 0
    #     while i >= 0:
    #         j = 0
    #         while j <= i - 1:
    #             j = j + 1
    #             c = c + 1
    #         i = i - 1

    with PerformanceDebugger(HitCollector) as debugger:
        loop(1)
        # ex_1(ran)
        # ex_2(-2)
        # ex_3(5, 10)
        # ex_4(0)
        # ex_5(-5)
        # ex_6(ran)
    assert debugger.is_overflow()
    # print("The value of i = ", -2)
    print(debugger)
