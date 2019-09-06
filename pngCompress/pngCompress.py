#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil

pngquant = './pngquant-mac/pngquant'
symb = '/'
if sys.platform == 'win32':
    pngquant = 'pngquant-win\\pngquant.exe'

# 是否替换原文件
SaveToOriginalDir = False
# 压缩质量范围
compress_quality = '75-80'
# 压缩工具


def compressPNG(inputpath, filename):
    cmd = pngquant + " --ext " + ".png --force " + " " + filename + " --quality " + compress_quality
    # 如果不替换原文件，则copy压缩后的图片到其他位置
    if not SaveToOriginalDir:
        suffix = os.path.splitext(filename)
        abspath = filename.replace(inputpath, '')
        compress_path = 'compress' + abspath
        folders = compress_path.split(symb)
        folders.pop()

        folderpath = os.getcwd()
        for folder_name in folders:
            folderpath = folderpath + symb + folder_name
            # print folderpath
            if not os.path.isdir(folderpath):
                os.makedirs(folderpath)

        new_path = os.getcwd() + symb + 'compress' + abspath
        cmd = pngquant + " " + filename + " --quality " + compress_quality + " --output " + new_path

    os.system(cmd)
    print(cmd)


def recursionDic(inputpath, path):
    if os.path.isfile(path):
        suffix = os.path.splitext(path)
        if suffix[1] == ".png":
            print path
            compressPNG(inputpath, path)
    else:
        lst = os.listdir(path)
        for ph in lst:
            recursionDic(inputpath, path + symb + ph)


if __name__ == '__main__':
    os.chdir(sys.path[0])  # 修改当前工作目录为py脚本所在目录

    # png所在路径（传入参数）
    inputpath = os.getcwd()
    print inputpath
    if len(sys.argv) > 1:
        inputpath = sys.argv[1]

    # 递归遍历路径下的png
    print inputpath
    recursionDic(inputpath, inputpath)
    print '压缩图片完成'
