import numpy as np
import motion



#middle_x = 430
middle_xbasket = 424
fasttimer = 0
prev_rad=250
speed_y = 0
speed_r = 0
speed_x = 0

motion_irl = motion.OmniMotionRobot()
motion_irl.open()
state = "findball"


### LISA FUNKTSIOONID ###
def controller(current, target, x_scale = 1, y_scale = 1):
    return (2 / (1 + np.exp(3*(target-current)/x_scale)) - 1) * y_scale

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def stop():
    motion_irl(0,0,0,0)



### MAIN FUNKTSIOONID ###
def backoff():
     
    print(" STATE: backoff")
    motion_irl.move(0,-20,0,0)

def orbit(radius, speed_x, cur_radius, cur_object_x, middle_x):
        if speed_x>0:
            speed_x=clamp(speed_x,4,60)
        if speed_x<0:
            speed_x=clamp(speed_x,-4,-60)
            
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
        
        motion_irl.move(int(speed_x), int(speed_y), int(speed_r),0)


def getclose(X,Y,middle_x):

    print("STATE: getclose")

    offcentre = (X - middle_x)
    t_speed = (offcentre/10)
    ###MATIKOOT
    Yslow = Y/5.5
    ###MATIKUUT
    print("offcentre:", offcentre)
    if offcentre <= 300 and offcentre >= -300 and Y < 200:
        motion_irl.move(int(t_speed),int(60-(abs(t_speed))),int(-t_speed/3),0)
        print("Full speed")
    else:
        motion_irl.move(int(t_speed/3),int((50-Yslow)),int(-t_speed/10),0)
        print("Slow down")


def findaball(processedData):
    global fasttimer     #BAD!!!!!!!!!!!!!
    print(" STATE: findball")
    ### robot tries to find ball
    gofasttimer = 900
    slowdowntimer = 0
    ballseen = 0
    try:
        if processedData.balls:
            fasttimer = 0
            ballseen = 1 
        if fasttimer >= 40:
            while slowdowntimer < 168:
                motion_irl.move(0,0, int(12 + (slowdowntimer/6)),0)
                slowdowntimer += 1
            slowdowntimer = 168
            while gofasttimer > 0:
                motion_irl.move(0,0,40,0)
                gofasttimer -= 1
            while slowdowntimer > 0:
                motion_irl.move(0,0, int(40 - (slowdowntimer/6)),0)
                slowdowntimer -= 1
            fasttimer = 0
        else:
            motion_irl.move(0,0,12,0) 
    except:
        motion_irl.move(0,0,12,0) 

    fasttimer += 1


def turn45(): # x ja left 0 : right 1
    temptimer = 0
    while temptimer <= 270:
        motion_irl.move(0,-15,65,0)
        temptimer += 1


def makeshot(dist, basketx, timer, ballseen):     
    if dist <= 1450:
        throwdistance = (dist) * 0.192307 + 338 ### old 
        print("Short shot")

    elif dist > 1450 and dist < 3200:
        throwdistance = (dist) * 0.15625 + 400 ### +420 last
        print("Mid shot")
    
    else:
        throwdistance = (dist) * 0.0952 + 590 ###bfr 590
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
        if ballseen == 0:
            if basketx <= middle_xbasket-1:### sec-1
                motion_irl.move(0,-6,2,0)
            elif basketx >= middle_xbasket+1:### sec+1
                motion_irl.move(0,-6,-2,0)
            else:
                pass
        else:
            if basketx <= middle_xbasket-1: ### sec-1
                motion_irl.move(0,0,2,0)
            elif basketx >= middle_xbasket+1: ### sec+1
                motion_irl.move(0,0,-2,0)
            else:
                pass



