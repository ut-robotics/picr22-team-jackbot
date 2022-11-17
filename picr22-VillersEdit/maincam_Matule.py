import numpy as np
import cv2
import time
import math
import segment
import image_processor
import _pickle as pickle
import Color as c
import motion
import time
import struct
import threading
import camera
from threading import Thread


EnemyBasket = "pinkish"
global state
global randomcounter
randomcounter = 0

centrex = 435


state = "findball"

motion_irl = motion.OmniMotionRobot()
motion_irl.open()


#Hsv for disposal zone
lowerLimits_basgeto = np.array([0, 47, 24])
upperLimits_basgeto = np.array([255, 15, 255])
# HSV tresholds
lowerLimits_ball = np.array([16, 35, 36])
upperLimits_ball = np.array([82, 255, 99])

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def white_edge(th_img):
    th_img[0:,0] = 255
    th_img[0,0:] = 255
    th_img[0:,-1] = 255
    th_img[-1,0:] = 255
    
    return th_img

def list_objects(ball):
    obj_xysc = []
    key_all = [ball]
    # save points in one list
    for i in range(len(key_all)):
        key_tmp = key_all[i]
        if len(key_tmp)>0:
            for kp in key_tmp:
                x = kp.pt[0]
                y = kp.pt[1]
                s = kp.size
                new_pt = (int(x),int(y),s,i)# last value 'i' used for undersatanding color
                obj_xysc.append(new_pt)
                
    return obj_xysc

def sort_size(obj_list):
    nr_of_obj = len(obj_list)
    
    if nr_of_obj > 1:
        # list all object sizes
        obj_size = np.zeros(nr_of_obj)
        
        for i in range(nr_of_obj):
            obj_size[i] = obj_list[i][2]
        
        # sort descending based on size
        idx = np.argsort(-obj_size)
        #print(obj_size)
        #print(idx)

        # create an ordered array
        obj_list_new = list(obj_list)
        
        for i in range(nr_of_obj):
            obj_list_new[i] = obj_list[idx[i]]
        
        return obj_list_new
    else:      
        return obj_list
    
def findaball():
    global state
    print(" STATE: findball")
    ### robot tries to find ball
    motion_irl.move(0,0,10,0)
    if processedData.balls[0].x >= centrex - 200 and processedData.balls[0].x <= centrex + 200:
        ### robot found ball
        state = "getclose"
        
        
def getclose():
    global state
    global randomcounter
    randomcounter += 1
    print("STATE: getclose")

    if len(processedData.balls) <= 0 and randomcounter >= 10:
        print("getclose debuig")
        randomcounter = 0
        state = "findball"

    if len(processedData.balls) > 0 and processedData.balls[0].y <= 300:
        
        offcentre = (processedData.balls[0].x - centrex)
        t_speed = (offcentre/10)
        Yslow = processedData.balls[0].y/6.66

        print("offcentre:", offcentre)
        if offcentre <= 250 and offcentre >= -250 and processedData.balls[0].y < 200:
            motion_irl.move(int(t_speed),int(50-(abs(t_speed))),int(-t_speed/3),0)
        else:
            motion_irl.move(int(t_speed/3),int((50-Yslow)),int(-t_speed/10),0)
            
    else:
        if processedData.balls[0].y > 300:

            state = "orbit"
            print("MAKING SHOT")
        else:
            state = "findaball"
            print("findball")
            
            
            print(" back to looking for the ball xdddd")

def ballcentred():
    global state
    print(" STATE: ballcentred")
    if len(processedData.balls) == 0:
        state = "findball"
    if processedData.balls[0].y >= 340:
        ###if ball is really close by y cordinate
        state = "putsis"
    else:
        
        ### move towards the ball really slowly
        motion_irl.move(0,5,0,0)
        print(processedData.balls[0].y)
    if processedData.balls[0].y <= 200:
        state = "findball"

