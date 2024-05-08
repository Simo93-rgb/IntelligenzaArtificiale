import pysmile
from licenze import pysmile_license
from classi import Nodo
from decision_process import decision_process, print_node_utility

COLOUR = "\033[91m"
RESET_COLOUR = "\033[0m"

if __name__ == "__main__":
    net = pysmile.Network()
    net.read_file("../Reti/problema_1.xdsl")
    net.update_beliefs()

    print(f"{COLOUR}Inizio Processo Decisione Prototipo{RESET_COLOUR}")
    decision_process(net)

    print("Utilità attesa finale")
    print_node_utility(net, Nodo.PROFITTO)
