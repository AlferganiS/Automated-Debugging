import ast
from typing import Any, Optional, Dict, List, Tuple

############## TYPES ##############

class Type:
    def __eq__(self, other):
        return isinstance(other, Anything) or type(self) == type(other)

    def __repr__(self) -> str:
        return self.__class__.__name__
    
    def __str__(self) -> str:
        return self.__repr__()
    

class Anything(Type):
    def __eq__(self, other):
        return isinstance(other, Type)
    

class Int(Type):
    pass


class Str(Type):
    pass

############# SCOPES ##############

class TypeScope:
    
    def __init__(self, parent=None):
        self.parent = parent
        self.types: Dict[str, Type] = dict()
        
    def enter(self) -> Any:
        return TypeScope(self)
    
    def exit(self) -> Any:
        return self.parent if self.parent else self
    
    def put(self, name: str, type_: Type) -> None:
        self.types[name] = type_
        
    
    def get(self, name: str) -> Optional[Type]:
        if name in self.types:
            return self.types[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None
        
    def update(self, name: str, type_: Type):
        if name in self.types:
            self.types[name] = type_
            return True
        elif self.parent:
            result = self.parent.update(name, type_)
            if not result:
                self.put(name, type_)
        return False
    

class FunctionScope:
    
    def __init__(self):
        self.types: Dict[str, Tuple[List[Type], Type]] = dict()
    
    def put(self, name: str, types: Tuple[List[Type], Type]) -> None:
        self.types[name] = types
        
    
    def get(self, name: str) -> Optional[Tuple[List[Type], Type]]:
        if name in self.types:
            return self.types[name]
        else:
            return None
        
########## TYPE CHECKING ##########

class ForwardTypeChecker(ast.NodeVisitor):
    
    def __init__(self):
        self.scope = TypeScope()
        self.functions = FunctionScope()
        self.current_return = None
        
    def generic_visit(self, node: ast.AST) -> Optional[Type]:
        raise SyntaxError(f'Unsupported node {node.__class__.__name__}')
        
    def visit_Module(self, node: ast.Module) -> Optional[Type]:
        for n in node.body:
            self.visit(n)
        return None
        
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Optional[Type]:
        assert self.current_return is None, \
            f'Nested function {node.name}'
        self.scope = self.scope.enter()
        types = list()
        args = node.args.args
        rets = node.returns
        body = node.body

        # order of appearance to the types variable, and put the types
        # in the scope.

        for arg in args:

            if arg.annotation and arg.annotation.id == 'int':
                self.scope.put(arg.arg, Int())
                types.append(Int())

            elif arg.annotation and arg.annotation.id == 'str':
                self.scope.put(arg.arg, Str())
                types.append(Str())

            else:
                self.scope.put(arg.arg, Anything())
                types.append(Anything())


        returns = Anything()

        # function return value

        
        if node.returns and node.returns.id == 'int':
            returns = Int()
        elif node.returns and node.returns.id == 'str':
            returns = Str()


        self.functions.put(node.name, (types, returns))
        self.current_return = returns
        
        # body

        for part in body:
            self.visit(part)

        self.current_return = None
        self.scope = self.scope.exit()
        return None
    
    def visit_Assign(self, node: ast.Assign) -> Optional[Type]:
        
        assert len(node.targets) == 1, \
            'Targets is longer than 1'
        assert isinstance(node.targets[0], ast.Name), \
            'Target is not a Name'
        target = node.targets[0]
        
        # target's (target.id) type in self.scope

        self.scope.update(target.id, self.visit(node.value))

        return None
    
    def visit_AnnAssign(self, node: ast.AnnAssign) -> Optional[Type]:
        assert isinstance(node.target, ast.Name), \
            'Target is not a Name'
        assert isinstance(node.annotation, ast.Name), \
            'Annotation is not a Name'
        assert node.value is not None, \
            'Value is None'

        # the target (hint: node.annotation) and check if they match

        type_ = self.visit(node.value)

        if node.annotation.id == 'int':
            self.scope.put(node.target.id, Int())
        elif node.annotation.id == 'str':
            self.scope.put(node.target.id, Str())
        else:
            self.scope.put(node.target.id, Anything())

        if self.scope.get(node.target.id) != type_:
            raise TypeError(
                f'{node.target.id} has not inferred Type {type_}')

        return None
    
    def visit_Expr(self, node: ast.Expr) -> Optional[Type]:

        self.visit(node.value)
        return None
    
    def visit_Return(self, node: ast.Return) -> Optional[Type]:
        # current_return type

        type_ = self.visit(node.value)

        if self.current_return != type_:
            raise TypeError(f'Expected return type {self.current_return} does not match {type_}')



    def visit_Name(self, node: ast.Name) -> Optional[Type]:
        # if it does not exist
        # Return the type of the expression

        type_ = self.scope.get(node.id)

        if type_ is None:
            raise TypeError(f'Undefined use of {node.id}')

        return type_



    def visit_BinOp(self, node: ast.BinOp) -> Optional[Type]:
        assert (isinstance(node.op, ast.Add) or
                isinstance(node.op, ast.Mult)), \
            f'Unsupported op {node.op.__class__.__name__}'
        # with the operator Add (+) or Mult (*)
        # Return the type of the expression

        type_1 = self.visit(node.left)
        type_2 = self.visit(node.right)

        if isinstance(type_1, Anything):
            return type_2
        
        elif isinstance(type_2, Anything):
            return type_1
        
        elif isinstance(node.op, ast.Add):
            if type_1 == type_2:
                return type_1
            
            else:
                raise TypeError(
                    f'Unsupported op {node.op.__class__.__name__} for types {type_1}, {type_2}')
            
        elif (type_1, type_2) == (Int(), Str()) or (type_1, type_2) == (Str(), Int()):
            return Str()
        
        elif (type_1, type_2) == (Int(), Int()):
            return Int()
        
        else:
            raise TypeError(
                f'Unsupported op {node.op.__class__.__name__} for types {type_1}, {type_2}')


    def visit_Call(self, node: ast.Call) -> Optional[Type]:
        assert isinstance(node.func, ast.Name), \
            'Func is not a Name'
        expected_types = self.functions.get(node.func.id)
        assert expected_types is not None, \
            'Func not defined'
        expected_types, return_type = expected_types
        assert len(expected_types) == len(node.args), \
            'Number of args do not match'
        
        # arguments

        for expected_type, arg in zip(expected_types, node.args):
            type_ = self.visit(arg)
            
            if expected_type != type_:
                raise TypeError(
                    f'Type {type_} of arg {arg} does not match {expected_type}')
                
        return return_type


    def visit_Constant(self, node: ast.Constant) -> Optional[Type]:
        # format that matches

        if isinstance(node.value, int):
            return Int()
        elif isinstance(node.value, str):
            return Str()
        else:
            return Anything()

############## TESTS ##############

def test(program: str, failing: bool = False):
    try:
        tree = ast.parse(program)
        checker = ForwardTypeChecker()
        checker.visit(tree)
    except AssertionError:
        pass
    except SyntaxError:
        pass
    except TypeError:
        return failing
    else:
        return not failing


if __name__ == '__main__':
    assert test('''
def f(x: int, y: int) -> int:
    return x + y

z: int = f(2, 3)
'''), 'test 1 failed'

    assert test('''
'a' + 3
''', failing=True), 'test 2 failed'

    assert test('''
def f(x: int) -> str:
    return x
''', failing=True), 'test 3 failed'

    assert test('''
a
''', failing=True), 'test 4 failed'
    assert test('''
def f(x: int):
    return x

y: int = f(2)
'''), 'test 5 failed'

    assert test('''
def f(x: int) -> str:
    return 'a' * x

y: int = f(2)
''', failing=True), 'test 6 failed'

    assert test('''
def f(x: int) -> int:
    return x

y: int = f('a')
''', failing=True), 'test 7 failed'
