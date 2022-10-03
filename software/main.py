import image_processor
import camera
import motion
import cv2
import time
import struct
import threading
from threading import Thread


def main_loop():
    state = "findball"
    debug = True
    
    ## task testing ########################################
    Thread(target=motion.movelogic()).start()
    
    ########################################################
    
    #motion_sim = motion.TurtleRobot()
    
    # not needed atm########################
    #motion_sim2 = motion.TurtleOmniRobot()
    motion_irl = motion.OmniMotionRobot()
    
    # instance for normal web cameras
    #cam = camera.OpenCVCamera(id = 2)
    #camera instance for realsense cameras
    ########################################
    
    cam = camera.RealsenseCamera()
    
    processor = image_processor.ImageProcessor(cam, debug=debug)

    processor.start()
    #motion_sim.open()
    
     # not needed atm
    #motion_sim2.open()
    motion_irl.open()
     ################

    start = time.time()
    fps = 0
    frame = 0
    frame_cnt = 0
    try:
        while True:
            # has argument aligned_depth that enables depth frame to color frame alignment. Costs performance
            processedData = processor.process_frame(aligned_depth=False)

            # This is where you add the driving behaviour of your robot. It should be able to filter out
            # objects of interest and calculate the required motion for reaching the objects

            frame_cnt +=1
            
            frame += 1
            if frame % 30 == 0:
                frame = 0
                end = time.time()
                fps = 30 / (end - start)
                start = end
                print("FPS: {}, framecount: {}".format(fps, frame_cnt))
                print("ball_count: {}".format(len(processedData.balls)))
                #if (frame_cnt > 1000):
                   # break
            try:
                print(processedData.balls[0].size)
            except:
                pass
            
            #print(processedData.balls[0])
            
            ###main tests here
            try:
                if state == "findball":
                    ### robot tries to find ball
                    motion.turn(0)
                    if processedData.balls[0].x >= 200 or processedData.balls[0].x <= 640:
                        ### robot found ball
                        state = "getclose"
                elif state == "getclose":
                    ### robot is in driving mode towards the ball hopefully xd
                    ## change speed depending on size
                    if processedData.balls[0].x <= 390:
                        if processedData.balls[0].x >= 200:
                            motion.turndrive(0)
                        else:
                            motion.turn(0)
                            
                    elif processedData.balls[0].x >= 450:
                        if processedData.balls[0].x <= 640:
                            motion.turndrive(1)
                        else:
                            motion.turn(1)
                            
                    else:
                        ### if ball is centered stop moving change later.
                        ### check how far the ball is in reality.
                        print("looking at the ball xdddd")
            except:
                pass    

            ## deafult send info
#             disable_failsafe = 0
#             command1 = struct.pack('<hhhHBH', 20, 0, -20, 0, disable_failsafe, 0xAAAA)
#             motion.OmniMotionRobot.send(motion_irl, command1)

                        
            
            if debug:
                debug_frame = processedData.debug_frame

                #cv2.imshow('debug', debug_frame) 

                k = cv2.waitKey(1) & 0xff
                if k == ord('q'):
                    break
    except KeyboardInterrupt:
        print("closing....")
    finally:
    #    cv2.destroyAllWindows()
        processor.stop()
        #motion_sim.close()
        # not needed
        #motion_sim2.close()
        ####################
        
main_loop()