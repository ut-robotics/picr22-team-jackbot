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

centrex = 430
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
    motion_irl.move(0,0,10)
    if processedData.balls[0].x >= 100 or processedData.balls[0].x <= 740:
        ### robot found ball
        state = "getclose"
        
def controller(current, target, x_scale = 1, y_scale = 1):
    return (2 / (1 + np.exp(3*(target-current)/x_scale)) - 1) * y_scale


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

debug = False
processor = image_processor.ImageProcessor(cam, debug=debug) #, debug=debug
processor.start()

r_const = 5
y_const = 1
prev_rad = 400

#cv2.namedWindow("Original") 
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def orbit(self, radius, speed_x, cur_radius, cur_object_x):
        speed_y = 0
        speed_r = 1000 * speed_x / radius

        # Correct radius check
        if cur_radius > 600:
            self.logger.LOGE("Invalid radius, radius: " + str(cur_radius))
            return

        # Radius adjustment
        if cur_radius > (radius + self.buffer_x) or cur_radius < (radius - self.buffer_x):
            speed_y -= (radius - cur_radius) / 100 * self.y_const

        # Centering object, rotational speed adjustment
        if cur_object_x > (self.middle_x + self.buffer_x) or cur_object_x < (self.middle_x - self.buffer_x):
            speed_r += (self.middle_x - cur_object_x) / 100 * self.r_const
        #self.logger.LOGI("orbit speeds x: " + str(speed_x) + " y: " + str(speed_y) + " r: " + str(speed_r) + " cur_object_x: " + str(cur_object_x))

        #print("x:", speed_x, "y:", speed_y, "r:", speed_r, "cur_rad:", cur_radius, "cur_x:", cur_object_x)
        motion_irl.move(speed_x, speed_y, speed_r)
        self.prev_rad = cur_radius

while True:
    
    ########################
    ########################
    #find baskets by processedata
    #find balls , black line by blob
    ########################
    ########################
    processedData = processor.process_frame(aligned_depth=True)
    ########################
    ########################
#     contours, hierarchy = cv2.findContours(t_balls, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_speed = 10
    try:
        print("0::" ,processedData.balls[0].y,"-1::", processedData.balls[-1].y)
        
        speed_x = -controller(processedData.basket_b, centrex, x_scale=1500, y_scale=(max_speed - 3))

        orbit(400, speed_x, processedData.balls[-1].y, processedData.balls[-1].x)
        
    
    except:
        print("NO BALL")
        motion_irl.move(0,0,0,100)
    #debug_frame = processedData.debug_frame 
    #cv2.imshow('Original', debug_frame)

    try:
        debug_frame = processedData.debug_frame 
        #cv2.imshow('Original', debug_frame)
    except:
        print("cam except")
    
print('closing program')
processor.stop()
cv2.destroyAllWindows()

#if __name__ == "__maincam__":
#    maincam()
    
    
