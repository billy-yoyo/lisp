
class Args:
    def __init__(self, positional, keyword):
        self.positional = positional
        self.keywords = keyword

    def __getattr__(self, name):
        return self.keywords[name.replace("_", "-")]

    def __getitem__(self, item):
        return self.positional[item]

    def __len__(self):
        return len(self.positional)

    def __iter__(self):
        return iter(self.positional)


class ArgProc:
    def __init__(self):
        self.parameter_short_name_map = {}
        self.parameter_full_names = []
        self.parameter_defaults = {}

    def add_parameter(self, full_name, short_name, default=None):
        self.parameter_full_names.append(full_name)
        self.parameter_short_name_map[short_name] = full_name
        self.parameter_defaults[full_name] = default

    def _ensure_parameter_name_correct(self, name, is_full=True):
        if (is_full and name not in self.parameter_full_names) or (not is_full and name not in self.parameter_short_name_map):
            raise KeyError(f"invalid parameter name {name}")

    def read(self, args):
        positional = []
        keywords = self.parameter_defaults.copy()
        buffered_parameter = None
        for arg in args:
            if buffered_parameter is not None:
                keywords[buffered_parameter] = arg
                buffered_parameter = None
            elif arg.startswith("--"):
                if "=" in arg:
                    arg_split = arg[2:].split("=")
                    arg_name = arg_split[0]
                    arg_value = "=".join(arg_split[1:])

                    self._ensure_parameter_name_correct(arg_name)
                    keywords[arg_name] = arg_value
                else:
                    arg_name = arg[2:]
                    self._ensure_parameter_name_correct(arg_name)
                    if self.parameter_defaults[arg_name] is False:
                        keywords[arg_name] = True
                    else:
                        buffered_parameter = arg[2:]
            elif arg.startswith("-"):
                if "=" in arg:
                    arg_split = arg[1:].split("=")
                    short_arg_name = arg_split[0]
                    arg_value = "=".join(arg_split[1:])

                    self._ensure_parameter_name_correct(short_arg_name, is_full=False)
                    keywords[self.parameter_short_name_map[short_arg_name]] = arg_value
                else:
                    short_arg_name = arg[1:]
                    self._ensure_parameter_name_correct(short_arg_name, is_full=False)
                    arg_name = self.parameter_short_name_map[short_arg_name] 
                    if self.parameter_defaults[arg_name] is False:
                        keywords[arg_name] = True
                    else:
                        buffered_parameter = arg_name
            else:
                positional.append(arg)
        return Args(positional, keywords)