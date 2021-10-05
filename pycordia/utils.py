import typing
import inspect
import datetime

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

def mutually_exclusive(*argument_names):
    def factory(fun):
        def wrapper(*args, **kwargs):
            mutuals = []
            for kw in kwargs:
                if kw in argument_names:
                    mutuals.append(kw)

            if len(mutuals) > 1:
                raise Exception(f"Only one of this group {argument_names} can be provided at a time, found {len(mutuals)}.")

            fun(*args, **kwargs)
        return wrapper
    return factory

def snowflake_to_date(snowflake: int) -> datetime.datetime:
    """Converts a snowflake to a valid `datetime.datetime` object

    Args:
        snowflake (int): A valid snowflake
    
    Returns: `datetime.datetime`
    """
    
    # The algorithm applied is the same as documented in
    # https://discord.com/developers/docs/reference

    # (snowflake >> 22) + Discord Epoch
    ms = (snowflake >> 22) + 1420070400000
    
    # Divided by 1000 and then provided to datetime.datetime
    return datetime.datetime.utcfromtimestamp(ms / 1000)

def make_optional(callable: typing.Callable, *args, **kwargs) -> typing.Optional[typing.Any]:
    """Return the result of `callable` if `args` or `kwargs` evaluate to True, else None

    Args:
        callable (typing.Callable): A callable object
    """
    if any(bool(arg) for arg in args) or \
        any(bool(kwargs[kwarg]) for kwarg in kwargs):
        return callable(*args, **kwargs)

