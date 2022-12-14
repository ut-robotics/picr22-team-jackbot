import numpy as np
import motion
import time
import camera

cam = camera.RealsenseCamera(exposure = 100)
camera_y = cam.rgb_height ##480 atm

class Robot():
    def __init__(self) -> None:
    
        self.middle_xbasket = 430
        self.fasttimer = 0
        self.prev_rad=250
        self.speed_y = 0
        self.speed_r = 0
        self.speed_x = 0
        self.motion_irl = motion.OmniMotionRobot()
        self.motion_irl.open()
        
        



    ### LISA FUNKTSIOONID ###
    def controller(self, current, target, x_scale = 1, y_scale = 1):
        return (2 / (1 + np.exp(3*(target-current)/x_scale)) - 1) * y_scale

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)




    ### MAIN FUNKTSIOONID ###
    def backoff(self):
        
        print(" STATE: backoff")
        self.motion_irl.move(0,-20,0,0)

    def orbit(self, radius, speed_x, cur_radius, cur_object_x, middle_x):
            if speed_x>0:
                speed_x=self.clamp(speed_x,4,60)
            if speed_x<0:
                speed_x=self.clamp(speed_x,-4,-60)
                
            speed_y = 0
            speed_r = 100 * speed_x / radius
            buffer_x = 2
            r_const = 3
            y_const = 1
            
        
            
            # Radius adjustment
            if cur_radius > (radius + buffer_x) or cur_radius < (radius - buffer_x):
                speed_y -= (radius - cur_radius) / 100 * y_const

            # Centering object, rotational speed adjustment
            if cur_object_x > (middle_x + buffer_x) or cur_object_x < (middle_x - buffer_x):
                speed_r += (middle_x - cur_object_x) / 100 * r_const

            print("robot:",int(speed_x), int(speed_y), int(speed_r))
            
            self.motion_irl.move(int(speed_x), int(speed_y), int(speed_r),0)


    def getclose(self, X, Y, middle_x):

        print("STATE: getclose")

        offcentre = (X - middle_x)
        t_speed = (offcentre/10)
        ###MATIKOOT
        Yslow = Y/6 #enne5.5
        ###MATIKUUT
        print("offcentre:", offcentre)
        if offcentre <= 300 and offcentre >= -300 and Y < camera_y*0.4167:
            self.motion_irl.move(int(t_speed),int(60-(abs(t_speed))),int(-t_speed/3),0)
            print("Full speed")
        else:
            self.motion_irl.move(int(t_speed/3),int((50-Yslow)),int(-t_speed/10),0)
            print("Slow down")


    def findaball(self, processedData):
        print(" STATE: findball")
        ### robot tries to find ball
        gofasttimer = time.time() ##900
        slowdowntimer = time.time()
        slowdownTimes = 0.05 ##setbyhand and needs
        
        try:
            if processedData.balls:
                self.fasttimer = 0
                
            if self.fasttimer >= 40:
                while slowdowntimer+slowdownTimes > time.time(): ##168
                    self.motion_irl.move(0,0, int(40 - ((slowdowntimer+slowdownTimes)-time.time())*(28/slowdownTimes)),0)
                while gofasttimer+0.14 > time.time(): ## setbyhand
                    self.motion_irl.move(0,0,40,0)
                    gofasttimer -= 1
                while slowdowntimer+slowdownTimes > time.time():
                    self.motion_irl.move(0,0, int(12 + ((slowdowntimer+slowdownTimes)-time.time())*(28/slowdownTimes)),0)

                self.fasttimer = 0
            else:
                self.motion_irl.move(0,0,12,0) 
        except:
            self.motion_irl.move(0,0,12,0) 

        self.fasttimer += 1


    def turn45(self): # x ja left 0 : right 1
        temptimer = time.time()
        while temptimer+0.075 >= time.time(): ## sekundites
            self.motion_irl.move(0,0,28,0)


    def makeshot(self, dist, basketx, timer, ballseen):     
        if dist <= 1450:
            throwdistance = (dist) * 0.192307 + 345 ### 338 old 
            print("Short shot")

        elif dist > 1450 and dist < 3200:
            throwdistance = (dist) * 0.15625 + 415 ### +400 last
            print("Mid shot")
        
        else:
            throwdistance = (dist) * 0.0952 + 620 ###bfr 590
            print("Long shot")
        ### old 0.18931 + 348.476439
        print("1")
        if timer == 2:
            ### change rotation so 3rd para to change how agressively it turns
            if basketx <= int(self.middle_xbasket)-1:### -1
                print("2")
                self.motion_irl.move(0,20,2,int(throwdistance))
            elif basketx >= int(self.middle_xbasket)+1: ### +1
                print("3")
                self.motion_irl.move(0,20,-2,int(throwdistance))
            else:
                self.motion_irl.move(0,20,0,int(throwdistance))
                print("4")
        else:
            if ballseen == 0:
                if basketx <= self.middle_xbasket-1:### sec-1
                    self.motion_irl.move(0,-6,2,0)
                elif basketx >= self.middle_xbasket+1:### sec+1
                    self.motion_irl.move(0,-6,-2,0)
                else:
                    pass
            else:
                if basketx <= self.middle_xbasket-1: ### sec-1
                    self.motion_irl.move(0,0,2,0)
                elif basketx >= self.middle_xbasket+1: ### sec+1
                    self.motion_irl.move(0,0,-2,0)
                else:
                    pass



