from .pattern_parser import parse_pattern
from .pattern import MacroPattern
from .template import parse_template, ASTTemplate

class Macro:
    def __init__(self, pattern, template):
        self.pattern = pattern
        self.template = template

def create_macro(args):
    assert len(args) == 2, f"macro expected 2 args, {len(args)} were given"
    pattern, template = args

    pattern = parse_pattern(pattern)
    if not isinstance(pattern, MacroPattern):
        raise ValueError("invalid macro pattern")
    
    template = parse_template(template)
    if not isinstance(template, ASTTemplate):
        raise ValueError("invalid macro template, must return ast template")

    return Macro(pattern, template)
