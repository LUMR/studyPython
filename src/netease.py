#!/usr/bin/env python3

import sys, os


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


def change_file1(source, targe):
    with open(source, 'rb') as file:
        print('打开文件%s ' % file.name)
        with open(targe, 'wb') as nfile:
            print('新文件 %s' % nfile.name)
            b = file.read()
            a = bytes([by ^ 0xA3 for by in b])
            nfile.write(a)
            print('转换完成')


if __name__ == '__main__':
    args = sys.argv[1:]
    if args.__len__() < 2:
        change_file(args[0])
    else:
        source = args[0]
        targe = args[1]
        files = os.listdir(source)
        for file in files:
            fileName = os.path.splitext(file)
            if fileName[1] == '.uc!':
                change_file1(os.path.join(source, file), os.path.join(targe, fileName[0] + '.mp3'))
