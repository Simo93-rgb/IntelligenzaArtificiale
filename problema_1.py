import pysmile
import pysmile_license
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


def print_node_utility(net, node_id: Nodo):
    colours = ["\033[92m", "\033[93m", "\033[94m", "\033[95m"]
    reset_colour = "\033[0m"

    node = net.get_node_value(node_id.value)
    print(f"Utilità attese di {node_id.value.replace('_', ' ').title()}:")

    for i, value in enumerate(node):
        color = colours[i % len(colours)]  # Cicla attraverso i colori se ci sono più valori degli indici
        outcome_id = net.get_outcome_id(node_id.value, i)
        formatted_value = round(value, 3)
        print(f"{color}{outcome_id}={formatted_value}{reset_colour}")
    print("\n")


def change_evidence_and_update(net, node_id: Nodo, outcome: Outcome = None):
    if outcome:
        net.set_evidence(node_id.value, outcome.value)
    else:
        net.clear_evidence(node_id.value)
    net.update_beliefs()


def user_choice(prompt: str, options: dict, net, node_id: Nodo) -> str:
    print_node_utility(net, node_id)
    print(prompt)
    for key, value in options.items():
        print(f"{key}. {value}")
    choice = input().strip()
    return options.get(choice, "Invalid choice")


def set_user_defined_evidence(net, node_id: Nodo, outcome_dict: dict, prompt: str):
    choice = user_choice(prompt, outcome_dict, net, node_id)
    if choice != "Invalid choice":
        change_evidence_and_update(net, node_id, Outcome[choice])
    else:
        print("Invalid input. No changes made.")


def decision_process(net):
    options = {"1": "YES", "2": "NO"}
    market_research = user_choice("Vuoi effettuare la ricerca di mercato?", options, net, Nodo.RICERCA)
    if market_research == "YES":
        change_evidence_and_update(net, Nodo.RICERCA, Outcome.YES)
        market_demand_options = {"1": "LOW", "2": "HIGH"}
        set_user_defined_evidence(net, Nodo.DOMANDA, market_demand_options,
                                  "Qual è il risultato della ricerca di mercato?")
    elif market_research == "NO":
        change_evidence_and_update(net, Nodo.RICERCA, Outcome.NO)
        change_evidence_and_update(net, Nodo.DOMANDA, Outcome.NOTHING)

    prototype_decision = user_choice("Vuoi prototipare?", options, net, Nodo.PROTOTIPAZIONE)
    if prototype_decision == "YES":
        change_evidence_and_update(net, Nodo.PROTOTIPAZIONE, Outcome.YES)
        # product_quality_options = {"1": "STANDARD", "2": "HIGH"}
        # set_user_defined_evidence(net, Nodo.QUALITY, product_quality_options, "Come cambia la qualità?")
    elif prototype_decision == "NO":
        change_evidence_and_update(net, Nodo.PROTOTIPAZIONE, Outcome.NO)
        change_evidence_and_update(net, Nodo.QUALITY, Outcome.STANDARD)

    production_decision = user_choice("Vuoi produrre?", options, net, Nodo.PRODUZIONE)
    if production_decision == "YES":
        change_evidence_and_update(net, Nodo.PRODUZIONE, Outcome.YES)
    elif production_decision == "NO":
        change_evidence_and_update(net, Nodo.PRODUZIONE, Outcome.NO)


def main():
    net = pysmile.Network()
    net.read_file("Reti/problema_1.xdsl")
    net.update_beliefs()

    decision_process(net)

    print("Utilità attesa finale")
    print_node_utility(net, Nodo.PROFITTO)


# Uncomment before running
main()
