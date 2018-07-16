#!/usr/bin/env python3

import sys,os


def change_file(filepath):
    with open(filepath, 'rb') as file:
        print('打开文件%s ' % file.name)
        fileName = file.name.split('.')[0] + '.mp3'
        with open(fileName, 'wb') as nfile:
            print('新文件 %s' % nfile.name)
            b = file.read()
            a = bytes([by ^ 0xA3 for by in b])
            cou = nfile.write(a)
            print('转换完成:%d' % cou)


if __name__ == '__main__':
    files = sys.argv[1:]
    for filepath in files:
        change_file(filepath)


