import image_processor
import camera
import motion
import cv2
import time
import robot
import OWOkood

middle_x = 441

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
    ref = OWOkood.Referee_cmd_client()
    ref.open()
    last_msg = ""
    name = "Jackbot"

    try:
        while True:
            # has argument aligned_depth that enables depth frame to color frame alignment. Costs performance
            processedData = processor.process_frame(aligned_depth=False)
            try:
                msg = ref.get_cmd()
                if msg != last_msg and msg != None:
                        
                    print("Message:",msg["signal"])
                    last_msg = msg
                    if name in msg["targets"]:
                        if msg["signal"]=="start":
                            if msg["targets"][1] == name:
                                print("GOGOGOGOGOGOGO",msg["baskets"][1])
                                
                                state="findball"
                            elif msg["targets"][0] == name:
                                print("GOGOGOGOGOGOGO",msg["baskets"][0])
                                state="findball"
                        else:
                            print("STOOOOOP!")
                            state = "stopped"
            except:    
                print("no ref")

            # This is where you add the driving behaviour of your robot. It should be able to filter out
            # objects of interest and calculate the required motion for reaching the objects
            try:
                ballX=processedData.balls[-1].x
                ballY=processedData.balls[-1].y
                interesting_ball = processedData.balls[-1]
            except:
                print("Cant see a ball")
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
                #    break

            if debug:
                debug_frame = processedData.debug_frame

                cv2.imshow('debug', debug_frame)

                k = cv2.waitKey(1) & 0xff
                if k == ord('q'):
                    break

            try:
                if len(processedData.balls)<0:
                    print("State:",state, "Ball X:", processedData.balls[0].x,"Ball Y:", processedData.balls[0].y )
            except:
                pass
            if state == "stopped":
                print("stopped")
                time.sleep(0.5) 
                continue

            if state == "findball":
                ### robot tries to find ball
                try:
                    if len(processedData.balls)>0:
                        if processedData.balls[-1].x >= middle_x - 200 and processedData.balls[-1].x <= middle_x + 200:
                            ### robot found ball
                            state = "getclose"
                    robot.findaball(processedData)
                except:
                    print("findball error")


            elif state == "getclose":
                ### ball found get close
                try:
                    if ballY > 180:
                        
                        print("ORBITING")
                        time.sleep(1)
                        state = "orbit"
                        
                    elif len(processedData.balls) <= 0:
                        print("getclose->findball")
                        state = "findball"
                    else:
                        print("robot.getclose",ballX,ballY)
                        robot.getclose(ballX,ballY)
                except:
                    print("getclose error")
                if len(processedData.balls) <= 0:
                    state = "findball"


            elif state == "backthefoff": ## basket fall back xd
                try:
                    print(" STATE: backoff")
                    timertemp = 0
                    while timertemp < 200:
                        timertemp += 1
                        robot.backoff()
                    state = "findball"
                except:
                    print("backoff error")


            elif state == "makeshot":
                try:
                    
                    
                    try:
                        print("BASKET DISTANCE : ", processedData.basket_b.distance)
                        #if processedData.basket_b.distance <= 500:
                           # state = "backthefoff"
                        print(processedData.basket_b.x)
                    except:
                        print("Basket not found makeshot")
                    
                    print(" STATE: makeshoot")
                    if temptimer >= 150: # 140
                            state = "findball"
                    if temptimer >= 70: # 50
                        
                        robot.makeshot((processedData.basket_b.distance))
                    temptimer += 1
                except:
                    print("Makeshot error")


            elif state == "orbit":
                try:
                    try:
                        speed_x = -robot.controller(processedData.basket_b.x, middle_x, x_scale=1500, y_scale=(max_speed - 3))
                    except:
                        print("No basket")
                        speed_x=max_speed 

                    if len(processedData.balls) <= 0 or interesting_ball.y < 120:
                        print("Orbit: Ball lost. Finding new ball")
                        state = "findball"

                    

                    elif processedData.basket_b.x > middle_x - aimTolerance and processedData.basket_b.x < middle_x + aimTolerance:
                        print("making shot")
                        temptimer = 0
                        state = "makeshot"
                       
                    else:
                        print(speed_x,interesting_ball.distance,interesting_ball.x)
                        robot.orbit(200, speed_x, interesting_ball.distance, interesting_ball.x)

                except:
                    print("orbit error")

            else:
                #orbit basics
                if len(processedData.balls) == 0:
                    robot.state = "findball"
                
                ### hoovers aorund the ball
                #try:
                 #   if processedData.basket_b.size >= 18000:
                  #      robot.state = "backthefoff"
                #except:
                 #   print("Orbit error")




    except KeyboardInterrupt:
        print("closing....")
    finally:
        cv2.destroyAllWindows()
        processor.stop()
        #motion_sim.close()
        #motion_sim2.close()

main_loop()
