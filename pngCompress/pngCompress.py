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


def compressPNG(inputpath, filename, postfix):
    cmd = pngquant + " " + filename + " --quality " + compress_quality + " --ext=" + postfix + " --force"
    # 如果不替换原文件，则copy压缩后的图片到其他位置
    if not SaveToOriginalDir:
        suffix = os.path.splitext(filename)
        abspath = filename.replace(inputpath, '')
        # compress_path = 'compress' + abspath
        folders = abspath.split(symb)
        folders.pop()
        # print("输入路径" + inputpath + " 压缩路径"+abspath)
        # folderpath = os.getcwd()

        outputpath = ""
        if inputpath[len(inputpath) - 1] == '/':
            inputpath = inputpath[0:-1]

        # print("inputpath =" + inputpath)
        input_folders = inputpath.split(symb)
        input_folders.pop()
        for path in input_folders:
            outputpath = outputpath + path + symb
        outputpath = outputpath + "compress"
        # print("outputpath : " + outputpath)

        folderpath = outputpath
        for folder_name in folders:
            folderpath = folderpath + symb + folder_name
            # print folderpath
            if not os.path.isdir(folderpath):
                os.makedirs(folderpath)

        new_path = outputpath + abspath
        # print("fuck ====" + outputpath + " " + abspath)
        # print("new_path ====" + new_path)
        cmd = pngquant + " " + filename + " --quality " + compress_quality + " -o " + new_path
    status = os.system(cmd)
    if status != 0:
        print("压缩失败" + filename)
    


def recursionDic(inputpath, path):
    if os.path.isfile(path):
        suffix = os.path.splitext(path)
        if suffix[1] == ".jpg":
            compressPNG(inputpath, path, ".jpg")
        elif suffix[1] == ".png":
            compressPNG(inputpath, path, ".png")
    else:
        lst = os.listdir(path)
        for ph in lst:
            recursionDic(inputpath, path + symb + ph)


if __name__ == '__main__':
    os.chdir(sys.path[0])  # 修改当前工作目录为py脚本所在目录

    # png所在路径（传入参数）
    inputpath = os.getcwd()
    if len(sys.argv) > 1:
        inputpath = sys.argv[1]
    if len(sys.argv) > 2:
        SaveToOriginalDir = sys.argv[2]


    outputpath = ""
    if inputpath[len(inputpath) - 1] == '/':
        inputpath = inputpath[0:-1]
    print("inputpath =" + inputpath)
    input_folders = inputpath.split(symb)
    input_folders.pop()
    for path in input_folders:
        outputpath = outputpath + path + symb
    outputpath = outputpath + "compress"
    if os.path.isdir(outputpath):
        shutil.rmtree(outputpath)

    # 递归遍历路径下的png
    print("输入路径:", inputpath)
    print("正在压缩 请稍后...")
    recursionDic(inputpath, inputpath)
    print('压缩图片完成')
