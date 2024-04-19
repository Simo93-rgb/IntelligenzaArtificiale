import pysmile
from licenze import pysmile_license
from classi import Nodo
from decision_process import decision_process, print_node_utility

if __name__ == "__main__":
    net = pysmile.Network()
    net.read_file("../Reti/problema_1.xdsl")
    net.update_beliefs()

    decision_process(net)
    # print("type su un nodo chance: {}".format(net.get_node_type("domanda_stimata_di_mercato")))
    # print("type su un nodo decision: {}".format(net.get_node_type("prototipazione")))
    # print("type su un nodo decision: {}".format(net.get_node_type("produzione")))
    print("Utilità attesa finale")
    print_node_utility(net, Nodo.PROFITTO)
