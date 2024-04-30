from classi import Outcome, Nodo, TipoNodo


def print_node_utility(net, node_id: Nodo):
    """
        Stampa l'utilità attesa per un dato nodo nella rete bayesiana.

        Parametri:
            net (Network): L'oggetto della rete bayesiana.

            node_id (Nodo): L'identificativo del nodo di cui si vogliono visualizzare le utilità.

        Restituisce:
            None
        """
    colours = ["\033[92m", "\033[93m", "\033[94m", "\033[95m"]
    reset_colour = "\033[0m"

    node = net.get_node_value(node_id.value)
    node_type: TipoNodo = net.get_node_type(node_id.value)
    if node_type == TipoNodo.DECISION.value:
        print(f"\nUtilità attese di {node_id.value.replace('_', ' ').title()}:")
    elif node_type == TipoNodo.CHANCE.value:
        print(f"\nLe probabilià di {node_id.value.replace('_', ' ').title()} sono:")

    for i, value in enumerate(node):
        color = colours[i % len(colours)]
        outcome_id = net.get_outcome_id(node_id.value, i)
        formatted_value = round(value, 3)
        print(f"{color}{outcome_id}={formatted_value}{reset_colour}")


def change_evidence_and_update(net, node_id: Nodo, outcome: Outcome = None) -> Outcome:
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
        net.set_evidence(node_id.value, outcome.value)
    else:
        net.clear_evidence(node_id.value)
    net.update_beliefs()
    return outcome


def user_choice(prompt: str, options: dict, net, node_id: Nodo) -> str:
    """
        Visualizza una domanda all'utente, stampa l'utilità del nodo specificato, e cattura la scelta dell'utente.

        Parametri:
            prompt (str): Il messaggio da visualizzare all'utente.

            options (dict): Un dizionario delle opzioni disponibili per l'utente.

            net (Network): L'oggetto della rete bayesiana.

            node_id (Nodo): Il nodo di cui visualizzare l'utilità.

        Restituisce:
            str: La scelta dell'utente o "Invalid choice" se la scelta non è valida.
        """
    print_node_utility(net, node_id)
    print(prompt)
    for key, value in options.items():
        print(f"{key}. {value}")
    choice = input().strip()
    return options.get(choice, "Invalid choice")


def set_user_defined_evidence(net, node_id: Nodo, outcome_dict: dict, prompt: str):
    """
        Chiede all'utente di definire l'evidenza per un nodo specifico e la imposta nella rete.

        Parametri:
            net (Network): L'oggetto della rete bayesiana.

            node_id (Nodo): Il nodo per il quale impostare l'evidenza.

            outcome_dict (dict): Un dizionario che mappa le scelte dell'utente ai risultati possibili.

            prompt (str): Il messaggio da visualizzare per chiedere all'utente di scegliere.

        Restituisce:
            None
        """
    choice = user_choice(prompt, outcome_dict, net, node_id)
    if choice != "Invalid choice":
        change_evidence_and_update(net, node_id, Outcome[choice])
    else:
        print("Invalid input. No changes made.")


def decision_process(net):
    """
        Gestisce il processo decisionale dell'utente per modificare le evidenze nella rete e visualizzare le utilità.

        Parametri:
            net (Network): L'oggetto della rete bayesiana.

        Restituisce:
            None
        """
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
        is_there_prototype = user_choice("Il prototipo c'è?", options, net, Nodo.QUALITY)
        if is_there_prototype == "YES":
            product_quality_options = {"1": "STANDARD", "2": "HIGH"}
            set_user_defined_evidence(net, Nodo.QUALITY, product_quality_options, "Come cambia la qualità?")
        else:
            print("La qualità sarà robabilistica con: \n * HIGH -> 85%\n * STANDARD -> 15%")
    elif prototype_decision == "NO":
        change_evidence_and_update(net, Nodo.PROTOTIPAZIONE, Outcome.NO)
        change_evidence_and_update(net, Nodo.QUALITY, Outcome.STANDARD)

    production_decision = user_choice("Vuoi produrre?", options, net, Nodo.PRODUZIONE)
    if production_decision == "YES":
        change_evidence_and_update(net, Nodo.PRODUZIONE, Outcome.YES)
    elif production_decision == "NO":
        change_evidence_and_update(net, Nodo.PRODUZIONE, Outcome.NO)
