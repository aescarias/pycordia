import typing
import inspect
import datetime
import enum
import random


class Color:
    class BrandColor(enum.Enum):
        blurple = 0x5865F2
        green = 0x57F287
        yellow = 0xFEE75C
        fuchsia = 0xEB459E
        red = 0xED4245
        white = 0xFFFFFF
        black = 0x000000

    brand = BrandColor
    
    @classmethod
    def random(cls):
        """Generate random color as an integer for use with Discord"""
        return random.randint(0, 0xFFFFFF)


class BoolEnumKey:
    def __init__(self, name: str, value: typing.Any, is_set: bool):
        self.name = name
        self.value = value
        self.is_set = is_set

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f"<EnumKey{':set'*bool(self.is_set)} name='{self.name}' value={self.value}>"


class BoolEnum:
    def __new__(cls, **kwargs):       
        # Get defined class attributes

        attribs = {}

        init = object.__new__(cls)
       

        for name, value in inspect.getmembers(cls):
            # If member is not a routine (a function) and if it's not a dunder
            if not inspect.isroutine(value) and \
                not (name.startswith("__") and name.endswith("__")):    
                attribs[name] = value

        for name, value in kwargs.items():
            if name not in attribs:
                raise ValueError(f"'{name}' is not a valid keyword argument")
            
            if name in attribs and not isinstance(value, bool):
                raise ValueError(f"Argument '{name}' value must be of boolean form")
            
        for name, value in attribs.items():
            setattr(init, name, BoolEnumKey(name, value, kwargs.get(name, False)))

        return init

    def __setattr__(self, name, value):
        attr = getattr(self, name, None)
        if attr and isinstance(attr, BoolEnumKey):
            if isinstance(value, bool):
                attr.is_set = value
                return

            raise ValueError(f"'{name}' must have a value of boolean form")

        return object.__setattr__(self, name, value)

    def __iter__(self) -> typing.Iterator[BoolEnumKey]:
        return iter(value for _, value in inspect.getmembers(
            self, predicate=lambda member: isinstance(member, BoolEnumKey)
        ))


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

def obj_to_dict(obj: typing.Any, *, alias: dict = None, ignore_fields: list = None):
    """Convert an `obj` into a dictionary.
    
    Parameters:
        obj (typing.Any): The object to convert
        alias (dict): A dictionary containing aliases for any parts of the object. \
            Follows a (attribute-alias) pair
        ignore_fields (list): A list of attributes to ignore when converting
    """
    new_inf = {}
    if ignore_fields is None:
        ignore_fields = []
    
    if obj.__dict__:
        for key, value in obj.__dict__.items():
            if not key.startswith("_"):
                if key not in ignore_fields:
                    if alias and key in alias:
                        new_inf[alias[key]] = value
                    else:
                        new_inf[key] = value

    return new_inf        

def mutually_exclusive(*argument_names):
    def factory(fun):
        async def wrapper(*args, **kwargs):
            mutuals = []
            for kw in kwargs:
                if kw in argument_names:
                    mutuals.append(kw)

            if len(mutuals) > 1:
                raise Exception(f"Only one of this group {argument_names} can be provided at a time, found {len(mutuals)}.")

            return await fun(*args, **kwargs)
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

def add_ext(hash_: str):
    if hash_.startswith("a_"):
        return f'{hash_}.gif'
    return f'{hash_}.png'

def get_flag_list(enum_flag: enum.EnumMeta, integer: int):
    return [flag for flag in enum_flag if integer & flag.value == flag.value]  # type: ignore
