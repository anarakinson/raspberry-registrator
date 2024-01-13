import RPi.GPIO as GPIO
import pigpio
import time
import subprocess
import argparse



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--angle", help="set angle", default="90")
    parser.add_argument("-p", "--pin", help="set servo pin", default="26")
    args = parser.parse_args()
    return args

def main():
    # if pigpiod not running
    # start pigpiod
    # subprocess.run(["sudo", "pigpiod"])
 
    args = parse_args()

    # get pin and angle
    servo = int(args.pin)
    angle = int(args.angle)

    if angle > 180:
        angle = 180
    if angle  < 0:
        angle = 0
    print(angle)
    # transform angle to frequency
    angle = ((angle / 90) * 1000) + 500
 
 
    # setting up servo
    pwm = pigpio.pi() 
    pwm.set_mode(servo, pigpio.OUTPUT)

    pwm.set_PWM_frequency(servo, 50)


#    for i in range(500, 2501, 5):
#        #print(f"freqency - {i}")
#        pwm.set_servo_pulsewidth(servo, i)
#        time.sleep(0.01)

 
    # rotating servo
    pwm.set_servo_pulsewidth(servo, angle)
    time.sleep(1)

    # turning off servo
    print("turning off")
    pwm.set_PWM_dutycycle(servo, 0)
    pwm.set_PWM_frequency( servo, 0 )

if __name__ == "__main__":
    main()
