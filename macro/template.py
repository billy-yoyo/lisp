from lisplib import NATIVES
from scope import Scope, UNKNOWN_VAR
from ast import ASTTuple
"""

(
    (ast ($name $args))
)

"""

class ASTTemplatePlaceholder:
    type = "template_placeholder"
    def __init__(self, value):
        self.value = value 

class ASTTemplate:
    def __init__(self, template_ast):
        self.template_ast = template_ast

    def replace_templates(self, match, ast):
        if ast.type == "tuple":
            new_args = []
            for arg in ast.args:
                new_args += self.replace_templates(match, arg)
            return ASTTuple(new_args)
        elif ast.type == "template_placeholder":
            replacement = match.get(ast.value)
            if replacement is UNKNOWN_VAR:
                raise ValueError(f"unknown ast interpolation name {ast.value}")

            if isinstance(replacement, list) or isinstance(replacement, tuple):
                return replacement
            else:
                return [replacement]
        else:
            return [ast]
    
    def create(self, match):
        return self.replace_templates(match, self.template_ast).args 

def tuple_mutator(scope, tuple_ast):
    new_args = []
    escaped = False
    interpolate = False
    for arg in tuple_ast.args:
        if escaped:
            new_args.append(arg)
            escaped = False 
        elif interpolate:
            if arg.type != "word" and arg.type != "string":
                raise ValueError("ast interpolation names must be words or strings")

            new_args.append(ASTTemplatePlaceholder(arg.value))
            interpolate = False
        elif arg.type == "word" and arg.value == "\\":
            escaped = True
        elif arg.type == "word" and arg.value == "$":
            interpolate = True
        elif arg.type == "tuple":
            new_args.append(tuple_mutator(scope, arg))
        else:
            new_args.append(arg)
    return ASTTuple(new_args)
        

def template_ast(scope, args):
    assert len(args) == 1, f"ast expects 1 arg, {len(args)} given"
    
    ast = args[0]
    assert ast.type == "tuple", f"ast expects first arg to be a tuple"

    return ASTTemplate(tuple_mutator(scope, ast))

template_scope = Scope()
template_scope.add_natives(NATIVES)
template_scope.define("ast", template_ast)

def parse_template(template_ast):
    sub_scope = Scope(parent=template_scope)
    
    return sub_scope.execute_statement(template_ast)