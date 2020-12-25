from .classes import *
from tokenizer import TokenParser
from macro import create_macro

parser = TokenParser()

def assert_next(stream):
    token = stream.next()
    if token is None:
        raise EOFError("failed to read token, reached end of file")
    return token

def safe_token(func):
    def wrapper(stream, token=None):
        return func(stream, token or assert_next(stream))
    return wrapper

@parser.parser("int")
@safe_token
def read_int(stream, token):
    assert token.name == "int"
    return ASTInt(int(token.content))

@parser.parser("float")
@safe_token
def read_float(stream, token):
    assert token.name == "float"
    return ASTFloat(float(token.content))

@parser.parser("string")
@safe_token
def read_string(stream, token):
    assert token.name == "string"
    return ASTString(token.content[1:-1])

@parser.parser("true")
@safe_token
def read_true(stream, token):
    assert token.name == "true"
    return ASTBool(True)

@parser.parser("false")
@safe_token
def read_false(stream, token):
    assert token.name == "false"
    return ASTBool(False)

@parser.parser("bool")
@safe_token
def read_bool(stream, token):
    assert token.name in ["true", "false"]
    return ASTBool(token.name == "true")

@parser.parser("null")
@safe_token
def read_null(stream, token):
    assert token.name == "null"
    return ASTNull()

@parser.parser("word")
@safe_token
def read_word(stream, token):
    assert token.name == "word"
    return ASTWord(token.content)

@parser.parser("value")
def read_value(stream):
    token = assert_next(stream)

    # first attempt to read any macros
    if stream.parser is not None:
        result = stream.attempt_macro()
        if result is not None:
            return result

    if token.name == "int":
        return read_int(stream, token)
    elif token.name == "float":
        return read_float(stream, token)
    elif token.name == "string":
        return read_string(stream, token)
    elif token.name == "true":
        return read_true(stream, token)
    elif token.name == "false":
        return read_false(stream, token)
    elif token.name == "null":
        return read_null(stream, token)
    elif token.name == "word":
        return read_word(stream, token)
    elif token.name == "open":
        return read_tuple(stream.revert())
    else:
        raise ValueError(f"unexpected token {token.name} could not be read as value")

@parser.parser("tuple")
def read_tuple(stream):
    open_bracket = assert_next(stream)

    if open_bracket.name != "open":
        raise ValueError(f"failed to read tuple, found no opening bracket")

    args = []
    token = assert_next(stream)
    while token.name != "close":
        value = read_value(stream.revert())
        if isinstance(value, list) or isinstance(value, tuple):
            args += value
        else:
            args.append(value)
        token = assert_next(stream)

    # catch macros
    if len(args) > 2 and args[0].type == "word" and args[0].value == "#" \
            and args[1].type == "word" and args[1].value == "macro":
        # parse macro rather than reading tuple
        macro = create_macro(args[2:])
        stream.parser.add_macro(macro)

        # empty list represtens no AST
        return []

    return ASTTuple(args)

@parser.parser("module")
def read_module(stream):
    statements = []
    try:
        while True:
            value = read_value(stream)
            if isinstance(value, list) or isinstance(value, tuple):
                statements += value
            else:
                statements.append(value)
    except EOFError:
        pass

    if not stream.done():
        token = stream.next()
        raise ValueError(f"encountered error on token {token.name} `{token.content}` at line, char: {token.pointer}")

    return statements
