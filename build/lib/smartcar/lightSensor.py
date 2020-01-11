import time
from .adc import *

class Light_Sensor:
    def __init__(self):
        self.adc = Adc()
        
    def getValues(self):
        '''
        Returns the voltage of the (left,right) photoresistor,
        respectively, as a 2-tuple.
        '''
        Left_IDR=self.adc.recvADC(0)
        Right_IDR=self.adc.recvADC(1)
        
        return (Left_IDR,Right_IDR)
    

if __name__=='__main__':
    print ('Program is starting ... ')
    try:
        light = Light_Sensor()
        while True:
            print('Light sensor values:',light.getValues())
    except KeyboardInterrupt:
        pass 

