import time
from .PCA9685 import PCA9685
from .dimension import *
from .filedb import *

class Motor:
    def __init__(self):
        self.pwm = PCA9685(0x40, debug=True)
        self.pwm.setPWMFreq(50)
        self._speed = 40
        self.db = FileDB()
        self.front_left_offset = self.db.get('front_left_offset',0)
        self.back_left_offset = self.db.get('back_left_offset',0)
        self.front_right_offset = self.db.get('front_right_offset',0)
        self.back_right_offset = self.db.get('back_right_offset',0)
        self.forward_offset = self.db.get('forward',1)
        self.wheel_duty = [0,0,0,0]
    
    def cali_left(self,front_offset,back_offset):
        self.front_left_offset -= front_offset
        self.back_left_offset -= back_offset
    
    def cali_right(self,front_offset,back_offset):
        self.front_right_offset -= front_offset
        self.back_right_offset -= back_offset
        
    def cali_flip_forward(self):
        self.forward_offset = -1*self.forward_offset
        
    def cali_ok(self):
        self.db.set('front_left_offset',self.front_left_offset)
        self.db.set('back_left_offset',self.back_left_offset)
        self.db.set('front_right_offset',self.front_right_offset)
        self.db.set('back_right_offset',self.back_right_offset)
        self.db.set('forward',self.forward_offset)
        
    def adjust_duty(self,duty1,duty2,duty3,duty4):
        duty1 += self.front_left_offset
        duty2 += self.back_left_offset
        duty3 += self.front_right_offset
        duty4 += self.back_right_offset
        return (duty1,duty2,duty3,duty4)
    
    def duty_range(self,duty1,duty2,duty3,duty4):
        if duty1>4095:
            duty1=4095
        elif duty1<-4095:
            duty1=-4095        
        
        if duty2>4095:
            duty2=4095
        elif duty2<-4095:
            duty2=-4095
            
        if duty3>4095:
            duty3=4095
        elif duty3<-4095:
            duty3=-4095
            
        if duty4>4095:
            duty4=4095
        elif duty4<-4095:
            duty4=-4095
        return duty1,duty2,duty3,duty4
        
    def left_Upper_Wheel(self,duty):
        self.wheel_duty[0] = duty
        if duty>0:
            self.pwm.setMotorPwm(0,0)
            self.pwm.setMotorPwm(1,duty)
        elif duty<0:
            self.pwm.setMotorPwm(1,0)
            self.pwm.setMotorPwm(0,abs(duty))
        else:
            self.pwm.setMotorPwm(0,4095)
            self.pwm.setMotorPwm(1,4095)
        
            
    def left_Lower_Wheel(self,duty):
        self.wheel_duty[1] = duty
        if duty>0:
            self.pwm.setMotorPwm(3,0)
            self.pwm.setMotorPwm(2,duty)
        elif duty<0:
            self.pwm.setMotorPwm(2,0)
            self.pwm.setMotorPwm(3,abs(duty))
        else:
            self.pwm.setMotorPwm(2,4095)
            self.pwm.setMotorPwm(3,4095)
            
    def right_Upper_Wheel(self,duty):
        self.wheel_duty[2] = duty
        if duty>0:
            self.pwm.setMotorPwm(6,0)
            self.pwm.setMotorPwm(7,duty)
        elif duty<0:
            self.pwm.setMotorPwm(7,0)
            self.pwm.setMotorPwm(6,abs(duty))
        else:
            self.pwm.setMotorPwm(6,4095)
            self.pwm.setMotorPwm(7,4095)
            
    def right_Lower_Wheel(self,duty):
        self.wheel_duty[3] = duty
        if duty>0:
            self.pwm.setMotorPwm(4,0)
            self.pwm.setMotorPwm(5,duty)
        elif duty<0:
            self.pwm.setMotorPwm(5,0)
            self.pwm.setMotorPwm(4,abs(duty))
        else:
            self.pwm.setMotorPwm(4,4095)
            self.pwm.setMotorPwm(5,4095)
            
    def set_motor_model(self,duty1,duty2,duty3,duty4):
        duty1,duty2,duty3,duty4=self.duty_range(duty1,duty2,duty3,duty4)
        self.left_Upper_Wheel(duty1)
        self.left_Lower_Wheel(duty2)
        self.right_Upper_Wheel(duty3)
        self.right_Lower_Wheel(duty4)

    def get_duty(self, speed): 
        return int(speed/100*4095)
    
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, s):
        self._speed = s
        if self._speed > 100:
            self._speed = 100
        elif self._speed < 0:
            self._speed = 0
            
    def forward(self):
        '''
        Car moves forward indefinitely.
        '''
        duty = self.get_duty(self.speed)
        (duty1,duty2,duty3,duty4) = self.adjust_duty(duty,duty,duty,duty)
        #print('Duty: {} - {} - {} - {}'.format(duty1,duty2,duty3,duty4));
        self.set_motor_model(self.forward_offset*duty1,self.forward_offset*duty2, \
                             self.forward_offset*duty3,self.forward_offset*duty4)

    def backward(self):
        '''
        Car moves backward indefinitely.
        '''
        duty = self.get_duty(self.speed)
        (duty1,duty2,duty3,duty4) = self.adjust_duty(duty,duty,duty,duty)
        self.set_motor_model(-self.forward_offset*duty1,-self.forward_offset*duty2, \
                             -self.forward_offset*duty3,-self.forward_offset*duty4)

    # Vo = V     (eq. 1)
    # Vi = V-v   (eq. 2)
    # where Vo and Vi are speed of outer and inner wheels, respectively.
    # Here the outer wheel is kept at the speed set for the car and the
    # inner wheel's speed is reduced by the reduced speed calculated to
    # generate the turn at the requested radius of curvature.
    #
    # So = Vo*t = V*t = Ro*@   (eq. 3)
    # Si = Vi*t = Ri*@         (eq. 4)
    # Where So and Si are the arc lengths traced out by the outer and inner wheels.
    # Taking the ratio of eqs. 3 and 4, yields
    # V/Vi = Ro/Ri    (eq. 5)
    # Letting the outer wheel define the radius of curviture,
    # Ro = R      (eq. 6)
    # Ri = R - w  (eq. 7)
    # Where w is width of car measured from center of wheels and 
    # substituting eq. 7 into eq. 5 yields,
    #
    # V/(V-v) =  R/(R-w)  (eq. 8)
    #
    # VR - Vw = VR -Rv    (eq. 9)
    #
    # v = Vw/R            (eq. 10)
    # substituing eq. 10 into eq. 2, yileds
    # Vi = V (1- w/R), the speed of the inner wheel
    #
    # Setting R = w/2, yields the tank turn value where the inner wheels
    # spin backwards at speed -V and the outer wheels spin at speed V.
    
    def turn_left(self, radius_of_curvature = car_width/2):
        '''
        Turns the car to the left.
        
        :radius_of_curvature: raduis of curvature of the turn in cm.  if no value is provided,
                              then car will turn like a tank about an axis perpendicular
                              to the center of the car.
        '''
        if radius_of_curvature < car_width/2:
            radius_of_curvature = car_width/2
        duty = self.get_duty(self.speed)
        # On a left turn, the internal wheels (internal to radius of curvature)
        # are the left wheels
        internal_wheel_speed = self.speed * (1 - car_width/radius_of_curvature)
        internal_wheel_duty = self.get_duty(internal_wheel_speed)
        #print(internal_wheel_speed,' <---> ',internal_wheel_duty)
        #(duty1,duty2,duty3,duty4) = self.adjust_duty(internal_wheel_duty,internal_wheel_duty,duty,duty)
        (duty1,duty2,duty3,duty4) = (internal_wheel_duty,internal_wheel_duty,duty,duty)
        #print('Duty: {} - {} - {} - {}'.format(duty1,duty2,duty3,duty4))
        self.set_motor_model(duty1,duty2,duty3,duty4)

    def turn_right(self, radius_of_curvature = car_width/2):
        '''
        Turns the car to the right.
        
        :radius_of_curvature: raduis of curvature of the turn in cm.  if no value is provided,
                              then car will turn like a tank about an axis perpendicular
                              to the center of the car.
        '''
        if radius_of_curvature < car_width/2:
            radius_of_curvature = car_width/2
        duty = self.get_duty(self.speed)
        # On a right turn, the internal wheels (internal to radius of curvature)
        # are the right wheels
        internal_wheel_speed = self.speed * (1 - car_width/radius_of_curvature)
        internal_wheel_duty = self.get_duty(internal_wheel_speed)
        #print(internal_wheel_speed,' <---> ',internal_wheel_duty)
        #(duty1,duty2,duty3,duty4) = self.adjust_duty(duty,duty,internal_wheel_duty,internal_wheel_duty)
        (duty1,duty2,duty3,duty4) = (duty,duty,internal_wheel_duty,internal_wheel_duty)
        #print('Duty: {} - {} - {} - {}'.format(duty1,duty2,duty3,duty4))
        self.set_motor_model(duty1,duty2,duty3,duty4)

    def stop(self):
        '''
        Stops the car instantaneously.  At medium and high speeds
        and sometimes low speed, depending on surface, the car may slip
        or slide.
        '''
        self.set_motor_model(0,0,0,0)

    def brake(self):
        '''
        Simulates breaking in a car.  Reduces powers to motor over
        a couple of seconds.  This prevents the car from slipping
        or sliding at higher power as may occur when stop() is applied.
        '''
        for i in range(5):
            duty = [self.wheel_duty[i]//100 for i in range(4)]
            self.set_motor_model(duty[0],duty[1],duty[2],duty[3])
            time.sleep(.5)
        self.set_motor_model(0,0,0,0)
                
if __name__=='__main__':
    motor = Motor()          
    def loop(): 
        motor.forward()     #Forward
        time.sleep(3)
        motor.backward()    #Back
        time.sleep(3)
        motor.turn_left()   #Tank turn left
        time.sleep(3)
        motor.turn_right()  #Tank turn right    
        time.sleep(3)
        motor.turn_left(car_width/2)
        time.sleep(3)
        motor.turn_left(car_width*10)
        time.sleep(5)
        motor.backward()    #Back
        time.sleep(5)
        motor.turn_right(car_width/2)
        time.sleep(3)
        motor.turn_right(car_width*10)
        time.sleep(5)
        motor.backward()    #Back
        time.sleep(5)
        motor.stop()        #Stop
        
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        motor.stop()
