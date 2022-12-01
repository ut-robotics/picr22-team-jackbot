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