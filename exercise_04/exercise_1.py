
import ast
from ast import FunctionDef, Name, NodeTransformer, Call, Return, arg, arguments, fix_missing_locations, parse, expr, stmt, unparse, AST
import inspect
from typing import Any, Callable

######## Test examples ########


def fib(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


# https://www.geeksforgeeks.org/python-program-for-merge-sort/


def merge(arr, l, m, r):  # auxiliary function, do not trace
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


def merge_sort(arr, l, r):  # main function
    if l < r:
        m = l + (r - l) // 2

        merge_sort(arr, l, m)  # <--- trace this
        merge_sort(arr, m + 1, r)  # <--- trace this
        merge(arr, l, m, r)  # <--- do not trace this!

    return arr


#############

def parse_expr(code: str) -> expr:
    return parse(code, mode='eval').body


def parse_stmt(code: str) -> stmt:
    return parse(code, mode='exec').body[0]


def log(*objects: Any):
    print(*objects)


def returned(return_val: Any, level: int) -> Any:
    log('  ' * level + f"return {repr(return_val)}")
    return return_val


class Transformer(NodeTransformer):

    def visit_Call(self, node):
        # print(f'visit call function: {dump(node.func)}') 

         if isinstance(node.func, Name) and node.func.id == self.ori_name:
             return Call(
                 func=parse_expr(self.traced_name),
                 args=[self.visit(a) for a in node.args] + [parse_expr('level')],   
                 keywords=node.keywords
             )
         
         return Call(
             func=self.visit(node.func),
             args=[self.visit(a) for a in node.args],
             keywords=node.keywords
             )

    def visit_FunctionDef(self, node: FunctionDef) -> FunctionDef:
        self.ori_name = node.name
        self.traced_name = node.name + '_traced'

        arg_names = [a.arg for a in node.args.args]
        arg_fmt = ', '.join([x + ' = ' + '{' + x + '}' for x in arg_names])
        enter_log = parse_stmt(f"log('  ' * level + f'call with {arg_fmt}')")

        return FunctionDef(
            name=self.traced_name,
            args=arguments(
                    args=node.args.args + [arg('level')],
                    defaults=[parse_expr('0')],
                    posonlyargs=node.args.posonlyargs,
                    kwonlyargs=node.args.kwonlyargs
                    ),
                    body=[enter_log] + [self.visit(s) for s in node.body],
                    decorator_list=node.decorator_list,
                    returns=node.returns
                ) 

    def visit_Return(self, node):

        # print(f'visit return value: {dump(node.value)}')
        return Return(
            value=Call(
            func=parse_expr('returned'),
            args=[self.visit(node.value), parse_expr('level')],
            keywords=[]
            ) 
        )

######## Tests ########

def call_traced(original_func: Callable, *args: Any) -> None:
    original_ast = parse(inspect.getsource(original_func))
    tr = Transformer()
    new_ast = tr.visit(original_ast)
    assert isinstance(new_ast.body[0], FunctionDef)

    new_func_code = unparse(fix_missing_locations(new_ast.body[0]))
    call_args = [repr(x) for x in args]
    call_func_code = f"{tr.traced_name}({', '.join(call_args)})"
    # to avoid scope issues, we simply wrap up the recursive func def and call in a closure
    code = f"def go():\n{with_indent(new_func_code)}\n{with_indent(call_func_code)}\ngo()"

    # Uncomment the following to show the final code
    from debuggingbook.bookutils import print_content
    print_content(code, '.py')
    print()

    exec(code)


def with_indent(code: str, level=1) -> str:
    lines = code.split('\n')
    indented = ['    ' * level + line for line in lines]
    return '\n'.join(indented)


if __name__ == '__main__':
    call_traced(fib, 4)

    arr = [12, 11, 13, 5, 6, 7]
    call_traced(merge_sort, arr, 0, len(arr) - 1)



