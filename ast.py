

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


def assert_next(stream):
    token = stream.next()
    if token is None:
        raise EOFError("failed to read token, reached end of file")
    return token

def read_value(stream):
    token = assert_next(stream)

    if token.name == "int":
        return ASTInt(int(token.content))
    elif token.name == "float":
        return ASTFloat(float(token.content))
    elif token.name == "string":
        return ASTString(token.content[1:-1])
    elif token.name == "true":
        return ASTBool(True)
    elif token.name == "false":
        return ASTBool(False)
    elif token.name == "null":
        return ASTNull()
    elif token.name == "word":
        return ASTWord(token.content)
    elif token.name == "open":
        return read_tuple(stream.revert())
    else:
        raise ValueError(f"unexpected token {token.name} could not be read as value")

def read_tuple(stream):
    open_bracket = assert_next(stream)

    if open_bracket.name != "open":
        raise ValueError(f"failed to read tuple, found no opening bracket")

    args = []
    token = assert_next(stream)
    while token.name != "close":
        args.append(read_value(stream.revert()))
        token = assert_next(stream)

    return ASTTuple(args)

def read_module(stream):
    statements = []
    try:
        while True:
            statements.append(read_value(stream))
    except EOFError:
        pass

    if not stream.done():
        token = stream.next()
        raise ValueError(f"encountered error on token {token.name} `{token.content}` at line, char: {token.pointer}")

    return statements
