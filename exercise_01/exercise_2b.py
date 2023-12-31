level = 0

def increase_level():
    global level
    level += 1

    
def decrease_level():
    global level
    level -= 1
    
    
def log(s: str = ''):
    print(s)


def indent(s: str) -> str:
    return '  ' * level + s

    
# TODO: change this function
def fib(n: int) -> int:
    log(indent(f'call with n = {n}'))
    increase_level()

    if n == 0:    
        decrease_level()
        log(indent(f'return 0'))
        return 0
    
    if n == 1:
        decrease_level()
        log(indent(f'return 1'))
        return 1
    
    _tmp = fib(n - 1) + fib(n - 2)
    decrease_level()
    log(indent(f'return {_tmp}'))
    return _tmp 

# https://www.geeksforgeeks.org/python-program-for-merge-sort/
def merge(arr, l, m, r): # auxiliary function, do not trace
    n1 = m - l + 1
    n2 = r - m

    L = [0] * (n1)
    R = [0] * (n2)

    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


# TODO: change this function
def merge_sort(arr, l, r): # main function
    log(indent(f'call with arr = {arr}, l = {l}, r = {r}'))
    increase_level()
    if l < r:
        m = l + (r - l) // 2
        merge_sort(arr, l, m)    # <--- trace this
        merge_sort(arr, m + 1, r)  # <--- trace this
        merge(arr, l, m, r)         # <--- do not trace this!
    decrease_level()
    log(indent(f'return {arr}'))
    return arr


if __name__ == '__main__':
    fib(4)
    log()
    arr = [12, 11, 13, 5, 6, 7]
    merge_sort(arr, 0, len(arr) - 1)