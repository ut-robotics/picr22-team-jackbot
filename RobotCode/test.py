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
    ref = OWOkood.Referee_cmd_client()
    ref.open()
    last_msg = ""
    name = "Jackbot"

    try:
        while True:
            # has argument aligned_depth that enables depth frame to color frame alignment. Costs performance
            time.sleep(1)
            processedData = processor.process_frame(aligned_depth=False)
            try:
                print("balli y", processedData.balls[-1].y, "palli x", processedData.balls[-1].x, "Dist bal", processedData.balls[-1].distance)
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
