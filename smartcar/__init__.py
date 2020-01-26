import sys
from . import motor
from . import servo

def align_wheels():
    print("The car will be moved forward and then backward.")
    print("Observe whether it veers right or left.")
    print('Make sure the Motors switch is on!\n')
    ans = input("Place rover on the ground and press enter when ready!")
    import time
    car = motor.Motor()
    car.speed=30
    try:
        while True:
            car.forward()
            time.sleep(2)
            car.backward()
            time.sleep(2)
            car.brake()
            print("Did the car veer left or right while moving forward?")
            ans = input("[R for right/L for left/S for more or less straight]: ")
            if ans.lower() == "l":
                car.cali_right(50,50)
            elif ans.lower() == "r":
                car.cali_left(50,50)
            elif ans.lower() == "s":
                car.cali_ok()
                print("Results written!  Front wheel calibration complete!")
                break
            else:
                raise KeyboardInterrupt()
    except KeyboardInterrupt:
        print("Exiting without configuring!")

def servo_install():
    s = servo.Servo()
    s.pan(90)
    s.tilt(90)

def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == "servo":
            servo_install()
        elif sys.argv[1] == "align":
            align_wheels()
    else:
        usage()

def usage():
    print("Usage:  smartcar [Command]")
    print("Commands:")
    print("  servo              Set servos to 90 degree for installation")
    print("  align              Align the steering ")
