import pysmile
from licenze import pysmile_license
from classi import Nodo
from prototipo import decision_process
TEMPORAL_PLATE = 5

network = pysmile.Network()
network.read_file("../Reti/problema_2.xdsl")
if __name__ == '__main__':
    for i in range(TEMPORAL_PLATE):
        network.update_beliefs()


