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
from runargs import run_args
from translate import translators

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
    stream = TokenStream(tokens)
    return read_module(stream)

def run_code(content):
    module = compile(content)
    global_scope.execute_module(module)

def run_file(filename):
    with open(filename, "r") as f:
        content = f.read()
    run_code(content)

def run_translate(filename, target, outfile=None):
    with open(filename, "r") as f:
        content = f.read()

    if not target in translators:
        raise ValueError(f"unknown translation target {target}")

    module = compile(content)
    output = translators[target].translate_all(module)

    if outfile:
        with open(outfile, "w") as f:
            f.write(output)
    else:
        print(output)

def run(args):
    if "translate" in args.named:
        run_translate(args.positional[0], args.named["translate"], outfile=args.named.get("out", None))
    else:
        run_file(args.positional[0])

run(run_args({
    "t": "translate",
    "o": "out"
}))
