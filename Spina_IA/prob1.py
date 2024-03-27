import pysmile
import pysmile_license

#funzione che stampa l'utilità per la ricerca di mearketing
def print_utility_ric(net):
    eu = net.get_node_value("ricerca_di_marketing")
    for i in range(0, len(eu)):
        print(net.get_outcome_id("ricerca_di_marketing", i) + "=" + str(eu[i]))

#funzione per settare l'evidenza
def change_evidence_and_update(net, node_id, outcome_id):
        if outcome_id is not None:
            net.set_evidence(node_id, outcome_id)
        else:
            net.clear_evidence(node_id)
        net.update_beliefs()

#funzione per stampare l'utilità di sviluppare o meno il prototipo
def print_ut_prot(net):
        eu = net.get_node_value("sviluppo_del_prototipo")
        for i in range(0, len(eu)):
            print(net.get_outcome_id("sviluppo_del_prototipo", i) + "=" + str(eu[i]))

#funzione per utitlità prodotto
def print_prodotto(net):
        expected_utility = net.get_node_value("prodotto")
        for i in range(0, len(expected_utility)):
            print(net.get_outcome_id("prodotto", i) + "=" + str(expected_utility[i]))

#funzione per mostrare le probabilità di profitto
def print_profitto(net):
        eu = net.get_node_value("profitto")
        print(eu)
        for i in range(0, len(eu)):
            print(net.get_outcome_id("profitto", i) + "=" + str(eu[i]))

net = pysmile.Network()
net.read_file("prob1.xdsl")

net.update_beliefs()
print("Devi sceliere se effettuare o meno la scelta di marketing, ecco cosa ti consiglio:")
print_utility_ric(net)
ric = input("\nVuoi effettuarla?\n1. si\n2. no")

#setto l'evidenza della ricerca in base alla scelta presa dall'utente
if ric == "1":
    change_evidence_and_update(net, "ricerca_di_marketing", "si")
    dom = input("Qual è il risultato della ricerca di mercato?")
    change_evidence_and_update(net, "risultato_della_ricerca", dom)
else:
    change_evidence_and_update(net, "ricerca_di_marketing", "no")
    change_evidence_and_update(net, "risultato_della_ricerca", "nessuno")
print("Ora devi scegliere se sviluppare o meno il prototipo:")
print_ut_prot(net)
prot = input("\nDesideri sviluppare un prototipo?\n1. si\n2. no")

#setto l'evidenza del prototipo in base all'input
if prot == "1":
    change_evidence_and_update(net, "sviluppo_del_prototipo", "si")
    q = input("Qual è la qualità del prodotto?")
    change_evidence_and_update(net, "qualita_del_prodotto", q)
else:
    change_evidence_and_update(net, "sviluppo_del_prototipo", "no")
    #se non si sviluppa il prototipo la qualità deve essere settata a standard
    change_evidence_and_update(net, "qualita_del_prodotto", "standard")
print("Ora non ti resta che scegliere se continuare la produzione del prodotto o no")
print_prodotto(net)
prod = input("\nVuoi proseguire?\n1. avanti\n2. ferma")

#setto la scelta del prodotto in modo da poter mostrare le probabilità di profitto
if prod == "1":
    change_evidence_and_update(net, "prodotto", "avanti")
else:
    change_evidence_and_update(net, "profitto", "nessuno")
print("\nIn base alle scelte effettuate le probabilità di profitto sono:")
print_profitto(net)


















