from .translator import Translator, TranslationContext
from .js import translator as js_translator

translators = {
    "js": js_translator
}
