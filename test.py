value = "a"
if type(value) is not int:
    raise Exception(f"'{value.__class__.__name__}' has to an integer")
