import image_processor
import camera
import motion
import cv2
import time
import robot
import OWOkood
import enum
import Color

class State(enum.Enum):
    STOPPED = 0
    FINDBALL = 1
    GETCLOSE = 2
    ORBIT = 3
    MAKESHOT = 4

    
middle_x = 428
ref_enable = False
def main_loop():
    debug = False
    cam = camera.RealsenseCamera(exposure = 100)
    processor = image_processor.ImageProcessor(cam, debug=debug)
    processor.start()

    start = time.time()
    
    slowtimer = 0
    fps = 0
    frame = 0
    frame_cnt = 0
    max_speed = 60
    aimTolerance = 8
    orbit_ball_tolerance = 160

    if ref_enable == True:
        state = State.STOPPED
        ref = OWOkood.Referee_cmd_client()
        ref.open()
    else:
        state=State.FINDBALL

    last_msg = ""
    name = "jackbot"

    targetBasket=Color.Color.MAGENTA

    try:
        while True:
            # has argument aligned_depth that enables depth frame to color frame alignment. Costs performance
            processedData = processor.process_frame(aligned_depth=False)
            if ref_enable == True:
                try:
                    #msg = { "signal": "start" , "targets": ["Jackbot","Jackbot"] , "baskets": ["blue","magneta"] }
                    msg = ref.get_cmd()
                    if msg != last_msg and msg != None:
                            
                        print("Message:",msg)
                        last_msg = msg
                        command_index = msg["targets"].index(name)
                        if command_index > -1:
                            command=msg["signal"]

                            if command=="start":
                                targetBasket = Color.Color.MAGENTA if msg["baskets"][command_index] == "magenta" else Color.Color.BLUE
                                state=State.FINDBALL
                            
                            else:
                                print("STOOOOOP!")
                                state = State.STOPPED
                except:    
                    print("no ref")
            
            if targetBasket == Color.Color.BLUE:
                ibasket = processedData.basket_b
            else:
                ibasket = processedData.basket_m
            

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
                print("state:", state, state == State.FINDBALL)
                #if (frame_cnt > 1000):
                #    break
            print("bfr debug")
            if debug:
                debug_frame = processedData.debug_frame
                cv2.imshow('debug', debug_frame)
                k = cv2.waitKey(1) & 0xff
                if k == ord('q'):
                    break
            print("bfr len proc")
            try:
                if len(processedData.balls)<0:
                    print("State:",state, "Ball X:",ballX,"Ball Y:", ballY )
            except:
                pass
            print("bfr stopped ")

            if state == State.STOPPED:
                print("stopped")
                time.sleep(0.5) 
                continue

            elif state == State.FINDBALL:
                ### robot tries to find ball
                try:
                    print("fb1")
                    if len(processedData.balls)>0:
                        print("fb2")
                        if ballX >= middle_x - 200 and ballX <= middle_x + 200:
                            ### robot found ball
                            print("fb3")
                            state = State.GETCLOSE
                    print("fb4")        
                    robot.findaball(processedData)
                except:
                    print("findball error")


            elif state == State.GETCLOSE:
                ### ball found get close
                try:
                    if ballY > 250:
                        try:
                            if ibasket.distance < 700 and ibasket.distance>0:
                                print("BASKET TOO CLOSE")
                                robot.turn45()
                            else:    
                                print("getclose->orbit")
                                state = State.ORBIT
                        except:
                               
                            print("getclose->orbit")
                            state = State.ORBIT
                        
                    elif len(processedData.balls) <= 0:
                        print("getclose->findball")
                        state = State.FINDBALL

                    else:
                        print("robot.getclose",ballX,ballY)
                        robot.getclose(ballX,ballY)

                except:
                    print("getclose error")

                if len(processedData.balls) <= 0:
                    state = State.FINDBALL


            elif state == State.MAKESHOT:
                try:
                    try:
                        print("BASKET DISTANCE : ", ibasket.distance)
                        print(ibasket.x)
                        try:
                            if ibasket.distance < 700 and ibasket.distance>0:
                                print("BASKET TOO CLOSE")
                                robot.turn45()
                                state=State.FINDBALL
                        except:
                            pass
                    except:
                        print("Basket not found makeshot")

                    ballseen = 0
                    try:
                        if ballY >= 250 and ballY <= 350:####second 310
                            ballseen = 1
                    except:
                        pass

                    
                    if temptimer >= 155: # 170f
                        print("makeshoot->findball")
                        state = State.FINDBALL

                    elif temptimer >= 55: # 90f
                        print("f")
                        robot.makeshot(ibasket.distance, ibasket.x, 2, ballseen)
                    if temptimer >= 5 and temptimer < 55: # 85sec
                        robot.makeshot(ibasket.distance, ibasket.x, 1, ballseen)
                    temptimer += 1
                except:
                    print("Makeshot error")


            elif state == State.ORBIT:
                try:
                    print("Orbiting")
                    try:
                        speed_x = -robot.controller(ibasket.x, middle_x, x_scale=1500, y_scale=(max_speed - 5))
                    except:
                        print("No basket")
                        speed_x=max_speed

                    if ibasket.x > middle_x - aimTolerance and ibasket.x < middle_x + aimTolerance:
                        print("making shot")
                        temptimer = 0
                        state = State.MAKESHOT

                    elif len(processedData.balls) <= 0 or ballY < 200:
                        print("Orbit: Ball lost. Finding new ball")
                        state = State.FINDBALL
                    
                       
                    else:
                        print(speed_x,interesting_ball.distance,interesting_ball.x)
                        robot.orbit(200, speed_x, interesting_ball.distance, interesting_ball.x)

                except:
                    print("orbit error")

            else:
                #orbit basics
                if len(processedData.balls) == 0:
                    state = State.FINDBALL




    except KeyboardInterrupt:
        print("closing....")
    finally:
        cv2.destroyAllWindows()
        processor.stop()
        #motion_sim.close()
        #motion_sim2.close()

main_loop()

