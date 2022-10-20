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
    

blobparams = cv2.SimpleBlobDetector_Params()
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
debug = True
processor = image_processor.ImageProcessor(cam, debug=debug) #, debug=debug
processor.start()
cv2.namedWindow("Original") # do not delete, used to quit the program
while True:
    processedData = processor.process_frame(aligned_depth=False)
    
#     contours, hierarchy = cv2.findContours(t_balls, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    try:
        print(processedData.balls[0].size, processedData.balls[0].x, processedData.balls[0].y)
    except:
        pass
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
    
    

#     all_objects = list_objects(keypoint_ball)
#     if len(all_objects) > 0:
#         #print(len(all_objects))
#         all_objects = sort_size(all_objects)
#         #print(all_objects)
#         
#         biggest_obj = all_objects[0]
#         close_xy = biggest_obj[0:2]
#         close_size = biggest_obj[2]


#         ###KPPID
#         x = close_xy[0]
#         y = close_xy[1]
#         dist = np.sqrt(np.power(width_center_new-x,2)+np.power(height_center_new-y,2))
#         
#         if close_xy[0] < width_center_new:
#             dist = dist*(-1)
# 
#         obj_loc = -((x-width_center_new)/width_center_new)    
# 
#         kp = 35.0 # increase proportionality constan (kp) to make turning stronger
#         # the linelocation value already shows error (location-center)
#         e = obj_loc # error of movement
#         Pout = kp*e
#         ###KPPID END
        
        # show line to the biggest object
#         img = cv2.arrowedLine(img, (int(width_center), int((height_center)+340)), close_xy, (0, 255, 255), 3)
    
    
    try:
        
        if state == "findball":
            ### robot tries to find ball
            motion_irl.move(0,0,10)
            if processedData.balls[0].x >= 100 or processedData.balls[0].x <= 740:
                ### robot found ball
                state = "getclose"
        elif state == "getclose":
            if processedData.balls[0].y >= 335:
                state = "ballcentered"
#             try:
            ### robot is in driving mode towards the ball hopefully xd
            ## change speed depending on size
            if processedData.balls[0].x <= 419:
                
                if processedData.balls[0].x >= 100 and processedData.balls[0].x < 200:
                    print("pooran vasakule semi hard")
                    motion_irl.move(-40,15,10)
                elif processedData.balls[0].x >= 200 and processedData.balls[0].x <= 300:
                    print("pooran vasakule kind of otse")
                    motion_irl.move(-15,30,5)
                elif processedData.balls[0].x >= 300 and processedData.balls[0].x < 420:
                    print("pooran vasakule kind of otse")
                    motion_irl.move(-10,20,1)
                else:
                    print("pooran vasakule vaga hard")
                    motion_irl.move(0,0,20)
                    
            elif processedData.balls[0].x >= 421:
                if processedData.balls[0].x <= 740 and processedData.balls[0].x > 640:
                    print("pooran paremale semi hard")
                    motion_irl.move(40,15,-10)
                elif processedData.balls[0].x <= 640 and processedData.balls[0].x >= 520:
                    print("pooran paremale kind of otse")
                    motion_irl.move(15,30,-5)
                elif processedData.balls[0].x <= 520 and processedData.balls[0].x > 420:
                    print("pooran paremale kind of otse")
                    motion_irl.move(10,20,-1)
                else:
                    print("pooran paremale vaga hard")
                    motion_irl.move(0,0,-20)
                
            else:
                motion_irl.move(0,5,0)
                
                ### if ball is centered stop moving change later.
                ### check how far the ball is in reality.
                print("looking at the ball xdddd")
#             except:
#                 print("FINDBALL EXCEPT")
#                 ## ball is out of view gives error starts
#                 #looking for the ball again xdd
#                 #state == "findball"
        elif state == "ballcentered":
            print("ballcentered xdddd")
            if processedData.balls[0].y >= 340:
                state = "putsis"
            else:
                motion_irl.move(0,5,0)
        else:
            motion_irl.move(10,0,5)
            print("putsis")
    except:
        print("vittus")
        pass
    try:
        if all_objects[0][2] >= 100:
            state = "ballcentered"
    except:
        pass
    #STRAIGHT PID TRY632
    
    
        
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
    
    
