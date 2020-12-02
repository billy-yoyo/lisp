from ...translator import TranslationWalker

walker = TranslationWalker("js_math")

@walker.visitor("native:+")
def visit_native_add(translator, args):
    return " + ".join(translator.translate(arg) for arg in args)

@walker.visitor("native:-")
def visit_native_sub(translator, args):
    return " - ".join(translator.translate(arg) for arg in args)

@walker.visitor("native:*")
def visit_native_mult(translator, args):
    return " * ".join(translator.translate(arg) for arg in args)

@walker.visitor("native:/")
def visit_native_div(translator, args):
    return " / ".join(translator.translate(arg) for arg in args)

@walker.visitor("native:^")
def visit_native_pow(translator, args):
    return " ** ".join(translator.translate(arg) for arg in args)

@walker.visitor("native:%")
def visit_native_modulo(translator, args):
    return " % ".join(translator.translate(arg) for arg in args)
