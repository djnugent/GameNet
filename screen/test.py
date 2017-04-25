from system import pressed_keys, grab_window, press_key, release_key, vJoy, JoyStick
import cv2
import win32gui


#Capture Joystick
js_in = JoyStick()
js_in.start()

#virtual JoyStick
js_out = vJoy()
js_out.open()
js_out.setXYZ(0,-1,0)


#move window to upper right
window = win32gui.FindWindow(None,"CrazyCars")
rect = win32gui.GetWindowRect(window)
w = rect[2] - rect[0]
h = rect[3] - rect[1]
win32gui.MoveWindow(window,0,0,w,h,False)
win32gui.SetForegroundWindow(window)

try:
    while True:

        x,y,z = js_in.x, js_in.y, js_in.z
        if(x is not None and z is not None):
            steering = x
            throttle = (z+1)/-2
            js_out.setXYZ(steering,throttle,0)
            print(steering,throttle)

        window = grab_window((10,35,514,410))
        cv2.imshow("window",window)
        cv2.waitKey(1)
finally:
    js_out.close()
