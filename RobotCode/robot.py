import numpy as np
import cv2
import time
import math
import segment
import image_processor

import Color as c
import motion
import time
import struct
import threading
import camera
from threading import Thread

middle_x = 435

prev_rad=250
speed_y = 0
speed_r = 0
speed_x = 0

motion_irl = motion.OmniMotionRobot()
motion_irl.open()
state = "findball"

###LISA FUNKTSIOONID
def controller(current, target, x_scale = 1, y_scale = 1):
    return (2 / (1 + np.exp(3*(target-current)/x_scale)) - 1) * y_scale

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

###MAIN FUNKTSIOONID
def backoff():
    global state
    print(" STATE: backoff")
    motion_irl.move(0,-20,0,0)

def stop():
    motion_irl(0,0,0,0
    )
def orbit2(processedData):

    print("Orbit1")
    radius=400
    max_speed=60
    r_const= 5
    global speed_y
    global state
    
    try:
        speed_x = -controller(processedData.basket_b.x, middle_x, x_scale=1500, y_scale=(max_speed - 3))
    except:
        print("No basket")
        speed_x=max_speed

    print("Orbit2")
    speed_r = 100 * speed_x / radius
    print("Orbit2.1")
    
    
    if processedData.balls[-1].x > middle_x+1 or processedData.balls[-1].x < (middle_x-1):
        speed_r += (middle_x - processedData.balls[-1].x) / 100 * r_const
    

    motion_irl.move(int(speed_x), int(speed_y), int(speed_r), 100)
    print("SpeedX:",speed_x)
    print("Orbit5")

def orbit(radius, speed_x, cur_radius, cur_object_x):
        if speed_x>0:
            speed_x=clamp(speed_x,5,70)
        if speed_x<0:
            speed_x=clamp(speed_x,-5,-70)
            
        speed_y = 0
        speed_r = 100 * speed_x / radius
        buffer_x = 1
        r_const = 5
        y_const = 3
        
       
        
        # Radius adjustment
        if cur_radius > (radius + buffer_x) or cur_radius < (radius - buffer_x):
            speed_y -= (radius - cur_radius) / 100 * y_const
        # Centering object, rotational speed adjustment
        if cur_object_x > (middle_x + buffer_x) or cur_object_x < (middle_x - buffer_x):
            speed_r += (middle_x - cur_object_x) / 100 * r_const

        print("robot:",int(speed_x), int(speed_y), int(speed_r))
        
        motion_irl.move(int(speed_x), int(speed_y), int(speed_r),0)
        


def getclose(X,Y):
    global state
    print("STATE: getclose")

    offcentre = (X - middle_x)
    t_speed = (offcentre/10)
    ###MATIKOOT
    Yslow = Y/4.2
    ###MATIKUUT
    print("offcentre:", offcentre)
    if offcentre <= 300 and offcentre >= -300 and Y < 130:
        motion_irl.move(int(t_speed),int(50-(abs(t_speed))),int(-t_speed/3),0)
        print("Full speed")
    else:
        motion_irl.move(int(t_speed/3),int((50-Yslow)),int(-t_speed/10),0)
        print("Slow down")
     

def findaball(processedData):
    global state
    print(" STATE: findball")
    ### robot tries to find ball
    motion_irl.move(0,0,10,0)
    

def makeshot(dist):
    global state
 
    throwdistance = (dist) * 0.18931 + 348.476439
    motion_irl.move(0,20,0,int(throwdistance))
    







