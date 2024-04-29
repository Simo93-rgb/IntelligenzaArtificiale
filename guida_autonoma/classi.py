from enum import Enum


class Outcome(Enum):
    SINISTRA = "sinistra"
    DESTRA = "destra"
    MANTIENI = "mantieni"
    CENTRO = "centro"
    PESSIMA = "pessima"
    BUONA = "buona"
    OTTIMA = "ottima"
    NORMALE = "normale"
    UMIDO = "umido"
    SCONNESSO = "sconesso"
    YES = "yes"
    NO = "no"


class Nodo(Enum):
    METEO = "Meteo"
    TERRENO = "Terreno"
    GUASTO = "Guasto"
    ACCURATEZZA_SENSORE = "Accuratezza_Sensore"
    SENSORE_POSIZIONE = "Sensore_Posizione"
    POSIZIONE = "Posizione"
    COMANDO = "Comando"

    def __add__(self, other):
        return Nodo(self.value + other.value)


class TipoNodo(Enum):
    DECISION = 17
    CHANCE = 18
