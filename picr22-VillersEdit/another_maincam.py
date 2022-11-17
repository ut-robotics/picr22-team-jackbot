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

    if len(processedData.balls) > 0 and processedData.balls[0].y <= 240:

        offcentre = (processedData.balls[0].x - centrex)
        t_speed = (offcentre/10)
        ###MATIKOOT
        Yslow = processedData.balls[0].y/6.66
        ###MATIKUUT
        print("offcentre:", offcentre)
        if offcentre <= 400 and offcentre >= -400 and processedData.balls[0].y < 200:
            motion_irl.move(int(t_speed),int(50-(abs(t_speed))),int(-t_speed/3),0)
        else:
            motion_irl.move(int(t_speed/3),int((50-Yslow)),int(-t_speed/10),0)
    else:
        if processedData.balls[0].y > 200:
            print("MAKING SHOT")
            time.sleep(1)
            state = "orbit"
            
        else:
            state = "findaball"
            print("findball")
 

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
    print(" STATE: makeshoot")
    print(processedData.basket_b.size)
    if processedData.basket_b.size >= 18000:
        state = "backthefoff"
    temptimer += 1
    print(processedData.basket_b.x)

    if temptimer >= 76:
            state = "findball"
    if temptimer >= 30:
        motion_irl.move(0,30,0,1000)







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
        print("Ball X:", processedData.balls[0].x,"Ball Y:", processedData.balls[0].y , " Basket Y:",  processedData.basket[0].y)
    except:
        print("Error1")

    try:
        if len(processedData.balls)<0:
            print("State:",state, "Ball X:", processedData.balls[0].x,"Ball Y:", processedData.balls[0].y )

        if state == "findball":
            ### robot tries to find ball
            findaball()

        elif state == "getclose":
            ### ball found get close
            getclose()

        elif state == "ballcentered":
            ballcentred()

        elif state == "angleshoot":
            angleshot()

        elif state == "backthefoff": ## basket fall back xd
            backoff()

        elif state == "makeshot":
            makeshot()

        elif state == "orbit":
            orbit()
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
        print("Error2")
    
        
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
    
    
