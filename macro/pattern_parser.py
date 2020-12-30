from scope import Scope
from .pattern import TokenPattern, ASTPattern, ReadPattern, SequencePattern, MacroMatch

def token_pattern(scope, args):
    data = {}

    for arg in args:
        assert arg.type == "tuple" and len(arg.args) == 2, f"key/value pair must have exactly 2 values, {len(arg.args)} were given"
        key, value = arg.args

        assert key.type in ["word", "string"], f"key must be a word or string, not {key.type}"
        assert value.type in ["word", "string"], f"value must be a word or string, not {value.type}"
        assert key.value in ["name", "content"], f"key must be one of 'name' or 'content', not {key.value}"
        data[key.value] = value.value

    return TokenPattern(**data)

def ast_pattern(scope, args):
    assert len(args) == 1, f"ast exepcted 1 argument, was given {len(args)}"
    
    name = args[0]
    assert name.type in ["word", "string"], "ast name must be word or string"

    return ASTPattern(name.value)

def read_pattern(scope, args):
    assert len(args) > 0, "invalid read call"

    flags = {}
    if args[0].type == "word" and args[0].value == "many":
        flags[ReadPattern.MANY] = True
        args = args[1:]

    assert len(args) > 0, "no pattern for read call"
    pattern = parse_pattern(args[0])

    save_type, save_name = None, None
    if len(args) > 1:
        assert len(args) == 3, f"read call expected to args at end, got {len(args) - 1}"
        save_type, save_name = args[1:]
        
        assert save_type.type == "word" and save_type.value in ["as", "into"]
        assert save_name.type in ["word", "string"]

        if save_type.value == "as":
            save_type = MacroMatch.AS
        else:
            save_type = MacroMatch.INTO

        save_name = save_name.value

    return ReadPattern(pattern=pattern, flags=flags, save_type=save_type, save_name=save_name)
        
def sequence_pattern(scope, args):
    return SequencePattern([parse_pattern(arg) for arg in args])

pattern_scope = Scope()
pattern_scope.define("token", token_pattern)
pattern_scope.define("ast", ast_pattern)
pattern_scope.define("read", read_pattern)
pattern_scope.define("seq", sequence_pattern)

def parse_pattern(pattern_ast):
    if pattern_ast.type == "word":
        return TokenPattern(content=pattern_ast.value)

    return pattern_scope.execute_statement(pattern_ast)
