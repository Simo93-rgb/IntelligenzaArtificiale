import pysmile
import pysmile_license
import colorama
from colorama import Fore, Style

#funzione per stampare le prbabilità del sensore delle varie posizioni rilevate
def print_sensore(net, sens):
    eu = net.get_node_value(sens)
    for i in range(0, len(eu)):
        print(net.get_outcome_id(sens, i) + "=" + str(eu[i]))

#funzione per mostrare l'utilità dell'azione
def print_azione(net, az):
    eu = net.get_node_value(az)
    for i in range(0, len(eu)):
        print(net.get_outcome_id(az, i) + "=" + str(eu[i]))
    return eu.index(max(eu))

net = pysmile.Network()
net.read_file("prob2_unroll.xdsl")
net.update_beliefs()

for i in range(0,5):
    net.update_beliefs()
    if i >=1:
        azione = "azione_" + str(i)
        sensore = "sensore_" + str(i)
    else:
        azione = "azione"
        sensore = "sensore"
    print("Il sensore rileva con le seguenti probabilità:")
    s = print_sensore(net, sensore)
    sens = input("Che posizione ha rilevato il nsore?")

    #setto la posizione rilevata del sensore in base all'input ricevuto ed aggiorno la rete
    net.set_evidence(sensore, sens)
    net.update_beliefs()
    print("L'azione consigliata e:")
    eu = print_azione(net, azione)

    #esegue l'azione in base alla migliore
    if eu == 0:
        print("azione eseguita:" + Fore.GREEN + "sinistra")
        print(Style.RESET_ALL)
        net.set_evidence(azione, "sinistra")
        net.update_beliefs()
    if eu == 1:
        print("azione eseguita:" + Fore.GREEN + "mantieni")
        print(Style.RESET_ALL)
        net.set_evidence(azione, "mantieni")
        net.update_beliefs()
    if eu == 2:
        print("azione eseguita:" + Fore.GREEN + "destra")
        print(Style.RESET_ALL)
        net.set_evidence(azione, "destra")
        net.update_beliefs()




