from . import motor

def align_wheels():
    print("The car will be moved forward and then backward.")
    print("Observe whether it veers right or left.")
    print('Make sure the Motors switch is on!\n')
    ans = input("Place rover on the ground and press enter when ready!")
    import time
    car = motor.Motor()
    try:
        while True:
            car.forward()
            time.sleep(2)
            car.backward()
            time.sleep(2)
            car.stop()
            print("Did the car veer left or right while moving forward?")
            ans = input("[R for right/L for left/S for more or less straight]: ")
            if ans.lower() == "l":
                car.cali_right(10,10)
            elif ans.lower() == "r":
                car.cali_left(10,10)
            elif ans.lower() == "s":
                car.cali_ok()
                print("Results written!  Front wheel calibration complete!")
                break
            else:
                raise KeyboardInterrupt()
    except KeyboardInterrupt:
        print("Exiting without configuring!")
