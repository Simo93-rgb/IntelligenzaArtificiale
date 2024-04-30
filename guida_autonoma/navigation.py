from classi import Outcome, Nodo
import random

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
METEO = "Meteo"
TERRENO = "Terreno"
GUASTO = "Guasto"
ACCURATEZZA_SENSORE = "Accuratezza_Sensore"
SENSORE_POSIZIONE = "Sensore_Posizione"
POSIZIONE = "Posizione"
COMANDO = "Comando"
COLOURS = ["\033[92m", "\033[93m", "\033[94m", "\033[95m"]
RESET_COLOUR = "\033[0m"


def change_evidence_and_update(net, node_id: str, outcome: Outcome = None) -> Outcome:
    """
        Modifica l'evidenza di un nodo nella rete e aggiorna le credenze della rete.

        Parametri:
            net (Network): L'oggetto della rete bayesiana.

            node_id (Nodo): Il nodo su cui modificare l'evidenza.

            outcome (Outcome, opzionale): Il risultato da impostare come evidenza. Se None, l'evidenza viene rimossa.

        Restituisce:
            None
        """
    if outcome:
        net.set_evidence(node_id, outcome.value)
    else:
        net.clear_evidence(node_id)
    net.update_beliefs()
    return outcome


def get_condition(net, temporal: int):
    t_str = f"_{str(temporal)}"
    pt_str = f"_{str(temporal - 1)}"
    if temporal == 0:
        change_evidence_and_update(net, METEO, Outcome.NORMALE)
        change_evidence_and_update(net, TERRENO, Outcome.NORMALE)
        change_evidence_and_update(net, GUASTO, Outcome.NO)
        print(f"\nSTART\nMeteo -> {Outcome.NORMALE.value}"
              f"\nTerreno -> {Outcome.NORMALE.value}"
              f"\nGuasto -> {Outcome.NO.value}"
              )
    elif temporal == 1:
        meteo = change_evidence_and_update(net, METEO + t_str, Outcome.NORMALE) \
            if random.random() <= 0.6667 \
            else change_evidence_and_update(net, METEO + t_str, Outcome.UMIDO)
        terreno = change_evidence_and_update(net, TERRENO + t_str, Outcome.NORMALE) \
            if random.random() <= 0.6667 \
            else change_evidence_and_update(net, TERRENO + t_str, Outcome.SCONNESSO)
        set_fault(net, meteo, terreno, t_str)
    else:
        meteo_precedente = Outcome(net.get_evidence_id(METEO + pt_str))
        terreno_precedente = Outcome(net.get_evidence_id(TERRENO + pt_str))
        fault_precedente = Outcome(net.get_evidence_id(GUASTO + pt_str))
        meteo = change_evidence_and_update(net, METEO + t_str, meteo_precedente) \
            if random.random() <= 0.6667 \
            else change_evidence_and_update(net, METEO + t_str, Outcome.UMIDO) \
            if meteo_precedente == Outcome.NORMALE \
            else change_evidence_and_update(net, METEO + t_str, Outcome.NORMALE)
        terreno = change_evidence_and_update(net, TERRENO + t_str, terreno_precedente) \
            if random.random() <= 0.6667 \
            else change_evidence_and_update(net, TERRENO + t_str, Outcome.SCONNESSO) \
            if terreno_precedente == Outcome.NORMALE \
            else change_evidence_and_update(net, TERRENO + t_str, Outcome.NORMALE)
        set_fault(net, Outcome(meteo), Outcome(terreno), t_str, fault_precedente)


def get_position(net, nodo: str, options: dict):
    print("Posizione rilevata?\n")
    for key, value in options.items():
        print(f"{key}. {value.value}")
    choice = input().strip()
    change_evidence_and_update(net, nodo, options.get(choice))


def set_action(net, nodo: str):
    valore_nodo = net.get_node_value(nodo)
    azione: Outcome = change_evidence_and_update(
        net,
        nodo,
        Outcome(net.get_outcome_id(nodo, valore_nodo.index(max(valore_nodo))))
    )
    print(f"{COLOURS[1]}Azione: {azione.value} direzione{RESET_COLOUR}\n") if azione == Outcome.MANTIENI \
        else print(f"{COLOURS[2]}Azione: Vai a {azione.value}{RESET_COLOUR}")


def set_fault(net, weather: Outcome, terrain: Outcome, temporal: str, fault: Outcome = Outcome.NO):
    if (weather == Outcome.UMIDO.value and random.random() <= 0.1
            or terrain == Outcome.SCONNESSO.value and random.random() <= 0.5
            or random.random() <= 0.1):
        fault = Outcome.YES.value
    print(f"Tempo {temporal[1:]}:\nMeteo -> {weather}\nTerreno -> {terrain}\nFault -> {fault}\n")
    change_evidence_and_update(net, GUASTO + temporal, fault)
