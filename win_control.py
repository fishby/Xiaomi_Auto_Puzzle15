import time
import numpy as np
from PIL import ImageGrab
import win32api, win32con
from ctypes import *

# 53 54
points = np.array([
    [
        [87, 224],
        [190, 224],
        [293, 224],
        [396, 224]
    ], [
        [87, 327],
        [190, 327],
        [293, 327],
        [396, 327]
    ], [
        [87, 430],
        [190, 430],
        [293, 430],
        [396, 430]
    ], [
        [87, 533],
        [190, 533],
        [293, 533],
        [396, 533]
    ]
], np.int32)

click_pt = np.array([157, 795], np.int32)
end_pt = np.array([403, 631], np.int32)
app_loc = np.array([0, 0], np.int32)
start_pt = (421, 132)

TIME_DELAY = 0.05
TIME_DELAY2 = 0.05

class POINT(Structure):
    _fields_ = [("x", c_ulong),("y", c_ulong)]

class win_control:
    hwnd = 0
    rect = []

    def __init__(self, hwnd, rect):
        self.hwnd = hwnd
        self.rect = rect
        app_loc[0] = rect[0]
        app_loc[1] = rect[1]

    def click(self, pid):
        pt = points[pid[0], pid[1]]
        self.screen_loc_down(pt)
        time.sleep(TIME_DELAY)
        self.screen_loc_up()
        time.sleep(TIME_DELAY)

    def screenshot(self, filename):
        # adb shell /system/bin/screencap -p /sdcard/screenshot1.png
        im = ImageGrab.grab(bbox=self.rect)
        im.save(filename)


    def mouse_move(self, pt):
        windll.user32.SetCursorPos(pt[0], pt[1])

    def screen_loc_down(self, pt):
        # 'adb shell sendevent /dev/input/event2 3 57 ' + ('%d' % pt[0]),
        self.mouse_move(pt + app_loc)
        time.sleep(TIME_DELAY)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    def screen_loc_up(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

