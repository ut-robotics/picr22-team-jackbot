print("xd")
import image_processor
print("xd2")
import camera
print("xd3")
import motion
print("xd4")
import cv2
import time
import robot
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
print("xd22222")
middle_x = 435

def main_loop():
    debug = False

    #motion_sim = motion.TurtleRobot()
    #motion_sim2 = motion.TurtleOmniRobot()
    
    #camera instance for normal web cameras
    #cam = camera.OpenCVCamera(id = 2)
    # camera instance for realsense cameras
    cam = camera.RealsenseCamera(exposure = 100)

    
    processor = image_processor.ImageProcessor(cam, debug=debug)

    processor.start()
 
    #motion_sim.open()
    #motion_sim2.open()

    start = time.time()
    fps = 0
    frame = 0
    frame_cnt = 0
    motion_irl = motion.OmniMotionRobot()
    motion_irl.open()
    distance1 = 0
    distance2 = 0
    distance3 = 0
    distance4 = 0
    distance5 = 0
    distance6 = 0
    distance7 = 0
    print("inloop23333")
    try:
        try:
            while True:
                try:
                    processedData = processor.process_frame(aligned_depth=False)

                    distance7 = distance6
                    distance6 = distance5
                    distance5 = distance4
                    distance4 = distance3
                    distance3 = distance2
                    distance2 = distance1
                    distance1 = processedData.basket_b.distance
                    distancebase = int(distance1+distance2+distance3+distance4+distance5+distance6+distance7)/7
                    motion_irl.move(0,0,0, 1100)
                    print("basket distance: ",distancebase)
                    
                except:
                    print("mitte nii putsis")
        except:
            print("cap")
            return

    except KeyboardInterrupt:
        print("closing....")

try:
    print("loop start")
    main_loop()
except:
    print("oof")