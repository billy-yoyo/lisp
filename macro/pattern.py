from scope import UNKNOWN_VAR
import json
"""
patterns:
 - token pattern, matches a single token by type and/or content
 - 


examples:
(seq (read (token (type word)) as name) \( (read many (seq (read (ast value) into args) ,)) (read (ast value) into args) \))

"""

class MacroMatch:
    INTO = "into"
    AS = "as"

    def __init__(self):
        self.data = {}

    def get(self, name):
        if name in self.data:
            return self.data[name][1]
        return UNKNOWN_VAR

    def store_as(self, name, value):
        self.data[name] = (MacroMatch.AS, value)

    def store_into(self, name, value):
        if name not in self.data or self.data[name][0] != MacroMatch.INTO:
            self.data[name] = (MacroMatch.INTO, [])
        self.data[name][1].append(value)

    def merge(self, match):
        for key, entry in match.data.items():
            type, value = entry
            if type == MacroMatch.INTO:
                for sub_value in value:
                    self.store_into(key, sub_value)
            else:
                self.store_as(key, value)
        
    def __str__(self):
        data = {
            name: str(v) if f == MacroMatch.AS else [str(x) for x in v] for name, (f, v) in self.data.items()
        }
        return json.dumps(data)


class MacroPattern:
    def matches(self, stream):
        return False

    def read_match(self, stream):
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

    def read_match(self, stream):
        if self.matches(stream):
            return stream.last()
        return None

    def __str__(self):
        if self.name and self.content:
            return f"token({self.name}, `{self.content}`)"
        elif self.name:
            return f"token({self.name})"
        else:
            return f"token(`{self.content}`)"


class ASTPattern(MacroPattern):
    def __init__(self, name=None):
        super().__init__()
        self.name = name
        self._cached = None

    def matches(self, stream):
        self._cached = stream.attempt_parse(self.name)
        return self._cached is not None 

    def read_match(self, stream):
        if self.matches(stream):
            return self._cached
        return None

    def __str__(self):
        return f"ast({self.name})"


class ReadPattern(MacroPattern):
    MANY = "many"

    def __init__(self, pattern=None, flags=None, save_type=None, save_name=None):
        super().__init__()
        self.pattern = pattern
        self.flags = flags
        self.save_type = save_type
        self.save_name = save_name

        if save_name is not None and save_type not in [MacroMatch.INTO, MacroMatch.AS]:
            raise ValueError(f"save name specified without valid save type")

    def flag(self, name):
        return name in self.flags

    def matches(self, stream):
        return self.pattern.matches(stream)

    def read_single(self, stream):
        match = self.pattern.read_match(stream)
        if match is not None and self.save_name is not None:
            data = MacroMatch()

            if isinstance(match, MacroMatch):
                data.merge(match)
            elif self.save_type == MacroMatch.AS:
                data.store_as(self.save_name, match)
            elif self.save_type == MacroMatch.INTO:
                data.store_into(self.save_name, match)
            return data
        return match

    def read_match(self, stream):
        if self.flag(ReadPattern.MANY):
            data = MacroMatch()

            branch = stream.branch()
            match = self.read_single(branch)
            while match is not None:
                stream.merge(branch)
                if isinstance(match, MacroMatch):
                    data.merge(match)

                branch = stream.branch()
                match = self.read_single(branch)
            
            return data
        else:
            return self.read_single(stream)

    def __str__(self):
        return f"read({self.pattern})"




class SequencePattern(MacroPattern):
    def __init__(self, patterns):
        super().__init__()
        self.patterns = patterns

    def matches(self, stream):
        return all(pattern.matches(stream) for pattern in self.patterns)

    def read_match(self, stream):
        data = MacroMatch()
        for pattern in self.patterns:
            match = pattern.read_match(stream)
            if match is None:
                return None

            if isinstance(match, MacroMatch):
                data.merge(match)
        return data

    def __str__(self):
        return " ".join(str(p) for p in self.patterns)


