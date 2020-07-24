#Libraries
import RPi.GPIO as GPIO
import time
import os

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        oldDist = 0
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if oldDist == 0 or dist - oldDist > 2 or oldDist - dist > 2:
                # os.system('mpg123 -l 2 Windeleimer/*.mp3')
                os.system('find /home/pi/Windeleimer -name "*.mp3" | sort --random-sort| head -n 1|xargs -d \'\n\' mpg123')
                #find -name "*.mp3" | sort --random-sort| head -n 100|xargs -d '\n' mpg123
                oldDist = dist
                print("old dist", oldDist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
