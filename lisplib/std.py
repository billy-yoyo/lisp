

def lisp_print(scope, args):
    print(" ".join(str(scope.execute_statement(arg)) for arg in args))

NATIVES = {
    "print": lisp_print
}
