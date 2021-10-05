import pycordia
import enum

class InteractionType(enum.Enum):
    ping = 1
    application_command = 2
    message_component = 3


class InteractionData:
    def __init__(self, data: dict) -> None:
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.type: int = data["type"]


class Interaction:
    def __init__(self, data: dict) -> None:
        self.id: str = data["id"]
        self.application_id = data
        self.type = InteractionType(data["type"])
        