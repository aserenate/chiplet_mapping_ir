import sys
sys.path.append('../../cfg/')
from config import *

# Note:
# -- 1. trace format: {(src_node0, dst_node0):comm_num0, (src_node1, dst_node1):comm_num1, ...}
class communicationModel:
    def __init__(self, topology):
        self.link_util              = topology.link_util
        self.route_table            = topology.route_table
        self.router_access_time     = 0

        self.communication_delay    = None
        self.communication_energy   = None
        self.bottleneck_link        = None
        
    def addTrace(self, trace):
        for pair, comm_num in trace.items():
            route = self.route_table[pair]
            for link in route:
                self.link_util[link][0] += comm_num
            self.router_access_time += len(route) - 1
    
    def calCommDelay(self):
        max_DR = 0
        max_DR_link = []
        for link, util in self.link_util.items():
            if util[0] / util[1] > max_DR:
                max_DR = util[0] / util[1]
                max_DR_link = [link]
            elif util[0] / util[1] == max_DR:
                max_DR_link.append(link)
        self.communication_delay = max_DR
        self.bottleneck_link     = max_DR_link
        
    def calCommEnergy(self):
        # TODO: need energy parameter
        energy = 0
        # 1. link energy
        for _, util in self.link_util.items():
            energy += util[0] * util[2]
        
        # 2. router energy
        energy += self.router_access_time * router_e
        
        self.communication_energy = energy
    
