from lisplib import NATIVES
from scope import Scope
"""

(
    (ast ($name $args))
)

"""

def template_ast(scope, args):
    pass

template_scope = Scope()
template_scope.add_natives(NATIVES)
template_scope.define("ast", template_ast)

def parse_template(template_ast):
    return template_scope.execute_statement(template_ast)