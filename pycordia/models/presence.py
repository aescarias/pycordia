from __future__ import annotations
from pycordia import api

import enum
import datetime


class StatusType(enum.Enum):
    online = "online"
    dnd = "dnd"
    idle = "idle"
    invisible = "invisible"
    offline = "offline"


class Presence:
    def __init__(self, *, 
        since: datetime.datetime, activities,
        status: StatusType, afk: bool = True    
    ):
        pass