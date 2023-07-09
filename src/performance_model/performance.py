
from computation_model import *
from communication_model import *

class performance(communicationModel, computationModel):
    def __init__(self, topology, MAC_nums, DIV_nums):
        super().__init__(topology=topology, MAC_nums=MAC_nums, DIV_nums=DIV_nums)
        self.delay  = None
        self.energy = None
        
    def calPerformance(self):
        self.calCommDelay()
        self.calCommEnergy()
        self.calCompDelay()
        self.calCompEnergy()
        self.delay  = max(self.communication_delay, self.computation_delay)
        self.energy = self.communication_energy + self.computation_energy
        