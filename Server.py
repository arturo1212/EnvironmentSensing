class Agent:
    ip = ""
    agent_type = ""
    conn_dt = ""
    def __init__(self):
        self.ip = ""


from socket import *

def recruitAgents():
    cs = socket(AF_INET, SOCK_DGRAM)
    cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    cs.sendto(b'Joinme', ('255.255.255.255', 4210))

recruitAgents()
