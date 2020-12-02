from .core_translator import walker as core_walker
from .math_translator import walker as math_walker
from .std_translator import walker as std_walker
from ...translator import TranslationWalker

lib_walker = TranslationWalker("js_lib")
lib_walker.merge(core_walker)
lib_walker.merge(math_walker)
lib_walker.merge(std_walker)
