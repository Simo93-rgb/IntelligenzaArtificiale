from enum import Enum


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
