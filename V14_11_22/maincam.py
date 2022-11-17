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
state = "findball"
motion_irl = motion.OmniMotionRobot()
motion_irl.open()


####
##motion_irl.move()

# def set_segmentation_table(table):
#     segment.set_table(table)
# 
# color_config = "colors/colors.pkl"
# with open(color_config, 'rb') as conf:
#     colors_lookup = pickle.load(conf)
#     set_segmentation_table(colors_lookup)
# 
# fragmented = np.zeros((1920, 1080), dtype=np.uint8)
# t_balls = np.zeros((1920, 1080), dtype=np.uint8)
# t_basket_b = np.zeros((1920, 1080), dtype=np.uint8)
# t_basket_m = np.zeros((1920, 1080), dtype=np.uint8)

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
    if processedData.balls[0].x >= 100 or processedData.balls[0].x <= 740:
        ### robot found ball
        state = "getclose"
        
def getclose():
    global state
    if len(processedData.balls) == 0:
        print("getclose debuig")
        state = "findball"
    if processedData.balls[0].y >= 335:
        state = "ballcentered"
#             try:
    ### robot is in driving mode towards the ball hopefully xd
    ## change speed depending on size
    if processedData.balls[0].x <= 419:
        
        if processedData.balls[0].x >= 100 and processedData.balls[0].x < 200:
            print("turning left semi hard")
            motion_irl.move(-50,20,10,0)
        elif processedData.balls[0].x >= 200 and processedData.balls[0].x <= 300:
            print("turning left kind of straight")
            motion_irl.move(-20,35,5,0)
        elif processedData.balls[0].x >= 300 and processedData.balls[0].x < 420:
            print("turning left kind of straight")
            motion_irl.move(-15,20,1,0)
        else:
            print("turning left vaga hard")
            motion_irl.move(0,0,25,0)
            
    elif processedData.balls[0].x >= 421:
        if processedData.balls[0].x <= 740 and processedData.balls[0].x > 640:
            print("turning right semi hard")
            motion_irl.move(50,20,-10,0)
        elif processedData.balls[0].x <= 640 and processedData.balls[0].x >= 520:
            print("turning right kind of straight")
            motion_irl.move(20,35,-5,0)
        elif processedData.balls[0].x <= 520 and processedData.balls[0].x > 420:
            print("turning right kind of straight")
            motion_irl.move(15,20,-1,0)
        else:
            print("turning right really hard")
            motion_irl.move(0,0,-25,0)
        
    else:
        motion_irl.move(0,5,0,0)
        
        ### if ball is centered stop moving change later.
        ### check how far the ball is in reality.
        print("looking at the ball xdddd")
#             except:
#                 print("FINDBALL EXCEPT")
#                 ## ball is out of view gives error starts
#                 #looking for the ball again xdd
#                 #state == "findball"


'''blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByArea = True
blobparams.minArea = 30
blobparams.maxArea = 80000
blobparams.filterByCircularity = False
#blobparams.minCircularity = 0.1
blobparams.minDistBetweenBlobs = 25
blobparams.filterByInertia = False
#blobparams.minInertiaRatio = 0.5
blobparams.filterByConvexity = False
#blobparams.minConvexity = 0.5
'''
detector = cv2.SimpleBlobDetector_create(blobparams)

# Open the camera
cam = camera.RealsenseCamera()
#cap = cv2.VideoCapture(4)
#width = 180#320#640#1280
#height = 90#180#360#720
#cap.set(3,1280)
#cap.set(4,720)
#cap.set(cv2.CAP_PROP_FPS, 60)

#width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
#height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
# limit width
#width_center = width/2
#height_center = height/2
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
        print(processedData.balls[0].size, processedData.balls[0].x, processedData.balls[0].y , " basket ",  processedData.basket[0].y)
    except:
        pass
#     
#     print("magneto, ", processedData.basket_m)
#     print("blu, ", processedData.basket_b)
    
    # Read the image from the camera
    #ret, frame = cap.read()
    #frame_bgr = frame.copy()
    #frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Our operations on the frame come here
#     thresholded_basgeto = np.invert(cv2.inRange(frame_hsv, lowerLimits_basgeto, upperLimits_basgeto))
#     thresholded_ball = np.invert(cv2.inRange(frame_hsv, lowerLimits_ball, upperLimits_ball))
# 
#     thresholded_basgeto = white_edge(thresholded_basgeto)
#     keypoint_basgeto = detector.detect(thresholded_basgeto)
#     keypoint_ball = detector.detect(thresholded_ball)
#     img = frame_bgr.copy()
#     img = cv2.drawKeypoints(img, keypoint_basgeto, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#     img = cv2.drawKeypoints(img, keypoint_ball, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#
    
    #motion_irl.move(0,0,0)

#     all_objects = list_objects(keypoint_ball)
#     if len(all_objects) > 0:
#         #print(len(all_objects))
#         all_objects = sort_size(all_objects)
#         #print(all_objects)
#         
#         biggest_obj = all_objects[0]
#         close_xy = biggest_obj[0:2]
#         close_size = biggest_obj[2]

        # show line to the biggest object
#         img = cv2.arrowedLine(img, (int(width_center), int((height_center)+340)), close_xy, (0, 255, 255), 3)
    
    try:
        print(state)
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
            if processedData.balls[0].y >= 340:
                ###if ball is really close by y cordinate
                state = "putsis"
            else:
                
                ### move towards the ball really slowly
                motion_irl.move(0,5,0,0)
                print(processedData.balls[0].y)
            if processedData.balls[0].y <= 200:
                state = "findball"
        elif state == "angleshoot":
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

            if temptimer >= 76:
                    state = "findball"
            if temptimer >= 30:
                motion_irl.move(0,30,0,1000)


        else:
            #orbit basics
            if len(processedData.balls) == 0:
                state = "findball"
            print(processedData.basket_b.size)
            ### hoovers aorund the ball
            if processedData.balls[0].y > 300:
                if processedData.balls[0].x > 424:
                    motion_irl.move(15,3,5,0)
                else:
                    motion_irl.move(5,3,5,0)
            elif processedData.balls[0].y < 548:
                if processedData.balls[0].x > 424:
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
        pass
    
        
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
    
    
