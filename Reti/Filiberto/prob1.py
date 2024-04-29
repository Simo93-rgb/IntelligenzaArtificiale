import pysmile
import pysmile_license

NO = "No"
YES = "Sì"

RES = ['n', 'N', '1', 's', 'S', '2']
RES_NO = RES[:3]
RES_YES = RES[3:]

PROD = "Produzione"
PROF = "Profitto"
PROT = "Sviluppo_prototipo"
QLT = "Qualità"
MRKT = "Ricerca_di_marketing"
MRKT_RES = "Risultato_ricerca_di_mercato"

NO_RES = "Nessun_risultato"


# Print expected utility in a node
def print_eu(net, node_name):
    print(f"\nUtilità attesa per {node_name.replace('_', ' ')}:")
    node_value = net.get_node_value(node_name)
    for i, v in enumerate(node_value):
        print(net.get_outcome_id(node_name, i), "=", '{0:.2f}'.format(v))

    if node_name == PROD:
        update_evidence(net, node_name, YES)

        print("\nLe probabilità di profitto sono le seguenti:")
        prof_prob = net.get_node_value(PROF)
        for i, v in enumerate(prof_prob):
            print(net.get_outcome_id(PROF, i), "=", '{0:.2f}%'.format(v * 100))

        print("\033[1m\033[32m\nSi consiglia di proseguire la produzione\033[0m\033[1m") \
            if net.get_outcome_id(node_name, node_value.index(max(node_value))) == YES \
            else print("\033[1m\033[31m\nSi consiglia di fermare la produzione\033[0m\033[1m")


# Update evidence in a node
def update_evidence(net, node_name, evidence):
    net.set_evidence(node_name, evidence) if evidence else net.clear_evidence(node_name)
    net.update_beliefs()
    return evidence


# Get user choice
def set_decision(net, node_name):
    print_eu(net, node_name)

    res = " "
    while res[0] not in RES:
        res = input(f"\nVuoi effettuare {node_name.replace('_', ' ')}?"
                    f"\n1) No\n2) Sì\nRisposta: ")

    return update_evidence(net, node_name, NO) if res[0] in RES_NO else update_evidence(net, node_name, YES)


# Set result of a previous choice
def set_result(net, node_name):
    printable_name = node_name.replace('_', ' ')

    if node_name == QLT:
        res = " "
        while res[0] not in RES:
            res = input("\nHai un prototipo da valutare?"
                        "\n1) No\n2) Sì\nRisposta: ")
        if res[0] in RES_NO:
            return
        else:
            print(f"\n{printable_name} ottenuta?")
    else:
        print(f"\n{printable_name} ottenuto?")

    node_value = net.get_node_value(node_name)

    if node_name == MRKT_RES:
        node_value = node_value[1:]
        net.delete_outcome(node_name, 0)

    for i, v in enumerate(node_value):
        print(f"{i + 1}) {net.get_outcome_id(node_name, i).replace('_', ' ')}")

    res = 0
    while not int(res) in range(1, len(node_value) + 1):
        res = input("Risposta: ")
        res = 0 if not res.isdigit() else int(res)

    update_evidence(net, node_name, net.get_outcome_id(node_name, res - 1))


network = pysmile.Network()
network.read_file("xdsl/prob1.xdsl")
network.update_beliefs()

if set_decision(network, MRKT) == YES:
    set_result(network, MRKT_RES)

if set_decision(network, PROT) == YES:
    set_result(network, QLT)

print_eu(network, PROD)
