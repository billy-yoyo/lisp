from tokenizer import (
    Tokenizer, 
    word_consumer, 
    wordlist_consumer,
    regex_consumer,
    TokenStream,
    TokenParser
)
from ast import parser
from scope import Scope
from lisplib import NATIVES
from argproc import ArgProc
from translate import translators
import sys

tokenizer = Tokenizer()
tokenizer.add_consumer("escaped_char", regex_consumer(r"^\\."))
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

def filter_tokens(tokens):
    new_tokens = []
    for token in tokens:
        if token.name == "whitespace":
            continue
        elif token.name == "escaped_char":
            token = token.copy(name="word", content=token.content[1:])
        new_tokens.append(token)
    return new_tokens

def compile(content):
    tokens = filter_tokens(tokenizer.consume_all(content))
    stream = TokenStream(tokens, parser=parser)
    return stream.parse("module")

def run_code(content):
    module = compile(content)
    print(f"--- module ---")
    print("\n".join(str(x) for x in module))
    print("--------------")
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
    if args.translate is not None:
        run_translate(args[0], args.translate, outfile=args.out)
    else:
        run_file(args[0])

argproc = ArgProc()
argproc.add_parameter("translate", "t")
argproc.add_parameter("out", "o")
args = argproc.read(sys.argv[1:])

run(args)
