

UNKNOWN_VAR = object()

class TranslationContext:
    def __init__(self, vars=None, parent=None):
        self.parent = parent
        self.vars = {}

    def set(self, name, var):
        self.vars[name] = var

    def get(self, name):
        ctx = self
        while ctx is not None:
            if name in ctx.vars:
                return ctx.vars[name]
            ctx = ctx.parent
        return UNKNOWN_VAR


class TranslationWalker:
    def __init__(self, name):
        self.name = name
        self.visitors = {}

    def create_translator(self, vars=None):
        return Translator(self, TranslationContext(vars=vars))

    def add_visitor(self, ast_type, visitor):
        self.visitors[ast_type] = visitor

    def visitor(self, ast_type):
        def decorator(visitor):
            self.add_visitor(ast_type, visitor)
            return visitor
        return decorator

    def visit(self, ast, translator):
        # special consideration for native function calls
        if ast.type == "tuple" and len(ast.args) > 0:
            # attempting to call an undefined variable; assume this is a native call
            if ast.args[0].type == "word" and translator.ctx.get(ast.args[0].value) is UNKNOWN_VAR:
                node_name = f"native:{ast.args[0].value}"
                if node_name not in self.visitors:
                    raise TypeError(f"no {self.name} visitor for native function {node_name}")

                return self.visitors[node_name](translator, ast.args[1:])

        if ast.type not in self.visitors:
            raise TypeError(f"no {self.name} visitor for ast type {ast.type}")

        if translator is None:
            raise ValueError("must give translator")

        return self.visitors[ast.type](translator, ast)


class Translator:
    def __init__(self, walker, ctx):
        self.walker = walker
        self.ctx = ctx

    def with_ctx(self, vars=None):
        child_ctx = TranslationContext(vars=vars, parent=self.ctx)
        return Translator(self.walker, child_ctx)

    def translate(self, ast):
        return self.walker.visit(ast, self)

