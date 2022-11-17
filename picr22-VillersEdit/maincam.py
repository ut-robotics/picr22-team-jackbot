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
    ### robot tries to find ball
    motion_irl.move(0,0,10,0)
    if processedData.balls[0].x >= centrex - 200 and processedData.balls[0].x <= centrex + 200:
        ### robot found ball
        state = "getclose"
        
        
def getclose():
    global state
    global randomcounter
    randomcounter += 1
    print("randomcounter", randomcounter)
    if len(processedData.balls) <= 0 and randomcounter >= 50:
        print("getclose debuig")
        randomcounter = 0
        state = "findball"

    if processedData.balls[0].x >= 250 and processedData.balls[0].x <= 600 and processedData.balls[0].y <= 245:
        if processedData.balls[0].x >= 425:
            notsoy = processedData.balls[0].y - 185
            notso = processedData.balls[0].x - 424
            print(notso)
            if notsoy > 0:
                motion_irl.move(int((notso/25)),int(((notso/9)+25)-notsoy/3),0,450)
            else:
                motion_irl.move(int((notso/25)+2),int((notso/9)+25),int(-(notso/45)-2),450)
        else:
            notso = processedData.balls[0].x
            notsoy = processedData.balls[0].y - 185
            print(notso)
            if notsoy > 0:
                motion_irl.move(int(-(notso/25)),int(((notso/9)+25)-notsoy/3),0,450)
            else:
                motion_irl.move(int(-(notso/25)-2),int((notso/9)+25),int((notso/45)+2),450)
#    offcentre = (processedData.balls[0].x - centrex)
#    t_speed = offcentre/5
#
#    print("offcentre:", offcentre)
#    if offcentre <= 435 and offcentre >= -435 and processedData[0].y < 390:
#        motion_irl.move(int(t_speed),int(-(t_speed/2)),int(t_speed/3),0)
        
    else:
        if processedData.balls[0].y >= 240:
            state = "ballcentered"
            print("makeshot")
        else:
            state = "findaball"
            print("findball")
        
        
        print(" back to looking for the ball xdddd")





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
            print("ballcentered xdddd")
            if len(processedData.balls) == 0:
                state = "findball"
            if processedData.balls[0].y >= 245:
                ###if ball is really close by y cordinate
                state = "putsis"
            else:
                
                ### move towards the ball really slowly
                motion_irl.move(0,5,0,0)
                print(processedData.balls[0].y)
            if processedData.balls[0].y <= 150:
                state = "findball"
        elif state == "angleshoot":
            print(processedData.basket_b.x)
            if processedData.basket_b.x <= 420:
                if processedData.basket_b.x >= 400 and processedData.basket_b.x <= 423:
                    motion_irl.move(2,0,2,0)
                else:
                    motion_irl.move(7,0,4,0)
            elif processedData.basket_b.x >= 428:
                if processedData.basket_b.x <= 448 and processedData.basket_b.x >= 423:
                    motion_irl.move(-2,0,-2,0)
                else:
                    motion_irl.move(-7,0,-4,0)
            else:
                state = "makeshot"
                motion_irl.move(0,0,0,0)
                print("shoot")
                ##shoot
                temptimer = 0

        elif state == "backthefoff": ## basket fall back xd
            timertemp = 0
            while timertemp < 50:
                timertemp += 1
                motion_irl.move(0,-10,5,0)
            state = "findball"

        elif state == "makeshot":
            print("shoot")
            print(processedData.basket_b.size)
            if processedData.basket_b.size >= 18000:
                state = "backthefoff"
            temptimer += 1
            print(processedData.basket_b.x)
            if len(processedData.balls) <= 0:
                if temptimer >= 112:
                        state = "findball"
                if temptimer >= 30:
                    ##check distance ?
                    motion_irl.move(0,15,0,1000)
            else:
                state = "findball"


        else:
            #orbit basics
            if len(processedData.balls) == 0:
                state = "findball"
            print("basketb size, ", processedData.basket_b.size)
            ### hoovers aorund the ball
            if processedData.balls[0].y > 236:
                if processedData.balls[0].x > 423:
                    motion_irl.move(15,3,5,0)
                else:
                    motion_irl.move(5,3,5,0)
            elif processedData.balls[0].y < 236:
                if processedData.balls[0].x > 425:
                    motion_irl.move(5,-3,5,0)
                else:
                    motion_irl.move(15,-3,5,0)
            else:
                motion_irl.move(0,0,10,0)
            ##find magneta or blu
            if processedData.basket_b.x >= 300 and processedData.basket_b.x <= 548:
                state = "angleshoot"
            if processedData.basket_b.size >= 18000:
                state = "backthefoff"
            print(processedData.basket_b.x)
            print("putsis @debug message@")
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
    
    
