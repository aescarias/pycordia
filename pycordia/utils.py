import typing
import inspect

def obj_from_dict(data: dict, obj: typing.Callable, alias: dict = None):
    """Convert a dictionary `data` into an `obj`.
    
    Parameters:
        data (dict): The data to provide.
        obj (typing.Callable): The object created from `data`
        alias (dict): A dictionary containing aliases for any parts of the dictionary. \
            Follows a (param-alias) pair
    """
    sig = inspect.signature(obj)
    new_inf = {}
    for param in sig.parameters:
        if alias and param in alias:
            new_inf[param] = data[alias[param]]
        elif param in data:    
            new_inf[param] = data[param]

    return obj(**new_inf)

def obj_to_dict(obj: typing.Any, alias: dict = None):
    """Convert an `obj` into a dictionary.
    
    Parameters:
        obj (typing.Any): The object to convert
        alias (dict): A dictionary containing aliases for any parts of the object. \
            Follows a (attribute-alias) pair
    """
    new_inf = {}
    if obj.__dict__:
        for key, value in obj.__dict__.items():
            if not key.startswith("_"):
                if alias and key in alias:
                    new_inf[alias[key]] = value
                else:
                    new_inf[key] = value

    return new_inf        
