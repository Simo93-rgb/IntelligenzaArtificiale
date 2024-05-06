from enum import Enum, auto


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
    SCONNESSO = "sconnesso"
    YES = "yes"
    NO = "no"


class Nodo():
    METEO = "Meteo"
    TERRENO = "Terreno"
    GUASTO = "Guasto"
    ACCURATEZZA_SENSORE = "Accuratezza_Sensore"
    SENSORE_POSIZIONE = "Sensore_Posizione"
    POSIZIONE = "Posizione"
    COMANDO = "Comando"



class TipoNodo(Enum):
    DECISION = 17
    CHANCE = 18
