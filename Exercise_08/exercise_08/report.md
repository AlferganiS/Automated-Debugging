# Report

# functions that are terminating on all inputs:
## ex_1
```sh
 def ex_1(i: int):
 while i < 0:
    i = i + 1
```
The value of the variable "i" keeps incrementing by 1 until eventually reaching 0 and violating the condition "i < 0".
## ex_6
```sh
def ex_6(i: int):
    c = 0
    while i >= 0:
        j = 0
        while j <= i - 1:
            j = j + 1
            c = c + 1
        i = i - 1
```
The value of the variable "i" keeps decrementing by 1 until eventually reaching 0 and violating the condition of the first loop "i >= 0". On the other hand, the value of variable "j" is set to 0 and keeps incrementing by 1 until eventually reaching the value of "i - 1" which is set by the previous loop that it must be greater than or equal to zero. Thus, "j" will eventually break the second loop, and "i" will eventually break the first.
# functions that are not terminating:
## ex_2:
```sh
def ex_2(i: int):
    while i != 1 and i != 0:
        i = i - 2
```
A negative input to this function for instance, "-2" will result in an infinite loop of the variable "i" decrementing by 2 and never satisfying the condition of being equal to one or zero.
## The frequencies of each line collected by the debugger:
```sh
The value of i =  -2
  60   0%     def ex_2(i: int):
  61  50%         while i != 1 and i != 0:
  62  49%             i = i - 2
 ```
 ## ex_3:
```sh
def ex_3(i: int, j: int):
    while i != j:
        i = i - 1
        j = j + 1
```
If the value of the variable "i" (5) is less than the variable "j" (10), the loop will never end.
## The frequencies of each line collected by the debugger:
```sh
The value of i = 5, The value of j =  10
  64   0%     def ex_3(i: int, j: int):
  65  33%         while i != j:
  66  33%             i = i - 1
  67  33%             j = j + 1
```
## ex_4:
```sh
def ex_4(i: int):
    while i >= -5 and i <= 5:
        if i > 0:
            i = i - 1
        if i < 0:
            i = i + 1
```
The value of the variable "i" will increase or decrease unit it reaches zero and the loop will be infinite.
## The frequencies of each line collected by the debugger:
```sh
The value of i = 0
  69   0%     def ex_4(i: int):
  70  33%         while i >= -5 and i <= 5:
  71  33%             if i > 0:
  72   0%                 i = i - 1
  73  33%             if i < 0:
  74   0%                 i = i + 1
```
## ex_5:
```sh
def ex_5(i: int):
    while i < 10:
        j = i
        while j > 0:
            j = j + 1
        i = i + 1
```
The value of the variable "i"(-5) is incrementing by one until it equals 1. Setting the value of the variable "j" to one, and entering the second loop where "j" is incrementing by 1 and the loop is infinite.
## The frequencies of each line collected by the debugger:
```sh
The value of i =  -5
  76   0%     def ex_5(i: int):
  77   0%         while i < 10:
  78   0%             j = i
  79  49%             while j > 0:
  80  49%                 j = j + 1
  81   0%             i = i + 1
```





