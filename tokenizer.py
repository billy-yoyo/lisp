import re

class Token:
    def __init__(self, name, content):
        self.name = name
        self.content = content

class Tokenizer:
    def __init__(self):
        self.consumers = {}

    def add_consumer(self, name, consumer):
        self.consumers[name] = consumer

    def consume(self, s):
        best_length = None
        best_name = None
        for name, consumer in self.consumers.items():
            length = consumer(s)
            if best_length is None or length > best_length:
                best_length = length
                best_name = name

        if best_name is not None:
            return Token(best_name, s[:best_length]), s[best_length:]
        else:
            return None, s

    def consume_all(self, s):
        tokens = []
        token, s = self.consume(s)
        while token is not None and s:
            tokens.append(token)
            token, s = self.consume(s)
        return tokens


class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pointer = 0

    def next(self):
        if self.pointer < len(self.tokens):
            token = self.tokens[self.pointer]
            self.pointer += 1
            return token
        else:
            return None

    def revert(self):
        self.pointer -= 1
        return self


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



    