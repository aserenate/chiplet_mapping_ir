import sys
sys.path.append('../../cfg/')
from config import *

class computationModel:
    def __init__(self, MAC_nums, DIV_nums):
        self.MAC_nums = MAC_nums
        self.DIV_nums = DIV_nums
        self.computation_delay  = None
        self.computation_energy = None
    
        self.MAC_delay          = 0
        self.DIV_delay          = 0
        self.MAC_times          = 0
        self.DIV_times          = 0 # TODO: not sure
        
        
    def addHWDefinedComputation(self, num, HW_num, type='MAC'):
        if type == 'MAC':
            self.MAC_times += num
            self.MAC_delay += num / HW_num
        elif type == 'DIV':
            self.DIV_times += num
            self.DIV_delay += num / HW_num
        else:
            print('{} operator is not considered'.format(type))
    
    def addComputation(self, num, type='MAC'):
        if type == 'MAC':
            self.MAC_times += num
            self.MAC_delay += num / self.MAC_nums * MAC_unit_delay
        elif type == 'DIV':
            self.DIV_times += num
            self.DIV_delay += num  / self.DIV_nums * DIV_unit_delay
        else:
            print('{} operator is not considered'.format(type))
    
    def calCompDelay(self):
        self.computation_delay = max(self.MAC_delay, self.DIV_delay)
        
    def calCompEnergy(self):
        MAC_energy = self.MAC_times * MAC_unit_energy
        DIV_energy = self.DIV_times * DIV_unit_energy
        self.computation_energy = MAC_energy + DIV_energy
    