from system import vJoy
import time

vj = vJoy()

try:
    print("opening joystick")
    vj.open()

    joystickPosition = vj.generateJoystickPosition(wAxisX=16000,wAxisY = 16000)
    vj.update(joystickPosition)

    print("Select axis: f,r,l:")
    axis = input()
    if axis =="f":
        x,y = 16000,0
    elif axis =='b':
        x,y = 16000,32000
    elif axis =="r":
        x,y = 32000,16000
    elif axis =="l":
        x,y = 0,16000
    else:
        print("invalid command")
    while True:
        joystickPosition = vj.generateJoystickPosition(wAxisX=x,wAxisY = y)
        vj.update(joystickPosition)

finally:
    vj.close()
