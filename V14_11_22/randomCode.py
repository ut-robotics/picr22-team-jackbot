import time


command1 = struct.pack('<hhhHBH', int(motor1), 0, -int(motor2), thrower1, disable_failsafe, 0xAAAA)
        