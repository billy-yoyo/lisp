from ..translator import TranslationWalker

js_walker = TranslationWalker("js")

@js_walker.visitor("int")
@js_walker.visitor("float")
@js_walker.visitor("string")
@js_walker.visitor("word")
def visit_value(translator, node):
    return f"{node.value}"

@js_walker.visitor("bool")
def visit_bool(translator, node):
    return "true" if node.value else "false"

@js_walker.visitor("null")
def visit_null(translator, node):
    return "null"

@js_walker.visitor("tuple")
def visit_tuple(translator, node):
    function = translator.translate(node.args[0])
    args = ", ".join(translator.translate(arg) for arg in node.args[1:])

    return f"{function}({args})"

@js_walker.visitor("native:def")
def visit_native_def(translator, args):
    assert len(args) == 3
    name, func_args, body = args

    assert name.type == "word", f"first arg of def must be name"
    assert func_args.type == "tuple" and all(func_arg.type == "word" for func_arg in func_args.args), f"second arg of def must be list of variable names"

    func_args = [translator.translate(arg) for arg in func_args]
    joined_args = ", ".join(func_args)
    translated_body = translator.with_ctx({arg: True for arg in func_args}).translate(body)

    return f"const {name.content} = ({joined_args}) => {{{translated_body}}};"

js_transltor = js_walker.create_translator()
