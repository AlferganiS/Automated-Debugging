import sys
from inspect import getsourcelines
from types import CodeType
from typing import Any, TextIO, List
from debuggingbook.Debugger import Debugger

class CallInfo:
    def __init__(self, caller: CodeType, line_no: int) -> None:
        self.caller = caller
        self.loc = line_no

    def __repr__(self) -> str:
        head = f'File "{self.caller.co_filename}", line {self.loc}, in {self.caller.co_name}'
        lines, start = getsourcelines(self.caller)
        code = lines[self.loc - start].strip()
        return f'{head}\n  {code}'

class Debugger(Debugger):
    def __init__(self, *, file: TextIO = sys.stdout) -> None:
        super().__init__(file=file)

        self.finishing: bool = False
        self.step_over: bool = False
        self.last_stack_len: int = 0
        self.last_line: int = 0
        self.frame = None
    
    def stop_here(self) -> bool:
        if self.finishing and self.now_finish():
            self.finishing = False
            return True

        if self.step_over and (self.now_next_line() or self.now_finish()):
            self.step_over = False
            return True

        return super().stop_here()

    def break_command(self, arg: str = "") -> None:
        """Set a breakpoint in given line. If no line is given, list all breakpoints"""
        if arg:
            try:
                line = int(arg)
                source_lines, start_line = getsourcelines(self.frame.f_code)
                end_line = start_line + len(source_lines) - 1
                if start_line <= line and line <= end_line:
                    self.breakpoints.add(line)
                else:
                    self.log(f"Line number {arg} out of bound ({start_line}-{end_line})")
            except ValueError:
                self.log(f"Expect a line number, but found '{arg}'")

        self.log("Breakpoints:", self.breakpoints)

    def delete_command(self, arg: str = "") -> None:
        """Delete breakpoint in line given by `arg`.
           Without given line, clear all breakpoints"""
        if arg:
            try:
                self.breakpoints.remove(int(arg))
            except ValueError:
                self.log(f"Expect a line number, but found '{arg}'")
            except KeyError:
                self.log(f"No such breakpoint: {arg}")
        else:
            self.breakpoints = set()

        self.log("Breakpoints:", self.breakpoints)

    def assign_command(self, arg: str) -> None:
        """Use as 'assign VAR=VALUE'. Assign VALUE to local variable VAR."""
        sep = arg.find('=')
        if sep > 0:
            var = arg[:sep].strip()
            expr = arg[sep + 1:].strip()
        else:
            self.help_command("assign")
            return

        if not var.isidentifier():
            self.log(f"SyntaxError: '{var}' is not an identifier")
            return

        vars = self.local_vars
        if not var in vars:
            self.log(f"Warning: a new variable '{var}' is created")

        try:
            vars[var] = eval(expr, self.frame.f_globals, vars)
        except Exception as err:
            self.log(f"{err.__class__.__name__}: {err}")

    def where_command(self, arg: str = "") -> None:
        """Show stack trace"""
        self.log("Traceback (most recent call last):")
        for info in self.get_call_info_stack():
            self.log(info)

    def get_call_info_stack(self) -> None:
        f = self.frame
        stack = [CallInfo(f.f_code, f.f_lineno)]
        while f.f_code.co_name != 'debug_main':
            f = f.f_back
            stack.append(CallInfo(f.f_code, f.f_lineno))

        return reversed(stack)

    def get_stack_len(self) -> int:
        f = self.frame
        length = 1
        while f.f_code.co_name != 'debug_main':
            f = f.f_back
            length += 1

        return length

    def finish_command(self, arg: str = "") -> None:
        """Resume execution until the current function returns"""
        self.finishing = True
        self.last_stack_len = self.get_stack_len()

        self.stepping = False
        self.interact = False

    def now_finish(self) -> bool:
        return self.event == 'return' and self.get_stack_len() == self.last_stack_len
    
    def next_command(self, arg: str = "") -> None:
        """Resume execution until the next line or the current function returns"""
        self.step_over = True
        self.last_line = self.frame.f_lineno
        self.last_stack_len = self.get_stack_len()

        self.stepping = False
        self.interact = False

    def now_next_line(self) -> bool:
        return self.frame.f_lineno > self.last_line

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No input file", file=sys.stderr)
        exit(1)

    module_name = sys.argv[1][:-3] # remove .py
    exec(f"from {module_name} import debug_main")

    with Debugger():
        debug_main()
