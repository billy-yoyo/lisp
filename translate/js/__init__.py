from .ast_translator import walker as ast_walker
from .lib import lib_walker
from ..translator import TranslationWalker, Translator

global_header = """
const r$ = (v, d$) => v && v.r$ ? d$.push(v.r$) && false : true;
""".strip()

walker = TranslationWalker("js", global_header=global_header)
walker.merge(ast_walker)
walker.merge(lib_walker)

translator = walker.create_translator()
