import turtle
import math
import numpy as np
import time
import tkinter as tk
import serial
import threading
import struct
from threading import Thread

global logic
logic = "test"

# disable_failsafe = 0
# command1 = struct.pack('<hhhHBH', 20, 0, -20, 0, disable_failsafe, 0xAAAA)
# OmniMotionRobot.send(motion_irl, command1)

    












class IRobotMotion:
    def open(self):
        pass
    def close(self):
        pass
    def move(self, x_speed, y_speed, rot_speed):
        pass

class OmniMotionRobot(IRobotMotion):
    def __init__(self):
         # Wheel angles
        self.motor_config = [120, 0, 240]
        self.serialObj = serial.Serial()
        
    def open(self):
        serial_port = "/dev/ttyACM0"
        self.serialObj.setPort(serial_port)
        self.serialObj.open()
        
    def close(self):
        self.serialObj.close()
        
    def send(self, command):
        self.serialObj.write(command)
    
    def move(self, robotSpeedX, robotSpeedY, rot_speed, shooter):
        speeds = [0, 0, 0]
        wheelDistanceFromCenter = 13  ##find out
        robotSpeed = math.sqrt(robotSpeedX * robotSpeedX + robotSpeedY * robotSpeedY)
        robotDirectionAngle = math.atan2(robotSpeedY, robotSpeedX)

        # This is where you need to calculate the speeds for robot motors
        for i in range(len(self.motor_config)):
            wheelLinearVelocity = robotSpeed * math.cos(robotDirectionAngle - math.radians(self.motor_config[i])) + rot_speed
            
            speeds[i] = int(wheelLinearVelocity)
            
        disable_failsafe = 0
        command1 = struct.pack('<hhhHBH', speeds[2], speeds[1], speeds[0], shooter, disable_failsafe, 0xAAAA)
        self.send(command1)
        
#     def thrower(thrower):
#         disable_failsafe = 0
#         command1 = struct.pack('<hhhHBH', 0, 0, 0, int(thrower), disable_failsafe, 0xAAAA)
#         self.send(command1)
        

#class TurtleRobot(IRobotMotion):
 #   def __init__(self, name="Default turtle robot"):
#
 #       window = tk.Tk()
  #      window.title(name)
#
 #       canvas = tk.Canvas(master=window, width=500, height=500)
  #      canvas.pack()

   #     self.screen = turtle.TurtleScreen(canvas)
    #    self.turtle_obj = turtle.RawTurtle(self.screen)
     #   self.turtle_obj.speed('fastest')

      #  self.steps = 20

   # def open(self):
    #    print("Wroom! Starting up turtle!")
        

   # def close(self):
    #    print("Going to dissapear...")
        
        
#         
# motion_irl = OmniMotionRobot()
# motion_irl.open()
#


def movexd(motor1, motor2 ,motor3, memethrower, time2):
    timestop = 0
    
    while timestop <= time2:
        timestart = time.time()
        disable_failsafe = 0
        command1 = struct.pack('<hhhHBH', int(motor1), int(motor3), int(motor2), int(memethrower), disable_failsafe, 0xAAAA)
        OmniMotionRobot.send(motion_irl, command1)
        mid = time.time()
        timestop += (mid-timestart)
