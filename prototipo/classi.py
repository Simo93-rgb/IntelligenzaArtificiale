from enum import Enum

0
class Outcome(Enum):
    YES = "yes"
    NO = "no"
    LOW = "low"
    HIGH = "high"
    NOTHING = "nothing"
    STANDARD = "standard"


class Nodo(Enum):
    PROFITTO = "profitto"
    RICERCA = "ricerca_di_mercato"
    DOMANDA = "domanda_stimata_di_mercato"
    PROTOTIPAZIONE = "prototipazione"
    QUALITY = "qualita_prodotto"
    PRODUZIONE = "produzione"

class TipoNodo(Enum):
    DECISION = 17
    CHANCE = 18