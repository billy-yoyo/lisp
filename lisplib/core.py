from scope import Scope, UNKNOWN_VAR

RETURN_NAME = "0_return"

class ReturnedValue:
    def __init__(self, value):
        self.value = value


def macro(scope, args):
    assert len(args) == 2, f"macro expected 2 args, {len(args)} were given"
    pattern, template = args




def def_func(scope, args):
    assert len(args) == 3, f"def expected 3 args, {len(args)} were given"
    name, func_args, body = args

    assert name.type == "word", f"first arg of def must be name"
    assert func_args.type == "tuple" and all(func_arg.type == "word" for func_arg in func_args.args), f"second arg of def must be list of variable names"

    arg_names = [func_arg.content for func_arg in func_args.args]

    def executor(source_scope, arg_values):
        arg_values = [source_scope.execute_statement(value) for value in arg_values]
        if len(arg_values) != len(arg_names):
            raise ValueError(f"function {name} expects {len(arg_names)} args, given {len(arg_values)}")
        
        function_scope = scope.branch(
            vars={name: value for name, value in zip(arg_names, arg_values)},
        )

        return function_scope.execute_statement(body)

    scope.define(name.content, executor)

def do(scope, statements):
    do_scope = scope.branch()
    for statement in statements:
        result = do_scope.execute_statement(statement)
        if isinstance(result, ReturnedValue):
            return result.value



def return_value(scope, args):
    assert len(args) == 1, f"return expects 1 arg, {len(args)} were given"
    value = scope.execute_statement(args[0])

    return ReturnedValue(value)



NATIVES = {
    "def": def_func,
    "do": do,
    "return": return_value,
    "macro": macro
}
