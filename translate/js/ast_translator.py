from ..translator import TranslationWalker

walker = TranslationWalker("js_ast")

@walker.visitor("int")
@walker.visitor("float")
@walker.visitor("string")
def visit_value(translator, node):
    return f"{repr(node.value)}"

@walker.visitor("word")
def visit_word(translator, node):
    return node.value

@walker.visitor("bool")
def visit_bool(translator, node):
    return "true" if node.value else "false"

@walker.visitor("null")
def visit_null(translator, node):
    return "null"

@walker.visitor("tuple")
def visit_tuple(translator, node):
    function = translator.translate(node.args[0])
    args = ", ".join(translator.translate(arg) for arg in node.args[1:])

    return f"{function}({args})"


