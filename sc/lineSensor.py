import time
import RPi.GPIO as GPIO

IR01 = 14
IR02 = 15
IR03 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR01,GPIO.IN)
GPIO.setup(IR02,GPIO.IN)
GPIO.setup(IR03,GPIO.IN)

class Line_Sensor:
    
    def getValues(self):
        '''
        Returns a 3-tuple (left,center, right) light sensor.  Each will have a
        value of 1 if black or 0 if white.
        '''
        return (GPIO.input(IR01),GPIO.input(IR02),GPIO.input(IR03))

# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    infrared=Line_Sensor()
    try:
        while True:
            print('Line sensor values:',infrared.getValues())
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        pass
