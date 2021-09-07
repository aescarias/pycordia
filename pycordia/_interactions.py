import aiohttp
import enum
from .models.message import Member
from typing import Optional

class AppCommandOptionTypes(enum.Enum):
    sub_command = 1
    sub_command_group = 2
    string = 3
    integer = 4
    boolean = 5
    user = 6
    channel = 7
    role = 8
    mentionable = 9
    number = 10

class AppCommandInteractionDataOption:
    def __init__(self, data: dict):
        self.name: str = data["name"]
        self.command_type = AppCommandOptionTypes(int(data["type"]))
        self.value: Optional[str] = data.get("value")
        self.options = data.get("options", [])

    def add_option(self, *, name: str, value: str, command_type):
        self.options.append(AppCommandInteractionDataOption(
            {
                "name": name,
                "value": value,
                "type": command_type
            }
        ))


class AppCommandOption:
    def __init__(self, data: dict):
        self.option_type = AppCommandOptionTypes(data["type"])
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.required: bool = data.get("required", False)
        self.choices: list = data.get("choices", [])
        self.options: list = data.get("options", [])

    def add_choice(self, *, name: str, value: str):
        self.choices.append({
            "name": name,
            "value": value
        })
    
    def add_option(self, *, option_type, name: str, description: str, required: bool = False):
        self.options.append(AppCommandOption(
            {
                "type": option_type,
                "name": name,
                "description": description,
                "required": required
            }
        ))


class AppCommand:
    class CommandTypes(enum.Enum):
        chat_input = 1
        user = 2
        message = 3

    def __init__(self, data: dict):
        CommandType = AppCommand.CommandTypes

        self.user_id: str = data["id"]
        if data.get("type"):
            self.command_type: Optional[CommandType] = CommandType(data["type"])
        else:
            self.command_type: Optional[CommandType] = None
        self.application_id: str = data["application_id"]
        self.guild_id: Optional[str] = data.get("guild_id")
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.default_permission: bool = data.get("default_permissions", True)


class InteractionClient:
    registered_commands = {

    }
    @classmethod
    def slash_command(cls, *, name: str):
        def command(func):
            cls.registered_commands[name] = func
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return command


# interact = InteractionClient()

# @interact.slash_command(
#     name="blep", description="Send a random adorable animal photo",
#     options=[AppCommandOption]
# )
# async def blep(*args, **kwargs):
#     print(args, kwargs)


