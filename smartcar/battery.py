from .adc import *

class Battery:
    def __init__(self):
        self.adc = Adc()
    
    def getLevel(self):
        '''
        Returns the battery voltage.
        '''
        return self.adc.recvADC(2)*3
