from pycordia import errors, utils
import typing
import enum


class ComponentType(enum.Enum):
    action_row = 1
    button = 2
    select_menu = 3


class ButtonStyles(enum.Enum):
    primary = 1
    secondary = 2
    success = 3
    danger = 4
    link = 5


class SelectMenuOption:
    def __init__(self, *, label: str, value: str, 
        description: str = None, emoji: dict = None, 
        default: bool = False
    ) -> None:
        self.label = label
        self.value = value
        self.description = description
        self.emoji = emoji
        self.default = default

    @classmethod
    def from_json(cls, data: dict):
        return utils.obj_from_dict(data, cls)

    def to_json(self):
        return utils.obj_to_dict(self)

    


class SelectMenu:
    def __init__(self, *, custom_id: str, placeholder: str = None, 
        min_values: int = 1, max_values: int = 1, disabled: bool = False
    ) -> None:
        pass


class Button:
    def __init__(self, *, custom_id: str = None, disabled: bool = False, 
        style: ButtonStyles, label: str, emoji = None, url: str = None
    ) -> None:
        self.__on_click_func = None

        self.custom_id = custom_id
        self.disabled = disabled
        self.style = style
        self.label = label
        self.emoji = emoji 
        self.url = url

        self.__verify_component()

    @classmethod
    def from_json(cls, data: dict):
        obj = utils.obj_from_dict(data, cls)
        obj.style = ComponentType(obj.style)
        return obj

    def to_json(self):
        obj = utils.obj_to_dict(self)
        obj["type"] = ComponentType.button.value
        obj["style"] = obj["style"].value
        return obj
    
    def __verify_component(self):
        if self.url and self.custom_id:
            raise errors.ComponentError(
                "A link button cannot have a custom ID."
            )
        elif not self.custom_id:
            raise errors.ComponentError(
                "Non-link buttons must contain a custom ID"
            )

    def on_click(self, fun):
        self.__on_click_func = fun 
        def wrapper():
            fun()
        return wrapper


# class ActionRow:
#     def __init__(self, *components: typing.List[typing.Union[SelectMenu, Button]]):
#         self.__verify_components(components)
        
#         self.component_type = ComponentType.action_row
#         self.__components = [*components]

#     @classmethod
#     def from_list(cls, data: list):
#         comps = []
#         for elem in data:
#             comp_type = int(elem["type"])
#             if comp_type == ComponentType.action_row.value:
#                 raise errors.ComponentError(
#                     "An ActionRow cannot contain another ActionRow"
#                 )
#             elif comp_type == ComponentType.button.value:
#                 comps.append(Button(**elem))
#             elif comp_type == ComponentType.

#         return ActionRow(*comps)

#     @property
#     def components(self):
#         return self.__components

#     def __verify_components(self, components):
#         for comp in components:
#             if isinstance(comp, ActionRow):
#                 raise errors.ComponentError(
#                     "An ActionRow cannot contain another ActionRow"
#                 )