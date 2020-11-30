from .translator import Translator, TranslationContext
from .js import js_translator

translators = {
    "js": js_translator
}
