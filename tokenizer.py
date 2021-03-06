import re

class Token:
    def __init__(self, name, content, pointer):
        self.name = name
        self.content = content
        self.pointer = pointer

    def copy(self, name=None, content=None, pointer=None):
        return Token(
            name=name or self.name,
            content=content or self.content,
            pointer=pointer or self.pointer
        )

    def __str__(self):
        return self.name

class Tokenizer:
    def __init__(self):
        self.consumers = {}

    def add_consumer(self, name, consumer):
        self.consumers[name] = consumer

    def consume(self, s, pointer):
        best_length = None
        best_name = None
        for name, consumer in self.consumers.items():
            length = consumer(s)
            if best_length is None or length > best_length:
                best_length = length
                best_name = name

        if best_name is not None:
            return Token(best_name, s[:best_length], pointer), s[best_length:]
        else:
            return None, s

    def consume_all(self, s):
        tokens = []
        pointer = (0, 0)
        token, s = self.consume(s, pointer)
        while token is not None and s:
            tokens.append(token)
            lines = token.content.split("\n")
            if len(lines) > 1:
                pointer = (pointer[0] + len(lines) - 1, len(lines[-1]))
            else:
                pointer = (pointer[0], pointer[1] + len(lines[0]))
            token, s = self.consume(s, pointer)

        if token:
            tokens.append(token)

        if s:
            raise ValueError(f"failed to consume rest of string: {s}")

        return tokens


class TokenStream:
    def __init__(self, tokens, parser=None, pointer=0):
        self.tokens = tokens
        self.pointer = pointer
        self.parser = parser

    def next(self):
        if self.pointer < len(self.tokens):
            token = self.tokens[self.pointer]
            self.pointer += 1
            return token
        else:
            return None

    def last(self):
        return self.tokens[self.pointer - 1]

    def revert(self):
        self.pointer -= 1
        return self

    def done(self):
        return self.pointer >= len(self.tokens)

    def branch(self):
        return TokenStream(self.tokens, parser=self.parser, pointer=self.pointer)

    def merge(self, branch):
        self.pointer = branch.pointer

    def parse(self, name):
        if self.parser is None:
            raise ValueError("stream has no associated parser")
            
        branch = self.branch()
        try:
            result = self.parser.parse(name, branch)
        except Exception as e:
            raise e
        else:
            self.merge(branch)
            return result

    def attempt_parse(self, name):
        if self.parser is not None:
            branch = self.branch()
            result = self.parser.attempt_parse(name, branch)
            if result is not None:
                self.merge(branch)
            return result
        return None

    def attempt_macro(self):
        return self.parser.attempt_macro(self)

    def __str__(self):
        return " ".join(str(token) for token in self.tokens[self.pointer:])


def word_consumer(word):
    return lambda s: len(word) if s.startswith(word) else 0

def wordlist_consumer(words):
    return lambda s: max(len(word) if s.startswith(word) else 0 for word in words)

def regex_consumer(pattern):
    regex = re.compile(pattern)

    def consumer(s):
        match = regex.match(s)
        if match is not None:
            return len(match.group(0))
        else:
            return 0
    
    return consumer

class TokenParser:
    def __init__(self):
        self.parsers = {}
        self.macros = []

    def add_parser(self, name, parser):
        self.parsers[name] = parser

    def parser(self, name):
        def decorator(func):
            self.add_parser(name, func)
            return func
        return decorator

    def add_macro(self, macro):
        self.macros.append(macro)

    def attempt_macro(self, stream):
        for macro in self.macros:
            branch = stream.branch()
            match = macro.pattern.read_match(branch)
            if match is not None:
                print(f"macro matched with {match}")
                stream.merge(branch)
                return macro.template.create(match)
        return None

    def attempt_parse(self, name, stream):
        try:
            if name in self.parsers:
                return self.parsers[name](stream)
        except:
            pass
        return None
    
    def parse(self, name, stream):
        return self.parsers[name](stream)