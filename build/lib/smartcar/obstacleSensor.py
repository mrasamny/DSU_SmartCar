import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
trigger_pin = 27
echo_pin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin,GPIO.OUT)
GPIO.setup(echo_pin,GPIO.IN)

class Obstacle_Sensor:
    
    def send_trigger_pulse(self):
        GPIO.output(trigger_pin,True)
        time.sleep(0.00015)
        GPIO.output(trigger_pin,False)

    def wait_for_echo(self,value,timeout):
        count = timeout
        while GPIO.input(echo_pin) != value and count>0:
            count = count-1
     
    def get_distance(self):
        distance_cm=[0,0,0,0,0]
        for i in range(3):
            self.send_trigger_pulse()
            self.wait_for_echo(True,10000)
            start = time.time()
            self.wait_for_echo(False,10000)
            finish = time.time()
            pulse_len = finish-start
            distance_cm[i] = pulse_len/0.000058
        distance_cm=sorted(distance_cm)
        return int(distance_cm[2])
          
                      
# Main program logic follows:
if __name__ == '__main__':
                
    print ('Program is starting ... ')
    ultrasonic=Obstacle_Sensor()
    try:
        while true:
            print('Object distance:',ultrasonic.get_distance())
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        pass
