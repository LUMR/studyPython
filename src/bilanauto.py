#!/usr/bin/env python3
import time
from subprocess import call
import cv2

import numpy as np
from pymouse import PyMouse

# 图片路径
PATH = '/Users/lumr/tmp/bl/'
# 截图尺寸与鼠标移动尺寸比例
R = 2
# 图片相似度
DIFF = 0.985

TMPScreenPath = PATH + 'tmp.jpg'


class MouseController:
    """
    鼠标控制器
    """

    def __init__(self):
        self.m = PyMouse()

    def position(self):
        print('鼠标当前位置是：%s,%s' % self.m.position())

    def click(self, x, y, button=1, times=1):
        if button == 2:
            self.rclick(x, y)
        else:
            self.lclick(x, y, times)
        self.position()

    def move(self, x, y):
        self.m.move(x, y)
        print('mouse move to (%d,%d)' % (x, y))

    def lclick(self, x, y, times=1):
        self.m.click(x, y, 1, times)
        print('mouse lclick on (%d,%d)' % (x, y))

    def rclick(self, x, y):
        self.m.press(x, y, 2)
        time.sleep(0.1)
        self.m.release(x, y, 2)
        print('mouse rclick on (%d,%d)' % (x, y))


NODES = sorted(['0',
                '1-0', '1-1', '1-1',
                # '2-0', '2-1',
                '3-0', '3-1', '3-2', '3-3', '3-4'
                ])


class ProcessManager:
    """游戏流程控制器
    @:param status 0 未开始 1开始 2出错
    @:param node 游戏处于的环节：0未开始 1关口选择 2确认进入关口 3小怪清理 4Boss清理 5结束
        3和4细分：1选择怪物 2点击怪物 3开始战斗 4战斗结束 5确认奖励 6结束
    """

    def __init__(self):
        self.status = 0
        self.node = 0
        self.kill_boss = False
        self.exchange_time = 0  # 切换船次数
        self.ship_time = 5  # 第1只船剩余油数
        self.other_ship_time = 5
        self.m = MouseController()

    def start(self, start_node='1-0'):
        """
        开始脚本
        :return:
        """
        print('脚本开始。')
        self.status = 1
        self.node = NODES.index(start_node)
        while True:
            time.sleep(3)
            if self.node >= len(NODES):
                self.node = 1
                break
            if self.status == 1:
                self.next()
            elif self.status == 2:
                break
        print('脚本结束。')

    def next(self):
        """
        进入下一个环节
        :return:
        """
        node_name = NODES[self.node]
        print('进入%s环节' % node_name)
        if node_name == '3-0':  # 寻敌环节
            time.sleep(3)
            if self.ship_time <= 0:
                self.click_image('exchange')
                self.ship_time,self.other_ship_time = self.other_ship_time,self.ship_time
                time.sleep(2)
                self.exchange_time += 1
            if exist_image('boss')[0]:
                if self.exchange_time % 2 != 1:
                    self.click_image('exchange')
                    self.ship_time, self.other_ship_time = self.other_ship_time, self.ship_time
                    return
                self.click_image('boss')
                self.kill_boss = True
            elif exist_image('level-mid')[0]:
                self.click_image('level-mid', 50, 50)
            elif exist_image('level-hard')[0]:
                self.click_image('level-hard', 50, 50)
            elif exist_image('ship-easy')[0]:
                self.click_image('ship-easy')
            elif exist_image('ship-mid')[0]:
                self.click_image('ship-mid')
            elif exist_image('item'):
                self.click_image('item', 0, 50)
                time.sleep(3)
                if exist_image('3-1')[0]:
                    self.click_image('3-3')
                return
            else:
                return
            self.node += 1
        elif node_name == '3-1':
            time.sleep(5)
            if exist_image('skip')[0]:
                self.click_image('skip')
                self.node = NODES.index('3-0')
            else:
                self.click_image('3-1')
                self.node += 1
        elif node_name == '3-2':
            time.sleep(60)
            while not exist_image('3-2')[0]:
                time.sleep(10)
            self.click_image('3-2')
            self.node += 1
        elif node_name == '3-4':  # 战斗结束
            self.click_image('3-4')
            if self.kill_boss:
                self.node += 1
                self.kill_boss = False
            else:
                self.node = NODES.index('3-0')
            self.ship_time -= 1
        else:
            if self.click_image(node_name):
                self.node += 1

    def click_image(self, tar_image, w=0, h=0, mindiff=DIFF):
        """
        点击图片进入下一步
        :param tar_image:
        :return:
        """
        for i in range(10):
            print('点击%s 按钮,第%d次尝试' % (tar_image, i))
            screen()
            time.sleep(0.2)
            diff, x, y = findImgLocation(tar_image + '.jpg')
            if diff > mindiff:
                self.m.lclick(x + w, y + h)
                return True
        self.status = 2
        return False

    def __getattr__(self, item):
        return self[item]


def findImgLocation(templatepath, srcPath=TMPScreenPath):
    src = cv2.imread(srcPath, cv2.IMREAD_GRAYSCALE)
    temp = cv2.imread(PATH + templatepath, cv2.IMREAD_GRAYSCALE)
    # src_gray = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
    res = cv2.matchTemplate(src, temp, cv2.TM_CCORR_NORMED)
    h, w = temp.shape[0:2]
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # cv2.rectangle(src, max_loc, (max_loc[0] + w, max_loc[1] + h), (7, 249, 151), 2)
    # cv2.imshow('View', src)
    # cv2.waitKey(12000)
    # cv2.destroyAllWindows()
    print('图片匹配完成，最高匹配率{0},位置为:{1}'.format(max_val, max_loc))
    return max_val, (int(max_loc[0]) + (w >> 1)) >> 1, (int(max_loc[1]) + (h >> 1)) >> 1


def exist_image(tar_image, minDiff=DIFF):
    screen()
    time.sleep(0.5)
    max_val, x, y = findImgLocation(tar_image + '.jpg')
    if max_val > minDiff:
        return True, x, y
    else:
        return False, 0, 0


last_time = 0


def screen():
    global last_time
    now = time.time()
    if now - last_time > 1.5:
        call(['screencapture', '-tjpg', TMPScreenPath])
    last_time = now


if __name__ == '__main__':
    pm = ProcessManager()
    print('脚本即将开始，请3秒内将画面移动到模拟器。')
    time.sleep(3)
    pm.start('3-0')
