import pysmile
from licenze import pysmile_license
from classi import Nodo
from decision_process import decision_process, print_node_utility

if __name__ == "__main__":
    net = pysmile.Network()
    net.read_file("../Reti/problema_1.xdsl")
    net.update_beliefs()

    decision_process(net)

    print("Utilità attesa finale")
    print_node_utility(net, Nodo.PROFITTO)
