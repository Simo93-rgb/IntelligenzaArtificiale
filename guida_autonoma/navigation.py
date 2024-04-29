from classi import Outcome, Nodo
import random

from prototipo.decision_process import change_evidence_and_update


def get_condition(net, temporal: int):
    t_str = f"_{str(temporal)}"
    pt_str = f"_{str(temporal - 1)}"
    if temporal == 0:
        change_evidence_and_update(net, Nodo.METEO, Outcome.NORMALE)
        change_evidence_and_update(net, Nodo.TERRENO, Outcome.NORMALE)
        change_evidence_and_update(net, Nodo.GUASTO, Outcome.NO)
        print(f"\nSTART\nMeteo -> {Outcome.NORMALE.value}"
              f"\nTerreno -> {Outcome.NORMALE.value}"
              f"\nGuasto -> {Outcome.NO.value}"
              )
    elif temporal == 1:
        meteo = change_evidence_and_update(net, Nodo.METEO + t_str, Outcome.NORMALE) \
            if random.random() <= 0.6667 \
            else change_evidence_and_update(net, Nodo.METEO + t_str, Outcome.UMIDO.value)
        terreno = change_evidence_and_update(net, Nodo.TERRENO + t_str, Outcome.NORMALE) \
            if random.random() <= 0.6667 \
            else change_evidence_and_update(net, Nodo.TERRENO + t_str, Outcome.SCONNESSO)
        set_fault(net, meteo, terreno, t_str)
    else:
        meteo_precedente = Outcome(net.get_evidence_id(Nodo.METEO + pt_str))
        terreno_precedente = Outcome(net.get_evidence_id(Nodo.TERRENO + pt_str))
        fault_precedente = Outcome(net.get_evidence_id(Nodo.GUASTO + pt_str))
        meteo = change_evidence_and_update(net, Nodo.METEO + t_str, meteo_precedente) \
            if random.random() <= 0.6667 \
            else change_evidence_and_update(net, Nodo.METEO + t_str, Outcome.UMIDO.value) \
            if meteo_precedente == Outcome.NORMALE \
            else change_evidence_and_update(net, Nodo.METEO + t_str, Outcome.NORMALE)
        terreno = change_evidence_and_update(net, Nodo.TERRENO + t_str, terreno_precedente) \
            if random.random() <= 0.6667 \
            else change_evidence_and_update(net, Nodo.TERRENO + t_str, Outcome.SCONNESSO) \
            if terreno_precedente == Outcome.NORMALE \
            else change_evidence_and_update(net, Nodo.TERRENO + t_str, Outcome.NORMALE)
        set_fault(net, meteo, terreno, t_str, fault_precedente)


def get_position(net, t):
    print("qualcosa")


def set_action(net, t):
    print("qualcosa")


def set_fault(net, weather: Outcome, terrain: Outcome, temporal: str, fault: Outcome = Outcome.NO.value):
    if (weather == Outcome.UMIDO.value and random.random() <= 0.1
            or terrain == Outcome.SCONNESSO.value and random.random() <= 0.5
            or random.random() <= 0.1):
        fault = Outcome.YES.value
    print(f"Tempo {temporal[1:]}:\nMeteo -> {weather}\nTerreno -> {terrain}\nFault -> {fault}\n")
    change_evidence_and_update(net, Nodo.GUASTO.value + temporal, fault)
