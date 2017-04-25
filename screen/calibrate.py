
from system import vJoy
import time

vj = vJoy()



try:
    print("opening joystick")
    vj.open()

    joystickPosition = vj.generateJoystickPosition(wAxisX=16000,wAxisY = 16000)
    vj.update(joystickPosition)

    print("Select axis: x,y:")
    axis = input()

    for i in range(16000,32000,2):
        if axis =="x":
            x,y = i,16000
        elif axis =="y":
            x,y = 16000,i

        else:
            print("invalid axis")
            break
        print(axis,i)
        joystickPosition = vj.generateJoystickPosition(wAxisX=x,wAxisY = y)
        vj.update(joystickPosition)

finally:
    vj.close()
