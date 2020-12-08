
"""
patterns:
 - token pattern, matches a single token by type and/or content
 - 


examples:
(read (token (type word)) as name) \( (read many ((read (ast value) into args) ,)) (ready (ast value) into args) \)

"""

class MacroMatch:
    def __init__(self):
        self.data = {}

    def set(self, name, value):
        self.data[name] = value


class MacroPattern:
    def matches(self, stream):
        return False

    def read_match(self, stream, match=None):
        if self.matches(stream):
            return match or MacroMatch()
        return None


class TokenPattern(MacroPattern):
    def __init__(self, name=None, content=None):
        super().__init__()
        self.name = name
        self.content = content

    def matches(self, stream):
        token = stream.next()
        if self.name is not None and token.name != self.name:
            return False

        if self.content is not None and token.content != self.content:
            return False

        return True


class ASTPattern(MacroPattern):
    def __init__(self, name=None):
        super().__init__()
        self.name = name


class ReadPattern(MacroPattern):
    MANY = "many"

    def __init__(self, pattern=None, flags=None, save_as=None):
        super().__init__()
        self.pattern = pattern
        self.flags = flags
        self.save_as = save_as

    def matches(self, stream):
        return self.pattern.matches(stream)

    def read_match(self, stream, match=None):
        


class SequencePattern(MacroPattern):
    def __init__(self, patterns):
        super().__init__()
        self.patterns = patterns

    def matches(self, stream):
        return all(pattern.matches(stream) for pattern in self.patterns)




