

UNKNOWN_VAR = object()

class TranslationContext:
    def __init__(self, vars=None, shallow=None, capture=None, parent=None):
        self.parent = parent
        self.vars = vars or {}
        self.shallow = shallow or {}
        self.capture = capture or []

    def set(self, name, var):
        if len(self.capture) == 0 or name in self.capture:
            self.vars[name] = var
        elif self.parent:
            self.parent.set(name, var)

    def get(self, name):
        if name in self.shallow:
            return self.shallow[name]

        ctx = self
        while ctx is not None:
            if name in ctx.vars:
                return ctx.vars[name]
            ctx = ctx.parent
        return UNKNOWN_VAR

    def get_shallow(self, name):
        if name in self.shallow:
            return self.shallow[name]

        if name in self.vars:
            return self.vars[name]

    def bubble(self, name, var):
        ctx = self
        while ctx is not None:
            if name in ctx.capture:
                ctx.set(name, var)
            ctx = ctx.parent


class TranslationWalker:
    def __init__(self, name, config=None, global_header=None):
        self.name = name
        self.visitors = {}
        self._config = config or {}
        self.global_header = global_header

    def merge(self, walker):
        self.visitors.update(walker.visitors)
        self._config.update(walker._config)

    def set_config(self, key, value):
        self._config[key] = value

    def config(self, key, default=None):
        if key in self._config:
            return self._config[key]
        else:
            return default

    def create_translator(self, vars=None, capture=None, shallow=None):
        return Translator(self, TranslationContext(vars=vars, capture=capture, shallow=shallow))

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

    def config(self, key, default=None):
        return self.walker.config(key, default=default)

    def with_ctx(self, vars=None, capture=None, shallow=None):
        child_ctx = TranslationContext(vars=vars, capture=capture, shallow=shallow, parent=self.ctx)
        return Translator(self.walker, child_ctx)

    def translate(self, ast):
        return self.walker.visit(ast, self)

    def translate_all(self, asts):
        lines = [self.translate(ast) for ast in asts]
        header = self.walker.global_header or ""
        return header + "\n" + ";\n".join(lines) + ";"

