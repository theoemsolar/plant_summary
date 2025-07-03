from dataclasses import dataclass
from datetime import datetime


@dataclass
class Inverter:
    id: int
    fsp: int
    date: datetime
    value: float
