#!/usr/bin/env python3
import time
from subprocess import call
import cv2

import pykeyboard
from pymouse import PyMouse

# 图片路径
PATH = '/Users/lumr/tmp/bl/'
# 截图尺寸与鼠标移动尺寸比例
R = 2

fileName = PATH + 'enter.jpg'


class MouseController:
    def __init__(self, mouse):
        self.m = mouse

    def position(self):
        print('鼠标当前位置是：%s,%s' % self.m.position())

    def click(self, x, y, button=1, times=1):
        if button == 2:
            self.rclick(x, y)
        else:
            self.lclick(x, y, times)
        self.position()

    def lclick(self, x, y, times=1):
        self.m.click(x, y, 1, times)

    def rclick(self, x, y):
        self.m.press(x, y, 2)
        time.sleep(0.1)
        self.m.release(x, y, 2)


def findImgLocation(srcPath, templatePath):
    src = cv2.imread(PATH + srcPath, 0)
    temp = cv2.imread(PATH + templatePath, 0)
    res = cv2.matchTemplate(src, temp, cv2.TM_CCORR_NORMED)
    h, w = temp.shape[0:2]
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return (max_loc[0] + w / 2) / R, (max_loc[1] + h / 2) / R


if __name__ == '__main__':
    # call(['screencapture', '-tjpg', fileName])
    gScreen = cv2.imread(PATH + 'enter.jpg', 0)
    screenHeight, screenWidth = gScreen.shape[0:2]
    pbutton = cv2.imread(PATH + 'enterbutton.jpg', 0)
    res = cv2.matchTemplate(gScreen, pbutton, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print('max value is {0} pos is {1}'.format(max_val, max_loc))
    x, y = findImgLocation('enter.jpg', 'enterbutton.jpg')
    print('x = {0} , y = {1}'.format(x, y))
    m = MouseController(PyMouse())
    m.rclick(x, y)
