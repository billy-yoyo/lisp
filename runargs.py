import sys

class RunArgs:
    def __init__(self, args, shorthands=None):
        shorthands = shorthands or {}

        self.positional = []
        self.named = {}

        i = 0
        while i < len(args):
            arg = args[i]
            if arg.startswith("-"):
                name, value = arg, None
                if "=" in arg:
                    spl = arg.split("=")
                    name, value = spl[0], "=".join(spl[1:])
                
                if name.startswith("--"):
                    name = name[2:]
                else:
                    shorthand = name[1:]
                    if shorthand not in shorthands:
                        name = shorthand
                    else:
                        name = shorthands[shorthand]
                
                if value is None:
                    value = args[i + 1]
                    i += 1
                
                self.named[name] = value
            else:
                self.positional.append(arg)
            i += 1

def run_args(shorthands=None):
    return RunArgs(sys.argv[1:], shorthands=shorthands)