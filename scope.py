
UNKNOWN_VAR = object()

class Scope:
    def __init__(self, vars=None, parent=None):
        self.vars = vars or {}
        self.parent = parent

    def branch(self, vars=None):
        return Scope(vars=vars, parent=self)

    def native(self, name):
        def decorator(func):
            self.vars[name] = func
            return func
        return decorator

    def add_natives(self, natives):
        self.vars.update(natives)

    def define(self, identifier, value):
        self.vars[identifier] = value

    def get(self, identifier):
        scope = self
        while scope is not None:
            if identifier in scope.vars:
                return scope.vars[identifier]
            else:
                scope = scope.parent 
        return UNKNOWN_VAR

    def execute_statement(self, statement):
        if statement.type == "tuple":
            function = self.execute_statement(statement.args[0])
            args = statement.args[1:]

            return function(self, args)
        elif statement.type == "word":
            value = self.get(statement.value)

            if value is UNKNOWN_VAR:
                raise ValueError(f"unknown variable {statement.value}")

            return value
        else:
            return statement.value
            

    def execute_module(self, module):
        module_scope = Scope(parent=self)
        for statement in module:
            module_scope.execute_statement(statement)