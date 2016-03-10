#coding:utf-8
import win_control
import cv2
import numpy as np
import time
import os
import win32gui
from PIL import ImageGrab

BLOCK_WIDTH = 101
SPLIT_WIDTH = 103
SPLIT_X = 37
SPLIT_Y = 174
SPLIT_END_X = 447
SPLIT_END_Y = 584

SPLIT_X_NEW = 68
SPLIT_Y_NEW = 384
SPLIT_END_X_NEW = 662
SPLIT_END_Y_NEW = 978

# pin
SRC_PIC = 'sc1.png'
# bijiao
DST_PIC = 'sc2.png'
title = u"夜神模拟器"

feature = np.array(
    [
        [ 154.8970995,  144.09307724, 128.39295877],
        [ 186.96664456, 180.78323924, 169.33606265],
        [ 170.54319854, 168.41955186, 171.13491254],
        [ 190.75719031, 196.76515718, 198.57256629],
        [ 53.86395379, 48.37012947, 37.64078495],
        [ 105.68277047, 113.26124885, 102.91122505],
        [ 53.52493793, 48.37736229, 36.58431679],
        [ 27.79831707, 30.68290084, 23.51140757],
        [ 13.12189232, 14.19292816, 11.41104649],
        [ 146.16350939, 151.9447392,  168.06109921],
        [ 61.36891077, 65.88807831, 79.73973744],
        [ 70.57765364, 80.04290379, 36.8155347 ],
    ]
)


def get_screenshot():
    win.screenshot(SRC_PIC)
    # win.screen_loc_down(win_control.click_pt)
    # time.sleep(0.2)
    # win.screenshot(DST_PIC)
    # win.screen_loc_up()
    time.sleep(0.05)


# [x, y]
def is_small(a, b):
    if a[1] < (b[1] - 80):
        return True
    elif (not (a[1] > b[1] + 80)) and (a[0] < b[0] - 80):
            return True
    return False


def get_id():
    src = cv2.imread(SRC_PIC)
    value = []
    for i in range(0, 15):
        x = i % 4
        y = i / 4
        img = src[(SPLIT_Y + y * SPLIT_WIDTH):(SPLIT_Y + y * SPLIT_WIDTH + BLOCK_WIDTH),
              (SPLIT_X + x * SPLIT_WIDTH):(SPLIT_X + x * SPLIT_WIDTH + BLOCK_WIDTH),
              :]
        value.append(np.average(img, axis=(0,1)))
    x = 3
    y = 4
    img = src[(SPLIT_Y + y * SPLIT_WIDTH):(SPLIT_Y + y * SPLIT_WIDTH + BLOCK_WIDTH - 2),
            (SPLIT_X + x * SPLIT_WIDTH):(SPLIT_X + x * SPLIT_WIDTH + BLOCK_WIDTH),
            :]
    value.append(np.average(img, axis=(0,1)))

    value = np.array(value)
    value = np.average(value, axis=(0))

    value = np.tile(value, (12,1))

    val = np.linalg.norm(feature - value, 2, axis=1)
    id = np.argmin(val)
    return '%d' % (id + 1), val[id]


def get_matrix():
    src = cv2.imread(SRC_PIC)
    dst = cv2.imread(DST_PIC)
    #dst_tem = dst[SPLIT_Y:SPLIT_END_Y, SPLIT_X:SPLIT_END_X,:]
    dst_tem = dst[SPLIT_Y_NEW:SPLIT_END_Y_NEW, SPLIT_X_NEW:SPLIT_END_X_NEW, :]
    dst_tem = cv2.resize(dst_tem, (410, 410))
    block = []
    position = []
    id = []
    cv2.rectangle(dst_tem, (3 * SPLIT_WIDTH, 3 * SPLIT_WIDTH), (3 * SPLIT_WIDTH + BLOCK_WIDTH, 3 * SPLIT_WIDTH + BLOCK_WIDTH), (255, 255, 255), cv2.cv.CV_FILLED)
    for i in range(0, 15):
        x = i % 4
        y = i / 4
        img = src[(SPLIT_Y + y * SPLIT_WIDTH):(SPLIT_Y + y * SPLIT_WIDTH + BLOCK_WIDTH),
              (SPLIT_X + x * SPLIT_WIDTH):(SPLIT_X + x * SPLIT_WIDTH + BLOCK_WIDTH),
              :]
        block.append(img)
        result = cv2.matchTemplate(dst_tem, block[i], cv2.TM_SQDIFF)
        value = cv2.minMaxLoc(result)
        position.append(value[2])
        id.append(i)

    for i in range(0, 15):
        for j in range(i + 1, 15):
            if is_small(position[j], position[i]):
                temp = position[i]
                position[i] = position[j]
                position[j] = temp
                temp_id = id[i]
                id[i] = id[j]
                id[j] = temp_id
    out = np.zeros((4, 4),np.int32)
    out[3, 3] = 16
    for i in range(0, 15):
        x = id[i] % 4
        y = id[i] / 4
        out[y, x] = i + 1
    out.shape = 16
    str = ''
    for i in range(0, 15):
        str += '%d' % out[i] + ','
    str += '0'
    return str


if __name__ == '__main__':
    hwnd = win32gui.FindWindow(None, title)
    if hwnd>0:
        rect = win32gui.GetWindowRect(hwnd)
        win = win_control.win_control(hwnd, rect)
        print(rect)
        im = ImageGrab.grab(bbox=rect)
        color = im.getpixel(win_control.start_pt)
        while color[0]!=60 or color[1]!=58 or color[2]!=59:
            im = ImageGrab.grab(bbox=rect)
            color = im.getpixel(win_control.start_pt)
            time.sleep(0.03)
        globals()['tt'] = time.clock()
        print('-----------------Start-----------------')
        time.sleep(2)

        rect = win32gui.GetWindowRect(hwnd)
        print(rect)

        id = '10'
        SRC_PIC = 'sc' + id + 'a.png'

        get_screenshot()

        id, err = get_id()
        print id, err
        if err > 5:
            print('no match')
            id = raw_input()
        DST_PIC = 'data\\' + id + '.jpg'
        str = get_matrix()

        cmd = 'java java_bin.PuzzleSolver ' + '15 i p 3 ' + str
        output = os.popen(cmd)
        str = output.read()

        # y x
        now_pid = [3, 3]
        last_f = str[0]
        now_f = 'E'
        if len(str) == 0 or (str[0] != 'L' and str[0] != 'R' and str[0] != 'U' and str[0] != 'D'):
            print('Pic can\'t be recognized/Puzzle can\'t be solved')
        else:
            for i in range(0, len(str)):
                now_f = str[i]
                if last_f != now_f:
                    last_f = now_f
                    win.click(now_pid)

                if str[i] == 'L':
                    now_pid[1] -= 1
                elif str[i] == 'R':
                    now_pid[1] += 1
                elif str[i] == 'U':
                    now_pid[0] -= 1
                elif str[i] == 'D':
                    now_pid[0] += 1
                # if now_f == last_f:
                #print(now_pid)
                #adb.click(now_pid)
            win.click(now_pid)
            while (time.clock()-globals()['tt'])<14.5:
                pass
            win.screen_loc_down(win_control.end_pt)
            time.sleep(0.1)
            win.screen_loc_up()
    else:
        print('Could not find the Window named ' + title)