#         
# def turn(left):
#     if left == 0:
#         disable_failsafe = 0
#         command1 = struct.pack('<hhhHBH', 7, 7, 7, 0, disable_failsafe, 0xAAAA)
#         OmniMotionRobot.send(motion_irl, command1)
#     else:
#         disable_failsafe = 0
#         command1 = struct.pack('<hhhHBH', -7, -7, -7, 0, disable_failsafe, 0xAAAA)
#         OmniMotionRobot.send(motion_irl, command1)
#         
# # def turndrive(right):
# #     if right == 0:
# #         disable_failsafe = 0
# #         command1 = struct.pack('<hhhHBH', -20, 0, 10, 0, disable_failsafe, 0xAAAA)
# #         OmniMotionRobot.send(motion_irl, command1)
# #     else:
# #         disable_failsafe = 0
# #         command1 = struct.pack('<hhhHBH', -10, 0, 30, 0, disable_failsafe, 0xAAAA)
# #         OmniMotionRobot.send(motion_irl, command1)
# #         
# # def turndrivestraight(right):
# #     if right == 0:
# #         disable_failsafe = 0
# #         command1 = struct.pack('<hhhHBH', -20, 0, 20, 0, disable_failsafe, 0xAAAA)
# #         OmniMotionRobot.send(motion_irl, command1)
# #     else:
# #         disable_failsafe = 0
# #         command1 = struct.pack('<hhhHBH', -20, 0, 30, 0, disable_failsafe, 0xAAAA)
# #         OmniMotionRobot.send(motion_irl, command1)
#     
# def turndrive(right):
#     if right == 0:
#         disable_failsafe = 0
#         command1 = struct.pack('<hhhHBH', -30, 0, 20, 0, disable_failsafe, 0xAAAA)
#         OmniMotionRobot.send(motion_irl, command1)
#     else:
#         disable_failsafe = 0
#         command1 = struct.pack('<hhhHBH', -20, 0, 30, 0, disable_failsafe, 0xAAAA)
#         OmniMotionRobot.send(motion_irl, command1)
#         
# def turndrivestraight(right):
#     if right == 0:
#         disable_failsafe = 0
#         command1 = struct.pack('<hhhHBH', -25, 0, 20, 0, disable_failsafe, 0xAAAA)
#         OmniMotionRobot.send(motion_irl, command1)
#     else:
#         disable_failsafe = 0
#         command1 = struct.pack('<hhhHBH', -20, 0, 25, 0, disable_failsafe, 0xAAAA)
#         OmniMotionRobot.send(motion_irl, command1)
#         
# def otse():
#     disable_failsafe = 0
#     command1 = struct.pack('<hhhHBH', -18, 0, 27, 0, disable_failsafe, 0xAAAA)
#     OmniMotionRobot.send(motion_irl, command1)
#     disable_failsafe = 0
#     command1 = struct.pack('<hhhHBH', -24, 0, 31, 0, disable_failsafe, 0xAAAA)
#     OmniMotionRobot.send(motion_irl, command1)
#     disable_failsafe = 0
#     command1 = struct.pack('<hhhHBH', -28, 0, 35, 0, disable_failsafe, 0xAAAA)
#     OmniMotionRobot.send(motion_irl, command1)
#     disable_failsafe = 0
#     command1 = struct.pack('<hhhHBH', -33, 0, 38, 0, disable_failsafe, 0xAAAA)
#     OmniMotionRobot.send(motion_irl, command1)
#     
# def StraightSLow():
#     disable_failsafe = 0
#     command1 = struct.pack('<hhhHBH', -10, 0, 10, 0, disable_failsafe, 0xAAAA)
#     OmniMotionRobot.send(motion_irl, command1)
#     
# def otsePIDDABLE():
#     disable_failsafe = 0
#     command1 = struct.pack('<hhhHBH', -18, 0, 27, 0, disable_failsafe, 0xAAAA)
#     OmniMotionRobot.send(motion_irl, command1)
#     
# def motor1(speed):
#     disable_failsafe = 0
#     command1 = struct.pack('<hhhHBH', 0, 0, 0, 0, disable_failsafe, 0xAAAA)
#     OmniMotionRobot.send(motion_irl, command1)
#     
# def motor2(speed):
#     disable_failsafe = 0
#     command1 = struct.pack('<hhhHBH', 0, 0, 0, 0, disable_failsafe, 0xAAAA)
#     OmniMotionRobot.send(motion_irl, command1)
#     
# def motor3(speed):
#     disable_failsafe = 0
#     command1 = struct.pack('<hhhHBH', 0, 0, 0, 0, disable_failsafe, 0xAAAA)
#     OmniMotionRobot.send(motion_irl, command1)
# 
# 
# def TurnAroundBall():
#     #maincam.all_objects[0][2]
#     #maincam.EnemyBasket
#     pass
# 
#         
# 
# def movelogic():
#     if logic == "test":
#         print("Test movelogic, start")
#         time.sleep(1)
#         move(-20,20,20,2)
#         time.sleep(1)
#         move(20,-20,-20,2)
#         time.sleep(1)
#         move(10,10,0,2)
#         print("Movelogic complete xddddd")
#     else:
#         ##main driving logic
#         print("Main drivin logic start")
#         ##search for ball
# #         while True:
# #             turn(1)
# #             time.sleep(0.05)
#         
#         
#         
#     #Very dumb logic to draw motion using turtle
# #     def move(self, x_speed, y_speed, rot_speed):
# #         self.screen.tracer(0, 0)
# #         angle_deg = 0
# # 
# #         angle_deg = np.degrees(math.atan2(x_speed, y_speed))
# # 
# #         distance = math.sqrt(math.pow(x_speed, 2) + math.pow(y_speed, 2))
# # 
# #         distance_step = distance / float(self.steps)
# #         angel_step = np.degrees(rot_speed / float(self.steps))
# # 
# #         self.turtle_obj.penup()
# #         self.turtle_obj.reset()
# #         self.turtle_obj.right(angle_deg - 90)
# #         self.turtle_obj.pendown()
# # 
# #         for i in range(0, self.steps):
# #             self.turtle_obj.right(angel_step)
# #             self.turtle_obj.forward(distance_step)
# # 
# #         self.turtle_obj.penup()
# #         self.screen.update()
# # 
# # 
# class TurtleOmniRobot():
#     def __init__(self, name="Default turtle omni robot"):
#         TurtleRobot.__init__(self, name)
# 
#         # Wheel angles
#         self.motor_config = [0, 120, 240]
# 
#     def move(self, robotSpeedX, robotSpeedY, rot_speed):
#         speeds = [0, 0, 0]
#         wheelDistanceFromCenter = 13  ##find out
#         robotSpeed = math.sqrt(robotSpeedX * robotSpeedX + robotSpeedY * robotSpeedY)
#         robotDirectionAngle = math.atan2(robotSpeedY, robotSpeedX)
# 
#         # This is where you need to calculate the speeds for robot motors
#         for i in len(self.motor_config):
#             wheelLinearVelocity = robotSpeed * math.cos(robotDirectionAngle - self.motor_config[i]) + rot_speed
#             
#             speeds[i] = wheelLinearVelocity
#         
#         simulated_speeds = self.speeds_to_direction(speeds)
# 
#         TurtleRobot.move(self, simulated_speeds[0], simulated_speeds[1], simulated_speeds[2])
# 
# #     def speeds_to_direction(self, speeds):
# #         offset_x = 0
# #         offset_y = 0
# #         degree = int((speeds[0] + speeds[1] + speeds[2]) / 3)
# #     
# #         for i in range(0, 3):
# #             end_vector = self.motor_side_forward_scale(self.motor_config[i] + 90, speeds[i], offset_x, offset_y)
# #             offset_x = end_vector[0]
# #             offset_y = end_vector[1]
# #     
# #         offsets = [offset_x * -1, offset_y]
# #         speeds = [int(a / 1.5) for a in offsets]
# #         speeds.append(degree)
# #     
# #         return speeds
# #  
# #     def motor_side_forward_scale(self, angel, length, offset_x=0, offset_y=0):
# #         ang_rad = math.radians(angel)
# #         return [length * math.cos(ang_rad) + offset_x, length * math.sin(ang_rad) + offset_y]
# # 