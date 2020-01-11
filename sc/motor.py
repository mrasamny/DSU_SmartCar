import time
from PCA9685 import PCA9685
from dimension import *
from filedb import *

class Motor:
    def __init__(self):
        self.pwm = PCA9685(0x40, debug=True)
        self.pwm.setPWMFreq(50)
        self._speed = 30
        self.db = FileDB()
        self.front_left_offset = self.db.get('front_left_offset',0)
        self.back_left_offset = self.db.get('back_left_offset',0)
        self.front_right_offset = self.db.get('front_right_offset',0)
        self.back_right_offset = self.db.get('back_right_offset',0)
    
    def cali_left(self,front_offset,back_offset):
        self.front_left_offset -= front_offset
        self.back_left_offset -= back_offset
    
    def cali_right(self,front_offset,back_offset):
        self.front_right_offset -= front_offset
        self.back_right_offset -= back_offset
        
    def cali_ok(self):
        self.db.set('front_left_offset',self.front_left_offset)
        self.db.set('back_left_offset',self.back_left_offset)
        self.db.set('front_right_offset',self.front_right_offset)
        self.db.set('back_right_offset',self.back_right_offset)
        
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
        duty += self.front_left_offset
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
        duty += self.back_left_offset
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
        duty += self.front_right_offset
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
        duty += self.back_right_offset
        if duty>0:
            self.pwm.setMotorPwm(4,0)
            self.pwm.setMotorPwm(5,duty)
        elif duty<0:
            self.pwm.setMotorPwm(5,0)
            self.pwm.setMotorPwm(4,abs(duty))
        else:
            self.pwm.setMotorPwm(4,4095)
            self.pwm.setMotorPwm(5,4095)
            
    def setMotorModel(self,duty1,duty2,duty3,duty4):
        duty1,duty2,duty3,duty4=self.duty_range(duty1,duty2,duty3,duty4)
        self.left_Upper_Wheel(duty1)
        self.left_Lower_Wheel(duty2)
        self.right_Upper_Wheel(duty3)
        self.right_Lower_Wheel(duty4)

    def getDuty(self, speed): 
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
        duty = self.getDuty(self.speed)
        self.setMotorModel(duty,duty,duty,duty)

    def backward(self):
        '''
        Car moves backward indefinitely.
        '''
        duty = self.getDuty(self.speed)
        self.setMotorModel(-duty,-duty,-duty,-duty)

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
        duty = self.getDuty(self.speed)
        # On a left turn, the internal wheels (internal to radius of curvature)
        # are the left wheels
        internal_wheel_speed = self.speed * (1 - car_width/radius_of_curvature)
        internal_wheel_duty = self.getDuty(internal_wheel_speed)
        self.setMotorModel(internal_wheel_duty,internal_wheel_duty,duty,duty)

    def turn_right(self, radius_of_curvature = car_width/2):
        '''
        Turns the car to the right.
        
        :radius_of_curvature: raduis of curvature of the turn in cm.  if no value is provided,
                              then car will turn like a tank about an axis perpendicular
                              to the center of the car.
        '''
        if radius_of_curvature < car_width/2:
            radius_of_curvature = car_width/2
        duty = self.getDuty(self.speed)
        # On a right turn, the internal wheels (internal to radius of curvature)
        # are the right wheels
        internal_wheel_speed = self.speed * (1 - car_width/radius_of_curvature)
        internal_wheel_duty = self.getDuty(internal_wheel_speed)
        self.setMotorModel(duty,duty,internal_wheel_duty,internal_wheel_duty)

    def stop(self):
        self.setMotorModel(0,0,0,0)
                
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
