from enum import Enum


class Plant(Enum):
    SEGREDO = "segredo"
    SANTO_ANTONIO = "santo_antonio"
    SARANDI = "sarandi"


PLANT_URLS = {
    Plant.SEGREDO: "https://oemsolarfsg.loca.lt",
    Plant.SANTO_ANTONIO: "https://oemsolarfsp.loca.lt",
}
