
class AST:
    type = "ast"

class ASTValue(AST):
    type = "value"
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.type}: {repr(self.value)}"

class ASTInt(ASTValue):
    type = "int"

class ASTFloat(ASTValue):
    type = "float"

class ASTString(ASTValue):
    type = "string"

class ASTBool(ASTValue):
    type = "bool"

class ASTNull(ASTValue):
    type = "null"
    def __init__(self):
        super().__init__(None)

class ASTWord(ASTValue):
    type = "word"

class ASTTuple(AST):
    type = "tuple"
    def __init__(self, args):
        self.args = args

    def __str__(self):
        lines = [f"tuple:"]
        for arg in self.args:
            arg_lines = str(arg).split("\n")
            lines += [f"  {line}" for line in arg_lines]
        return "\n".join(lines)