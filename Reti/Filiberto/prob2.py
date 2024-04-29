import pysmile
import pysmile_license
import random
from datetime import datetime

random.seed(datetime.now().timestamp())

NO = "No"
YES = "Sì"
DRY = "Secco"
WET = "Umido"
IRR = "Sconnesso"
REG = "Regolare"
LFT = "Sinistra"
STAY = "Mantieni"
CTR = "Centro"
RGT = "Destra"
POS = [LFT, CTR, RGT]

ACT = "Azione"
FLT = "Guasto"
MET = "Meteo"
OBS = "Osservazione"
TER = "Terreno"

N = 5


# Update evidence in a node
def update_evidence(net, node_name, evidence):
    net.set_evidence(node_name, evidence) if evidence else net.clear_evidence(node_name)
    net.update_beliefs()
    return evidence


# Set fault condition
def set_fault(net, met, ter, t_str, flt=NO):
    if (met == WET and random.random() <= 0.1
            or ter == IRR and random.random() <= 0.5
            or random.random() <= 0.1):
        flt = YES
    print(f"Tempo {t_str[1:]}:\n{MET} {met}\n{TER} {ter}\n{FLT} {flt}\n")
    return update_evidence(net, FLT + t_str, flt)


# Get meteo, terrain and fault conditions
def get_conditions(net, t):
    t_str = f"_{str(t)}"
    pt_str = f"_{str(t-1)}"
    if t == 0:
        update_evidence(net, MET, DRY)
        update_evidence(net, TER, REG)
        update_evidence(net, FLT, NO)
        print(f"\nInizio marcia:\n{MET} {DRY}\n{TER} {REG}\n{FLT} {NO}\n")
    elif t == 1:
        met = update_evidence(net, MET + t_str, DRY) if random.random() <= 0.67 \
            else update_evidence(net, MET + t_str, WET)
        ter = update_evidence(net, TER + t_str, REG) if random.random() <= 0.67 \
            else update_evidence(net, TER + t_str, IRR)
        set_fault(net, met, ter, t_str)
    else:
        p_met = net.get_evidence_id(MET + pt_str)
        p_ter = net.get_evidence_id(TER + pt_str)
        p_flt = net.get_evidence_id(FLT + pt_str)
        met = update_evidence(net, MET + t_str, p_met) if random.random() <= 0.67 \
            else update_evidence(net, MET + t_str, WET) if p_met == DRY \
            else update_evidence(net, MET + t_str, DRY)
        ter = update_evidence(net, TER + t_str, p_ter) if random.random() <= 0.67 \
            else update_evidence(net, TER + t_str, IRR) if p_ter == REG \
            else update_evidence(net, TER + t_str, REG)
        set_fault(net, met, ter, t_str, p_flt)


# Get vehicle position automatically
def get_auto_position(net, observation):
    pos_prob = net.get_node_value(observation)
    rand = random.random()
    pos = update_evidence(net, observation, LFT) if rand <= pos_prob[0] \
        else update_evidence(net, observation, CTR) if pos_prob[0] < rand <= pos_prob[1] \
        else update_evidence(net, observation, RGT)
    print(f"Posizione rilevata: {pos}")


# Get vehicle position manually
def get_position(net, observation):
    pos = 0
    while pos not in range(1, len(POS) + 1):
        pos = input("Posizione rilevata:\n"
                    "1) Sinistra\n"
                    "2) Centro\n"
                    "3) Destra\n"
                    "Risposta: ")
        pos = int(pos) if pos.isdigit() else 0
    update_evidence(net, observation, POS[pos-1])


# Set action to take
def set_action(net, action):
    mov_val = net.get_node_value(action)
    mov = update_evidence(net, action, net.get_outcome_id(action, mov_val.index(max(mov_val))))
    print(f"{ACT}: {mov} direzione\n") if mov == STAY \
        else print(f"{ACT}: Vai a {mov}")


network = pysmile.Network()
network.read_file("xdsl/prob2_unrolled.xdsl")

for i in range(N + 1):
    network.update_beliefs()

    if i == 0:
        act = ACT
        obs = OBS
    else:
        t_string = f"_{str(i)}"
        act = ACT + t_string
        obs = OBS + t_string

    get_conditions(network, i)
    get_position(network, obs)
    set_action(network, act)
    print(10 * "_")