def angleshot():
    global temptimer
    global state
    print(" STATE: angleshot")
    print(processedData.basket_b.x)
    if processedData.basket_b.x <= 400:
        if processedData.basket_b.x >= 400 and processedData.basket_b.x <= 421:
            motion_irl.move(2,0,2,0)
        else:
            motion_irl.move(7,0,4,0)
    elif processedData.basket_b.x >= 448:
        if processedData.basket_b.x <= 448 and processedData.basket_b.x >= 427:
            motion_irl.move(-2,0,-2,0)
        else:
            motion_irl.move(-7,0,-4,0)
    elif processedData.basket_b.x <= 426 and processedData.basket_b.x >= 424:
        state = "makeshot"
        motion_irl.move(0,0,0,0)
        print("shoot")
        ##shoot
        temptimer = 0

def backoff():
    global state
    print(" STATE: backoff")
    timertemp = 0
    while timertemp < 50:
        timertemp += 1
        motion_irl.move(0,-10,5,0)
    state = "findball"

def makeshot():
    global state
    global temptimer
    print(" STATE: makeshoot")
    temptimer += 1
    if len(processedData.balls) == 0:
        state = "findball"
    elif temptimer >= 140: # 140
            state = "findball"
    elif temptimer >= 50: # 50
        throwdistance = processedData.basket_b.distance * 0.19054 + 364.7
        motion_irl.move(0,20,0,int(throwdistance))
    try:
        print("BASKET DISTANCE : ", processedData.basket_b.distance)
        if processedData.basket_b.distance <= 800:
            state = "backthefoff"
        print(processedData.basket_b.x)
    except:
        print("Basket not found makeshot")

def orbit():
    global state
    temptimer = 0
    print("Orbit")
    if len(processedData.balls) == 0:
        state = "findball"
    else:
        X_speed = (processedData.balls[0].y)/10
        R_speed = (processedData.balls[0].y)/40
        X_correct = clamp((processedData.balls[0].x - 435),-3,3)       
        
        print("X_Speed:",X_speed,"R_speed:",R_speed+X_correct)
    
        motion_irl.move(X_speed+X_correct,0,R_speed,100)

        if processedData.basket_b.x >= 400 and processedData.basket_b.x <= 470:
            state = "makeshot"





# Open the camera
cam = camera.RealsenseCamera()

debug = False
processor = image_processor.ImageProcessor(cam, debug=debug) #, debug=debug
processor.start()
#cv2.namedWindow("Original") # do not delete, used to quit the program
#cv2.namedWindow("Debugger")
#cv2.namedWindow("Debugger2")
while True:
    
    ########################
    ########################
    #find baskets by processedata
    #find balls , black line by blob
    ########################
    ########################
    processedData = processor.process_frame(aligned_depth=False)
    ########################
    ########################
#     contours, hierarchy = cv2.findContours(t_balls, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        
    try: 

        if state == "findball":
            ### robot tries to find ball
            try:
                findaball()
            except:
                print("findball error")

        elif state == "getclose":
            ### ball found get close
            try:
                getclose()
            except:
                print("getclose error")

        elif state == "ballcentered":
            try:
                ballcentred()
            except:
                print("ballcentred error")

        elif state == "angleshoot":
            try:
                angleshot()
            except:
                print("agleshot error")

        elif state == "backthefoff": ## basket fall back xd
            try:
                backoff()
            except:
                print("backoff error")

        elif state == "makeshot":
            try:
                makeshot()
            except:
                print("Makeshot error")
        
        elif state == "orbit":
            try:
                orbit()
            except:
                print("Orbit error")
        else:
            
            #orbit basics
            if len(processedData.balls) == 0:
                state = "findball"
            
            ### hoovers aorund the ball
            try:
                orbit()
            except:
                print("Orbit error")
            
            
            
    except:
        print("Error2 - The nastiest of errors")
    
        
    if debug:
        debug_frame = processedData.debug_frame 
        cv2.imshow('Original', debug_frame)
    
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
            ##end xd
            break
print('closing program')
processor.stop()
cv2.destroyAllWindows()

#if __name__ == "__maincam__":
#    maincam()
    
    
