import image_processor
import camera
import motion
import time
import robot
import OWOkood
import enum
import Color
import cv2

class State(enum.Enum):
    STOPPED = 0
    FINDBALL = 1
    GETCLOSE = 2
    ORBIT = 3
    MAKESHOT = 4
    
def main_loop():
    debug = False
    middle_x = 428
    ref_enable = False
    orbit_max_speed = 60
    aim_tolerance = 8
    find_ball_tolerance = 200

    frame = 0
    frame_cnt = 0
    fps = 0
    cam = camera.RealsenseCamera(exposure = 100)
    processor = image_processor.ImageProcessor(cam, debug=debug)
    processor.start()

    start = time.time()


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
            
            if debug:
                debug_frame = processedData.debug_frame
                cv2.imshow('debug', debug_frame)
                k = cv2.waitKey(1) & 0xff
                if k == ord('q'):
                    break
            

            ### Ref command read
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
                                print("Command: STOP")
                                state = State.STOPPED
                except:    
                    print("NO REF")
            
            ### Select basket
            if targetBasket == Color.Color.BLUE:
                ibasket = processedData.basket_b
            else:
                ibasket = processedData.basket_m
            

            ### Shorten stuff / Print ball location
            try:
                ballX=processedData.balls[-1].x
                ballY=processedData.balls[-1].y
                print("Ball   X:",ballX," Y:",ballY)
            except:
                print("Cant see a ball")
            
            
            ##### STATEMACHINE #####

            if state == State.STOPPED:
                print("stopped")
                time.sleep(0.5) 
                continue


            ### SPINN UNTIL BOT SEES BALL ###
            elif state == State.FINDBALL:
                ### robot tries to find ball
                try:
                    if len(processedData.balls)>0:
                        if ballX >= middle_x - find_ball_tolerance and ballX <= middle_x + find_ball_tolerance:
                            ### robot found ball
                            state = State.GETCLOSE
                            print("findball->getclose")
                    robot.findaball(processedData)

                except:
                    print("findball error")


            ### GET CLOSE TO THE BALL ###
            elif state == State.GETCLOSE:
                try:
                    if ballY > 250:
                        try:
                            if ibasket.distance < 700 and ibasket.distance>0:
                                print("BASKET TOO CLOSE!!!!")
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
                        robot.getclose(ballX,ballY,middle_x)

                except:
                    print("getclose error")

                if len(processedData.balls) <= 0:
                    print("getclose->findball")
                    state = State.FINDBALL


            ### ORBIT AROUND THE BALL UNTILL BASKET CENTERED ###
            elif state == State.ORBIT:
                try:
                    print("Orbiting")
                    try:
                        speed_x = -robot.controller(ibasket.x, middle_x, x_scale=1500, y_scale=(orbit_max_speed - 5))
                    except:
                        print("No basket")
                        speed_x = orbit_max_speed

                    if ibasket.x > middle_x - aim_tolerance and ibasket.x < middle_x + aim_tolerance:
                        print("making shot")
                        temptimer = 0
                        state = State.MAKESHOT

                    elif len(processedData.balls) <= 0 or ballY < 200:
                        print("Orbit: Ball lost. Finding new ball")
                        state = State.FINDBALL
                    
                    else:
                        print(speed_x,ballY,ballX)
                        robot.orbit(200, speed_x, ballY, ballX, middle_x)

                except:
                    print("orbit error")


            ### SHOOT BALL TWOARDS THE BASKET ###
            elif state == State.MAKESHOT:
                try:
                    try:
                        print("BASKET DISTANCE : ", ibasket.distance)
                        print(ibasket.x)
                        try:
                            if ibasket.distance < 700 and ibasket.distance>0:
                                print("BASKET TOO CLOSE")
                                robot.turn45()
                                print("makeshot->findball")
                                state = State.FINDBALL
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

