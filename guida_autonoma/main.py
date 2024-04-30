import pysmile
from licenze import pysmile_license
from classi import Nodo, Outcome
from prototipo import decision_process
from navigation import get_condition, get_position, set_fault, set_action, COMANDO, POSIZIONE, SENSORE_POSIZIONE

TEMPORAL_PLATE = 5

network = pysmile.Network()
network.read_file("../Reti/problema_2 unrolled.xdsl")

if __name__ == '__main__':
    for i in range(TEMPORAL_PLATE):
        network.update_beliefs()

        comando: str = COMANDO
        posizione: str = SENSORE_POSIZIONE
        if i != 0:
            comando: str = comando + f"_{str(i)}"
            posizione: str = posizione + f"_{str(i)}"

        get_condition(network, i)
        prompt = "Posizione rilevata?\n" \
                 "1) Sinistra\n" \
                 "2) Centro\n" \
                 "3) Destra\n" \
                 "Risposta: "
        options = {"1": Outcome.SINISTRA, "2": Outcome.CENTRO, "3": Outcome.DESTRA}
        get_position(network, posizione, options)
        set_action(network, comando)
        print(10 * "_")