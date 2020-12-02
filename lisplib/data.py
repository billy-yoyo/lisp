

def lisp_arr(scope, args):
    return [scope.execute_statement(arg) for arg in args]

def lisp_dict(scope, args):
    data = {}
    for arg in args:
        if len(arg.args) != 2:
            raise ValueError("each entry must be key/object pair")

        key, value = [scope.execute_statement(item) for item in arg.args]
        if not isinstance(key, int) and not isinstance(key, str):
            raise ValueError("key must be an int or string")

        data[key] = value
    return data 

def lisp_obj(scope, args):
    data = object()
    for arg in args:
        if len(arg.args) != 2:
            raise ValueError("each entry must be key/object pair")

        key, value = arg.args

        if key.type != "word" and key.type != "string":
            raise ValueError("key must be a word or string")
        else:
            key = key.value

        value = scope.execute_statement(value)
        setattr(key, value)
    return data

NATIVES = {
    "arr": lisp_arr,
    "dict": lisp_dict,
    "obj": lisp_obj
}
