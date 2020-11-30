from tokenizer import (
    Tokenizer, 
    word_consumer, 
    wordlist_consumer,
    regex_consumer,
    TokenStream
)
from ast import read_module
from scope import Scope
from lisplib import NATIVES
import sys

tokenizer = Tokenizer()
tokenizer.add_consumer("open", word_consumer("("))
tokenizer.add_consumer("close", word_consumer(")"))
tokenizer.add_consumer("true", word_consumer("true"))
tokenizer.add_consumer("false", word_consumer("false"))
tokenizer.add_consumer("null", word_consumer("null"))
tokenizer.add_consumer("word", regex_consumer(r"^(?:[a-zA-Z$_][a-zA-Z$_0-9]*|[!£%^&*-+=\[\]\{\}@'#~,<.>/?\\])"))
tokenizer.add_consumer("int", regex_consumer(r"^[0-9]+"))
tokenizer.add_consumer("float", regex_consumer(r"^[0-9]+\.[0-9]+"))
tokenizer.add_consumer("string", regex_consumer(r"^\"(?:[^\"\\]|\\.)*\""))
tokenizer.add_consumer("whitespace", regex_consumer(r"^\s+"))

global_scope = Scope()
global_scope.add_natives(NATIVES)

def compile(content):
    tokens = [token for token in tokenizer.consume_all(content) if token.name != "whitespace"]
    print(" ".join(token.name for token in tokens))
    stream = TokenStream(tokens)
    return read_module(stream)

def run(content):
    module = compile(content)
    print("\n".join(str(statement) for statement in module))
    global_scope.execute_module(module)


def run_file(filename):
    with open(filename, "r") as f:
        text = f.read()
    run(text)

run_file(sys.argv[1])
