import image_processor
import camera
import motion
import cv2
import time
import robot
import OWOkood

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
            time.sleep(1)
            processedData = processor.process_frame(aligned_depth=False)
            try:
                #print("palli y:", processedData.balls[-1].y, ", palli x:", processedData.balls[-1].x, ", Dist bal", processedData.balls[-1].distance)
                print(""processedData.basket_m.distance)
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