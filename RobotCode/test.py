import image_processor
import camera
import motion
import cv2
import time
import robot
import OWOkood
import time
middle_xbasket = 424
motion_irl = motion.OmniMotionRobot()
motion_irl.open()

def makeshot(dist, basketx, timer):     
    if dist <= 1450:
        throwdistance = (dist) * 0.192307 + 360 ### 338 old 
        print("Short shot")

    elif dist > 1450 and dist < 3200:
        throwdistance = (dist) * 0.15625 + 430 ### +400 last
        print("Mid shot")
    
    else:
        throwdistance = (dist) * 0.0952 + 620 ###bfr 590
        print("Long shot")
    ### old 0.18931 + 348.476439
    print("1")
    if timer == 2:
        ### change rotation so 3rd para to change how agressively it turns
        if basketx <= int(middle_xbasket)-1:### -1
            print("2")
            motion_irl.move(0,20,2,int(throwdistance))
        elif basketx >= int(middle_xbasket)+1: ### +1
            print("3")
            motion_irl.move(0,20,-2,int(throwdistance))
        else:
            motion_irl.move(0,20,0,int(throwdistance))
            print("4")
    else:
        if basketx <= middle_xbasket-1: ### sec-1
            motion_irl.move(0,0,2,0)
        elif basketx >= middle_xbasket+1: ### sec+1
            motion_irl.move(0,0,-2,0)
        else:
            pass

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

    
    max_speed = 60
    aimTolerance=20

    state = "stopped"
    
    last_msg = ""
    name = "Jackbot"

    try:
        while True:
            
            # has argument aligned_depth that enables depth frame to color frame alignment. Costs performance
            time.sleep(0.5)
            processedData = processor.process_frame(aligned_depth=False)
            temptimer = 0
            x = input("Wait insert 0 or 1: ")
            try:
                while x == "1":
                    print("x is : ", x, " temptimer is : ", temptimer)
                    
                    try:
                        processedData = processor.process_frame(aligned_depth=False)
                        if temptimer >= 200:
                            x = "0"
                        if temptimer >= 100: # 90f
                            print("f")
                            makeshot(processedData.basket_m.distance, processedData.basket_m.x, 2)
                        if temptimer >= 5 and temptimer < 100: # 85sec
                            makeshot(processedData.basket_m.distance, processedData.basket_m.x, 1)
                        temptimer += 1
                        makeshot(processedData.basket_m.distance, processedData.basket_m.x)
                    except:
                        print("error overhere")
            except:
                print("error")
            
            try:
                print(processedData.basket_b.distance)
            
            except:
                print("No basket")




    except KeyboardInterrupt:
        print("closing....")
    finally:
        cv2.destroyAllWindows()
        processor.stop()
        #motion_sim.close()
        #motion_sim2.close()

main_loop()

# oribitng with swerve
#try:
# 
#                            tempbally = 0
#                            closestbally = 0
#                            closestballx = 0
#                            for i in processedData.balls:
#                                i.y = tempbally
#                                if tempbally >= closestbally:
#                                    closestbally = tempbally
#                                    closestballx = i.x
#
#                            if closestballx > (middle_x + orbit_ball_tolerance):
#                                print("Swerve RIGHT")
#                                if slowtimer >= 1800:
#                                    robot.swerve(closestballx,1)
#                                    slowtimer = 0
#                                else:
#                                    print(speed_x,interesting_ball.distance,interesting_ball.x)
#                                    robot.orbit(200, speed_x, ballY, ballX)
#                                pass
#
#                            elif closestballx < (middle_x - orbit_ball_tolerance):
#                                print("Swerve LEFT")
#                                if slowtimer >= 1800:
#                                    robot.swerve(closestballx,0)
#                                    slowtimer = 0
#                                else:
#                                    print(speed_x,interesting_ball.distance,interesting_ball.x)
#                                    robot.orbit(200, speed_x, ballY, ballX)
#                                pass
#                            else:        
#                                print(speed_x,interesting_ball.distance,interesting_ball.x)
#                                robot.orbit(200, speed_x, ballY, ballX)
#                        except:
#                            print(speed_x,interesting_ball.distance,interesting_ball.x)
#                            robot.orbit(200, speed_x, ballY, ballX)