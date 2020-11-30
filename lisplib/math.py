
def lisp_add(scope, args):
    return sum(scope.execute_statement(arg) for arg in args)

def lisp_sub(scope, args):
    total = scope.execute_statement(args[0])
    for arg in args[1:]:
        total -= scope.execute_statement(arg)
    return total

def lisp_mult(scope, args):
    total = 1
    for arg in args:
        total = total * scope.execute_statement(arg)
    return total

def lisp_div(scope, args):
    total = scope.execute_statement(args[0])
    for arg in args[1:]:
        total /= scope.execute_statement(arg)
    return total

def lisp_pow(scope, args):
    total = scope.execute_statement(args[0])
    for arg in args[1:]:
        total **= scope.execute_statement(arg)
    return total

def lisp_modulo(scope, args):
    total = scope.execute_statement(args[0])
    for arg in args[1:]:
        total %= scope.execute_statement(arg)
    return total

NATIVES = {
    "+": lisp_add,
    "-": lisp_sub,
    "*": lisp_mult,
    "/": lisp_div,
    "^": lisp_pow,
    "%": lisp_modulo
}