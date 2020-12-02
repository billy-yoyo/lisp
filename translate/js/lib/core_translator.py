from ...translator import TranslationWalker

walker = TranslationWalker("js_core", config={
    "return_func_name": "r$",
    "do_object": "d$",
})

@walker.visitor("native:def")
def visit_native_def(translator, args):
    assert len(args) == 3
    name, func_args, body = args

    assert name.type == "word", f"first arg of def must be name"
    assert func_args.type == "tuple" and all(func_arg.type == "word" for func_arg in func_args.args), f"second arg of def must be list of variable names"

    func_args = [translator.translate(arg) for arg in func_args]
    joined_args = ", ".join(func_args)
    translated_body = translator.with_ctx({arg: True for arg in func_args}).translate(body)
    translator.ctx.set(name.content, True)

    return f"({name.content} = ({joined_args}) => {translated_body})"

def wrap_in_returner(translator, statement_ast):
    statement = translator.translate(statement_ast)

    ret_name = translator.config("return_func_name")
    do_obj = translator.config("do_object")

    return f"{ret_name}({statement},{do_obj})"
    

@walker.visitor("native:do")
def visit_native_do(translator, args):
    do_translator = translator.with_ctx()
    
    do_obj = translator.config("do_object")

    statements = [wrap_in_returner(do_translator, arg) for arg in args]
    statement_content = ' && \n'.join(stat for stat in statements)
    statement_content = "    " + statement_content.replace("\n", "\n    ")

    return f"({do_obj} => [\n{statement_content}\n] && {do_obj}.pop())([])"

@walker.visitor("native:return")
def visit_native_return(translator, args):
    assert len(args) == 1, f"return expects 1 arg, {len(args)} were given"
    value = translator.with_ctx().translate(args[0])

    return_func_name = translator.config("return_func_name")
    return f"{{ {return_func_name}: {value} }}"

    