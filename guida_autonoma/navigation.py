import sys
import pysmile
from classi import Outcome
import random

METEO = "Meteo"
TERRENO = "Terreno"
GUASTO = "Guasto"
ACCURATEZZA_SENSORE = "Accuratezza_Sensore"
SENSORE_POSIZIONE = "Sensore_Posizione"
POSIZIONE = "Posizione"
COMANDO = "Comando"
COLOURS = ["\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]
RESET_COLOUR = "\033[0m"
PROB_TERRENO = (5 / 7)
PROB_METEO = (2 / 3)


def print_node_utility(net, node_id: str):
    """
        Stampa l'utilità attesa per un dato nodo nella rete bayesiana.

        Parametri:
            net (Network): L'oggetto della rete bayesiana.

            node_id (Nodo): L'identificativo del nodo di cui si vogliono visualizzare le utilità.

        Restituisce:
            None
        """
    reset_colour = "\033[0m"

    node = net.get_node_value(node_id)
    print(f"\nUtilità attese di {node_id.replace('_', ' ').title()}:")

    for i, value in enumerate(node):
        color = COLOURS[i % len(COLOURS)]
        outcome_id = net.get_outcome_id(node_id, i)
        formatted_value = round(value, 3)
        print(f"{color}{outcome_id}={formatted_value}{reset_colour}")


def change_evidence_and_update(net, node_id: str, outcome: Outcome = None) -> Outcome:
    """
    Modifica l'evidenza di un nodo nella rete e aggiorna le credenze della rete.

    Args:
        net (Network): L'oggetto della rete bayesiana.
        node_id (str): Il nodo su cui modificare l'evidenza.
        outcome (Outcome, optional): Il risultato da impostare come evidenza. Se None, l'evidenza viene rimossa.

    Returns:
        Outcome: Il risultato passato per argomento, utilizzato per ulteriori logiche.
    """
    if outcome:
        net.set_evidence(node_id, outcome.value)
    else:
        net.clear_evidence(node_id)
    net.update_beliefs()
    return outcome


def get_condition(net, temporal: int) -> None:
    """
    Recupera e modifica le condizioni della rete basate sul tempo specificato.

    Args:
        net (BayesianNetwork): L'oggetto della rete bayesiana.
        temporal (int): Il tempo specificato per il quale ottenere le condizioni.

    Returns:
        None
    """
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
            if random.random() <= PROB_METEO \
            else change_evidence_and_update(net, METEO + t_str, Outcome.UMIDO)
        terreno = change_evidence_and_update(net, TERRENO + t_str, Outcome.NORMALE) \
            if random.random() <= PROB_TERRENO \
            else change_evidence_and_update(net, TERRENO + t_str, Outcome.SCONNESSO)
        set_fault(net, meteo, terreno, t_str)
    else:
        meteo_precedente = Outcome(net.get_evidence_id(METEO + pt_str))
        terreno_precedente = Outcome(net.get_evidence_id(TERRENO + pt_str))
        fault_precedente = Outcome(net.get_evidence_id(GUASTO + pt_str))
        meteo = change_evidence_and_update(net, METEO + t_str, meteo_precedente) \
            if random.random() <= PROB_METEO \
            else change_evidence_and_update(net, METEO + t_str, Outcome.UMIDO) \
            if meteo_precedente == Outcome.NORMALE \
            else change_evidence_and_update(net, METEO + t_str, Outcome.NORMALE)
        terreno = change_evidence_and_update(net, TERRENO + t_str, terreno_precedente) \
            if random.random() <= PROB_TERRENO \
            else change_evidence_and_update(net, TERRENO + t_str, Outcome.SCONNESSO) \
            if terreno_precedente == Outcome.NORMALE \
            else change_evidence_and_update(net, TERRENO + t_str, Outcome.NORMALE)
        set_fault(net, Outcome(meteo), Outcome(terreno), t_str, fault_precedente)


def get_position(net, nodo: str, options: dict) -> None:
    """
        Rileva e modifica l'evidenza di posizione del nodo specificato in base all'input dell'utente.

        Args:
            net (BayesianNetwork): L'oggetto della rete bayesiana.
            nodo (str): Il nodo per cui la posizione deve essere determinata.
            options (dict): Un dizionario delle possibili posizioni che l'utente può scegliere.

        Returns:
            None
        """
    print("Posizione rilevata?\n")
    for key, value in options.items():
        print(f"{key}. {value.value}")
    try:
        choice = input("Inserisci il numero: ").strip()
        if options.get(choice) is None:
            raise KeyError("Opzione non valida")
        change_evidence_and_update(net, nodo, options.get(choice))
    except KeyError as e:
        print(e)
        sys.exit("Terminazione a causa di KeyError")


def set_action(net, nodo: str) -> None:
    """
        Determina e stampa l'azione ottimale per il nodo specificato basata sul valore più alto di probabilità del nodo.

        Args:
            net (BayesianNetwork): L'oggetto della rete bayesiana.
            nodo (str): Il nodo per cui l'azione deve essere determinata.

        Returns:
            None
        """
    valore_nodo = net.get_node_value(nodo)
    print_node_utility(net, nodo)
    azione: Outcome = change_evidence_and_update(
        net,
        nodo,
        Outcome(net.get_outcome_id(nodo, valore_nodo.index(max(valore_nodo))))
    )
    print(f"{COLOURS[4]}Azione: {azione.value} direzione{RESET_COLOUR}\n") \
        if azione == Outcome.MANTIENI \
        else print(f"{COLOURS[4]}Azione: Vai a {azione.value}{RESET_COLOUR}")


def set_fault(net, weather: Outcome, terrain: Outcome, temporal: str, fault: Outcome = Outcome.NO) -> None:
    """
    Determina e imposta una condizione di guasto basata sul meteo e sul terreno.

    Args:
        net (BayesianNetwork): La rete bayesiana in uso.
        weather (Outcome): L'ultima evidenza meteo impostata.
        terrain (Outcome): L'ultima evidenza terreno impostata.
        temporal (str): Stringa temporale per identificare il tempo corrente.
        fault (Outcome, optional): L'ultima condizione di guasto, di default a 'NO'.

    Returns:
        None
    """
    if (weather == Outcome.UMIDO.value and random.random() <= 0.1
            or terrain == Outcome.SCONNESSO.value and random.random() <= 0.5
            or random.random() <= 0.1):
        print("Si è verificato un guasto")
        sys.exit("Terminazione del programma a causa del sensore rotto")
    print(f"Tempo {temporal[1:]}:\nMeteo -> {weather}\nTerreno -> {terrain}\nFault -> {fault}\n")
    change_evidence_and_update(net, GUASTO + temporal, fault)
