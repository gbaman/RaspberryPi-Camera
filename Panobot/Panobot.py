# By Andrew Mulholland aka gbaman

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.


# Cam forward - pin 11
# Cam back - pin 12
# Rotate left - pin 15
# Rotate right - pin 13

numrotate = 20 #Only used if no calibrater is run
timeforrotate = 1.3 # How long the motors run each rotate
numupdown = 5 # How many layers

from subprocess import call # Allows us to run normal bash commands
import RPi.GPIO as GPIO
import time
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

def rotater(dir, timer): # Subroutine for rotating the robot
    if dir == 'left':
        GPIO.output(15,True)
        time.sleep(timer)
        GPIO.output(15,False)
    elif dir == 'right':
        GPIO.output(13,True)
        time.sleep(timer)
        GPIO.output(13,False)  
    else:
        print('Rotating error')

def camUpDown(dir,timer): # Subroutine for controlling the camera movement
    if dir == 'forward':
        GPIO.output(11,True)
        time.sleep(timer)
        GPIO.output(11,False)
    elif dir == 'back':
        GPIO.output(12,True)
        time.sleep(timer)
        GPIO.output(12,False)  
    else:
        print('cam error')

def calibrater(): # Subroutine no longer used and based on time but kept in for reference
    print('Commencing calibration, please enter any key when one full rotation is complete')
    start_time = time.time()
    GPIO.output(13,True)
    inthing = raw_input()
    end_time = time.time()
    GPIO.output(13,False)
    rotateTime = end_time - start_time
    print('Full rotation took ' + str(rotateTime))
    rotater("left", rotateTime)
    return rotateTime

def directcontrol(): # A direct controller used to configure the robot
    done = False
    while done == False:
        print("What would you like to control? For camera, hit c, for main unit, hit m, to quit hit q")
        control = raw_input()
        print('How many units?')
        unit = raw_input()
        unit = int(unit)
        if control == "c":
            print("Forward or back ?")
            dir = raw_input()
            for count in range(0,unit):
                camUpDown(dir, 0.3)
        elif control == "m":
            print("Rotate left or right ?")
            dir = raw_input()
            for count in range(0,unit):
                rotater(dir, timeforrotate)
        elif control == "q":
            done = True
        else:
            print("dont be bad")

#def totaltimecal():

def calibrater2(): # Subroutine that allows the user to configure how far they want to robot to turn
    done = False
    totalrotate = 0
    while done == False:
        print('How many rotations? If done, enter q. If direct control required, enter c')
        rotate = raw_input()
        if rotate == 'q':
            done = True
        elif rotate == "c":
            directcontrol()
        else:
            rotate = int(rotate)
            for count in range(0,rotate):
                rotater('left', timeforrotate)
                time.sleep(0.2)
            totalrotate = rotate + totalrotate
        
    print(totalrotate)
    return(totalrotate)
    
def takepicture(num, level): # Subroutine to take the picture - Make sure there is a /home/pi/pano1 directory!!!
    call(["raspistill", "-hf", "-t", "1000" ,"-o", "/home/pi/pano1/photo" + str(level) + "_" + str(num) + '.jpg'])


def controller(): # Main control subroutine. To do a dummy run, comment out takepicture(count1, count2) and uncomment out the time.sleeps
    #fullrotate = calibrater()
    fullrotate = 29
    numrotater = calibrater2()
    fullrotate = (numrotate * timeforrotate) * 0.75
    count2 = 1
    for count1 in range(0,numrotater):
        print('Number of turns remaining = ' +str(numrotate - count1))
        rotater("right", timeforrotate)
        for count2 in range(0,numupdown):
            takepicture(count1, count2)
            camUpDown("forward", 0.3)
            #time.sleep(0.5)
        for count3 in range(0,numupdown):
            camUpDown("back", 0.30)
            time.sleep(0.2)
        #time.sleep(0.5)


# Main code --------------------------------------------------------------------------------------------------------------
controller() # Runs the control subroutine
GPIO.cleanup() # Always good to clean up after outselves
