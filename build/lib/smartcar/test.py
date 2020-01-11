import time
from .led import *
led=Led()
def test_Led():
    try:
        led.ledIndex(0x01,255,0,0)      #Red
        led.ledIndex(0x02,255,125,0)    #orange
        led.ledIndex(0x04,255,255,0)    #yellow
        led.ledIndex(0x08,0,255,0)      #green
        led.ledIndex(0x10,0,255,255)    #cyan-blue
        led.ledIndex(0x20,0,0,255)      #blue
        led.ledIndex(0x40,128,0,128)    #purple
        led.ledIndex(0x80,255,255,255)  #white'''
        print("The LED has been lit, the color is red orange yellow green cyan-blue blue white")
        time.sleep(3)               #wait 3s
        led.colorWipe(led.strip, Color(0,0,0))  #turn off the light
        print("\nEnd of program")
    except KeyboardInterrupt:
        led.colorWipe(led.strip, Color(0,0,0))  #turn off the light
        print("\nEnd of program")

        
        
from .motor import *            
PWM=Motor()          
def test_Motor(): 
    try:
        PWM.forward()       #Forward
        print("The car is moving forward")
        time.sleep(1)
        PWM.backward()   #Back
        print("The car is going backwards")
        time.sleep(1)
        PWM.turn_left()       #Left 
        print("The car is turning left")
        time.sleep(1)
        PWM.turn_right()       #Right 
        print("The car is turning right")  
        time.sleep(1)
        PWM.stop()                   #Stop
        print("\nEnd of program")
    except KeyboardInterrupt:
        PWM.setMotorModel(0,0,0,0)
        print("\nEnd of program")


from .obstacleSensor import *
obstacle=Obstacle_Sensor()                
def test_Ultrasonic():
    try:
        while True:
            data=obstacle.get_distance()   #Get the value
            print(("Obstacle distance is "+str(data)+"CM"))
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEnd of program")


from .lineSensor import *
def test_Infrared():
    line = Line_Sensor()
    try:
        while True:
            line = line.getValues()
            if line == (False,True,False):
                print('Middle')
            elif  line == (False,False,True):
                print('Right')
            elif line == (True,False,False):
                print('Left')
    except KeyboardInterrupt:
        print("\nEnd of program")


from .servo import *
pwm=Servo()
def test_Servo():
    try:
        while True:
            for i in range(50,110,1):
                pwm.pan(i)
                time.sleep(0.01)
            for i in range(110,50,-1):
                pwm.pan(i)
                time.sleep(0.01)
            for i in range(80,150,1):
                pwm.tilt(i)
                time.sleep(0.01)
            for i in range(150,80,-1):
                pwm.tilt(i)
                time.sleep(0.01)   
    except KeyboardInterrupt:
        pwm.pan(90)
        pwm.tilt(90)
        print("\nEnd of program")
        
        
from .adc import *
from .lightSensor import *
adc=Adc()
light = Light_Sensor()
def test_Adc():
    try:
        while True:
            Left_IDR,Right_IDR=light.getValues()
            print(("The photoresistor voltage on the left is "+str(Left_IDR)+"V"))
            print(("The photoresistor voltage on the right is "+str(Right_IDR)+"V"))
            power=adc.getBatteryLevel()
            print(("The battery voltage is "+str(power*3)+"V"))
            time.sleep(1)
            print('\n')
    except KeyboardInterrupt:
        print("\nEnd of program")

from .buzzer import *
buzzer=Buzzer()
def test_Buzzer():
    try:
        buzzer.on()
        time.sleep(1)
        print("1S")
        time.sleep(1)
        print("2S")
        time.sleep(1)
        print("3S")
        buzzer.off()
        print("\nEnd of program")
    except KeyboardInterrupt:
        buzzer.off()
        print("\nEnd of program")
        
import cv2
def test_Camera():
        try:
            print("\nOpen camera")
            capturing_Flag = True
            cap = cv2.VideoCapture(0)
            while(capturing_Flag):
                ret, frame = cap.read()
                cv2.imshow("Capture", frame)
                cv2.waitKey(5)
            cv2.destroyAllWindows()
        except KeyboardInterrupt:
                print("\nClose camera")
                capturing_Flag = False
        
# Main program logic follows:
if __name__ == '__main__':

    print ('Program is starting ... ')
    import sys
    if len(sys.argv)<2:
        print("Parameter error: Please assign the device")
        exit() 
    if sys.argv[1] == 'Led':
        test_Led()
    elif sys.argv[1] == 'Motor':
        test_Motor()
    elif sys.argv[1] == 'Ultrasonic':
        test_Ultrasonic()
    elif sys.argv[1] == 'Infrared':
        test_Infrared()        
    elif sys.argv[1] == 'Servo': 
        test_Servo()               
    elif sys.argv[1] == 'ADC':   
        test_Adc()  
    elif sys.argv[1] == 'Buzzer':   
        test_Buzzer() 
    elif sys.argv[1] == 'Camera':  
        test_Camera() 

        
        
        
        
