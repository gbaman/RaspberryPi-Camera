#Timelapse controller v0.1
#By Andrew Mulholland aka gbaman

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

from subprocess import call # Allows us to run normal bash commands
from time import sleep
from os import path # Allows checking if folder exists
from os import makedirs # Allows creation of directories

#Subroutine used to check if folder exists and if not, create one
def pathcheck(dir):
    if path.isdir(dir) == False: #Check if directory exists
        print("The directory to store the photos does not exist, want me to make it for you? y or n")
        q = False
        while q == False:
            question = raw_input()
            if question == "y":
                makedirs(dir) #Makes the directory
                print('Ok, directory created (we think but not error detection is in this program, might want to check yourself just in case)')
                q = True
                return True
            elif question == "n":
                print('Ok, Please enter a new directory')
                return False
            else:
                print("Please enter a valid option, y or n")
                q = False
                
                

# Subroutine to take the picture
def takepicture(num, dir):
    if num in range(0,10):
        num = "0" + str(num)
    else:
        num = str(num)
    call(["raspistill", "-hf", "-t", "1000" ,"-o", dir + "/" + str(num) + '.jpg'])
    # Command to take the picture
    
    
    
# Subroutine to calculate times remaining
def status(time, remainpic):
    print("Remaining pictures = " + str(remainpic))
    print("Remaining time = " + str(int(time) * int(remainpic)) + " seconds or " + str((int(time) * int(remainpic)) / 60) + " minutes remaining")



# Subroutine to control the timelapse and count pictures
def timelapsecontrol(time, picnum, dir):
    picnum = int(picnum)
    for count in range(0, picnum):
        takepicture((count+1), dir)
        remainpic = (picnum - count)
        status(time, remainpic)
        sleep(int(time) - 1)
    print("Timelapse completed")


# The main control subroutine
def maincontrol():
    print("Welcome to pi timelapser. Written by Gbaman at pi.gbaman.info")
    print("To get started, where would you like the photos to be saved?")
    i = False
    while i == False:
        print("For default location (/home/pi/timelapse) enter d, for custom location enter c")
        locationchoice = raw_input()
        if locationchoice == "d":
            dir = "/home/pi/timelapse"
            pathsorted = pathcheck(dir)
            i = pathsorted
        elif locationchoice == "c":
            print("Enter your chosen directory")
            dir = raw_input()
            pathsorted = pathcheck(dir)
            i = pathsorted
        else:
            print("Please enter a valid option, c or d")
            i = False
    print("Ok, now that directory to save the pictures is sorted, lets choose how many pictures you want to take and how often to take them")
    i = False
    while i == False:
        print("How many pictures would you like to take in total?")
        picnum = raw_input()
        print("How long between each picture? Minimum of 1 second")
        pictime = raw_input()
        if pictime < 1:
            print("Please enter a number greater than 1")
            continue
        print("The estimated time for this timelapse is " + str(int(picnum) * int(pictime)) + " seconds or " + str(int(picnum) * int(pictime) / 60) + " minutes or around " + str((int(picnum) * int(pictime) / 60) / 60) + " hours")
        print("That sound right and you ready to go? y to start or n to enter picture numbers again")
        k = False
        while k == False:
            inready = raw_input()
            if inready == "y":
                k = True
                i = True
                timelapsecontrol(pictime, picnum, dir)
            elif inready == "n":
                k = True
                i = False
            else:
                print("Please enter a valid option")
        
        
    
#-----Main program------------------------------------------------------------------------------------------------------------------------------------------------------

maincontrol()
  