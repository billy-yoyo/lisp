from ...translator import TranslationWalker

walker = TranslationWalker("js_std")

@walker.visitor("native:print")
def visit_native_print(translator, args):
    values = f", ".join(translator.translate(arg) for arg in args)

    return f"console.log({values})"

    