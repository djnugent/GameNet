import win32api as wapi
import ctypes
import numpy as np
from PIL import ImageGrab
import cv2
import time
import struct
from threading import Thread
import wx
from wx.adv import Joystick as JS

###########################SCREEN CAPTURE########################
def grab_window(box =(0,40,800,640) ):
        return np.array(ImageGrab.grab(bbox=box))


####################################KEY INPUT################################
keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'$/\\":
    keyList.append(char)

def pressed_keys():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys


##########################KEY OUTPUT##############################
SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]



key_map = {"w":0x11, "a":0x1E, "s":0x1f, "d":0x20}

def press_key(key):
    hexKeyCode = key_map[key.lower()]
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def release_key(key):
    hexKeyCode = key_map[key.lower()]
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


#######################################CAPTURE JOYSTICK########################
class JoyStick(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.x, self.y, self.z = None,None,None

    def run(self):
        self.app = wx.App()
        frame = wx.Frame(None)
        #set up joystick
        joy = JS()
        joy.SetCapture(frame)
        frame.Bind(wx.EVT_JOY_MOVE, self.xyEvent)
        frame.Bind(wx.EVT_JOY_ZMOVE, self.zEvent)
        self.app.MainLoop()

    def xyEvent(self,event):
        _x,_y = event.GetPosition()
        self.x = (_x / 32768) - 1
        self.y = (_y / 32768) - 1

    def zEvent(self,event):
        _z = event.GetZPosition()
        self.z = (_z / 32768) - 1


######################################VIRTUAL JOYSTICK#########################
CONST_DLL_VJOY = "C:\\Program Files\\vJoy\\x64\\vJoyInterface.dll"

class vJoy(object):
    def __init__(self, reference = 1):
        self.handle = None
        self.dll = ctypes.CDLL( CONST_DLL_VJOY )
        self.reference = reference
        self.acquired = False

    def open(self):
        if self.dll.AcquireVJD( self.reference ):
            self.acquired = True
            return True
        return False
    def close(self):
        if self.dll.RelinquishVJD( self.reference ):
            self.acquired = False
            return True
        return False
    def generateJoystickPosition(self,
        wThrottle = 0, wRudder = 0, wAileron = 0,
        wAxisX = 0, wAxisY = 0, wAxisZ = 0,
        wAxisXRot = 0, wAxisYRot = 0, wAxisZRot = 0,
        wSlider = 0, wDial = 0, wWheel = 0,
        wAxisVX = 0, wAxisVY = 0, wAxisVZ = 0,
        wAxisVBRX = 0, wAxisVBRY = 0, wAxisVBRZ = 0,
        lButtons = 0, bHats = 0, bHatsEx1 = 0, bHatsEx2 = 0, bHatsEx3 = 0):
        """
        typedef struct _JOYSTICK_POSITION
        {
            BYTE    bDevice; // Index of device. 1-based
            LONG    wThrottle;
            LONG    wRudder;
            LONG    wAileron;
            LONG    wAxisX;
            LONG    wAxisY;
            LONG    wAxisZ;
            LONG    wAxisXRot;
            LONG    wAxisYRot;
            LONG    wAxisZRot;
            LONG    wSlider;
            LONG    wDial;
            LONG    wWheel;
            LONG    wAxisVX;
            LONG    wAxisVY;
            LONG    wAxisVZ;
            LONG    wAxisVBRX;
            LONG    wAxisVBRY;
            LONG    wAxisVBRZ;
            LONG    lButtons;   // 32 buttons: 0x00000001 means button1 is pressed, 0x80000000 -> button32 is pressed
            DWORD   bHats;      // Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
                        DWORD   bHatsEx1;   // 16-bit of continuous HAT switch
                        DWORD   bHatsEx2;   // 16-bit of continuous HAT switch
                        DWORD   bHatsEx3;   // 16-bit of continuous HAT switch
        } JOYSTICK_POSITION, *PJOYSTICK_POSITION;
        """
        joyPosFormat = "BlllllllllllllllllllIIII"
        pos = struct.pack( joyPosFormat, self.reference, wThrottle, wRudder,
                                   wAileron, wAxisX, wAxisY, wAxisZ, wAxisXRot, wAxisYRot,
                                   wAxisZRot, wSlider, wDial, wWheel, wAxisVX, wAxisVY, wAxisVZ,
                                   wAxisVBRX, wAxisVBRY, wAxisVBRZ, lButtons, bHats, bHatsEx1, bHatsEx2, bHatsEx3 )
        return pos


    def setXYZ(self,x,y,z):
        x_axis = int(x * 16000 + 16000)
        y_axis = int(y * 16000 + 16000)
        z_axis = int(z * 16000 + 16000)
        joystickPosition = self.generateJoystickPosition(wAxisX=x_axis,wAxisY = y_axis,wAxisZ=z_axis)
        self.update(joystickPosition)

    def update(self, joystickPosition):
        if self.dll.UpdateVJD( self.reference, joystickPosition ):
            return True
        return False
    #Not working, send buttons one by one
    def sendButtons( self, bState ):
        joyPosition = self.generateJoystickPosition( lButtons = bState )
        return self.update( joyPosition )
    def setButton( self, index, state ):
        if self.dll.SetBtn( state, self.reference, index ):
            return True
        return False
