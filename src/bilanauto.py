#!/usr/bin/env python3
import time
from subprocess import call
import cv2

import pykeyboard
import pymouse


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


fileName = '/Users/lumr/tmp/test.jpg'

if __name__ == '__main__':
    call(['screencapture', '-tjpg', '/Users/lumr/tmp/test.jpg'])
    cv2.imread(fileName)
    m = MouseController(pymouse.PyMouse())
    k = pykeyboard.PyKeyboard()
    # print('鼠标当前位置是：%s,%s' % m.position())
    m.click(600, 500, 2)

    # m.click(600, 500, 2, 2)
    # m.press(720, 450, 2)
    time.sleep(0.1)
    # m.release(720, 450, 2)
