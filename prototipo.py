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


def print_node_utility(net, node_id: str):
    node = net.get_node_value(node_id)
    for i in range(0, len(node)):
        print(net.get_outcome_id(node_id, i) + "=" + str(node[i]))


def print_eu_domanda_mercato(net):
    print_node_utility(net, "ricerca_di_mercato")


def print_eu_prototipazione(net):
    print_node_utility(net, "prototipazione")


def print_eu_produzione(net):
    print_node_utility(net, "produzione")


def print_eu_profitto(net):
    print_node_utility(net, "profitto")


def change_evidence_and_update(net, node_id, outcome: Outcome = None):
    if outcome not in Outcome.__members__.values():
        raise ValueError(f"outcome deve essere uno dei seguenti: {list(Outcome)}")
    if outcome is not None:
        net.set_evidence(node_id, outcome.value)
    else:
        net.clear_evidence(node_id)
    net.update_beliefs()


def cambia_scelta_ricerca_di_mercato(net, outcome: Outcome = None):
    change_evidence_and_update(net, "ricerca_di_mercato", outcome)


def cambia_evidenza_domanda_stimata_di_mercato(net, outcome: Outcome = None):
    change_evidence_and_update(net, "domanda_stimata_di_mercato", outcome)


def cambia_scelta_prototipazione(net, outcome: Outcome = None):
    change_evidence_and_update(net, "prototipazione", outcome)


def cambia_evidenza_qualita_prodotto(net, outcome: Outcome = None):
    change_evidence_and_update(net, "qualita_prodotto", outcome)


def cambia_scelta_produzione(net, outcome: Outcome = None):
    change_evidence_and_update(net, "produzione", outcome)


def scelta_ricerca(net):
    print("Devi sceliere se effettuare o meno la scelta di marketing, "
          "ecco le utilità:")
    print_eu_domanda_mercato(net)
    ricerca = input("\nVuoi effettuarla?\n1. si\n2. no\n")
    return ricerca == "1"


def set_evidenza_domanda(net, fare_ricerca: bool):
    if fare_ricerca:
        print('Hai scelto di fare la ricerca di mercato')
        cambia_scelta_ricerca_di_mercato(net, Outcome.YES)
        domanda = input("Qual è il risultato della ricerca di mercato?"
                        "Lo devi impostare tu"
                        "\n1. low\n2. high\n")
        if domanda == 1:
            cambia_evidenza_domanda_stimata_di_mercato(net, Outcome.LOW)
        else:
            cambia_evidenza_domanda_stimata_di_mercato(net, Outcome.HIGH)
    else:
        print('Hai scelto di non fare la ricerca di mercato')
        cambia_scelta_ricerca_di_mercato(net, Outcome.NO)
        cambia_evidenza_domanda_stimata_di_mercato(net, Outcome.NOTHING)


def scelta_prototipazione(net):
    print("Devi sceliere se prototipare, "
          "ecco le utilità:")
    print_eu_prototipazione(net)
    risposta_prototipazione = input("\nVuoi prototipare?\n1. si\n2. no\n")
    return risposta_prototipazione == "1"


def set_evidenza_prototipazione(net, prototipare: bool):
    if prototipare:
        print('Hai scelto di costruire un prototipo')
        cambia_scelta_prototipazione(net, Outcome.YES)
        costruzione_prototipo = input("Come cambia la qualità? "
                                      "La devi impostare tu"
                                      "\n1. standard\n2. high\n")
        if costruzione_prototipo == "1":
            cambia_evidenza_qualita_prodotto(net, Outcome.STANDARD)
        else:
            cambia_evidenza_qualita_prodotto(net, Outcome.HIGH)
    else:
        print('Hai scelto di non costruire il prototipo \n')
        cambia_scelta_prototipazione(net, Outcome.NO)
        cambia_evidenza_qualita_prodotto(net, Outcome.STANDARD)



def scelta_produzione_prodotto(net):
    print("Devi sceliere se produrre, "
          "ecco le utilità:")
    print_eu_produzione(net)
    risposta_produzione = input("\nVuoi produrre?\n1. si\n2. no\n")
    return risposta_produzione == "1"


def set_evidenza_produzione_prodotto(net, produrre: bool):
    if produrre:
        print('Hai scelto di mandare avanti la produzione')
        cambia_scelta_produzione(net, Outcome.YES)
    else:
        print('Hai scelto di non produrre\n')
        cambia_scelta_produzione(net, Outcome.NO)


net = pysmile.Network()
net.read_file("Reti/problema_1.xdsl")
net.update_beliefs()

ricerca_mercato = scelta_ricerca(net)
set_evidenza_domanda(net, ricerca_mercato)
prototipazione = scelta_prototipazione(net)
set_evidenza_prototipazione(net, prototipazione)
produzione = scelta_produzione_prodotto(net)
set_evidenza_produzione_prodotto(net, produzione)

print("Utilità attesa finale")
print_eu_profitto(net)