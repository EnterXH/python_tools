# -*- coding: utf-8 -*-

import os
import sys
import shutil

def CopyFileToOutputFolder(inputpath, outputpath, relativepath):
    # print("输入：" + inputpath + '/' + relativepath)
    # print("输出：" + outputpath + '/' + relativepath)
    # print(os.path.exists(inputpath + '/' + relativepath))
    if os.path.exists(inputpath + '/' + relativepath):
        folders = relativepath.split('/')
        # 取出最后一项内容，
        folders.pop()
        # 开始创建不存在的文件夹
        folderpath = outputpath
        for folder_name in folders:
            folderpath = folderpath + '/' + folder_name
            if not os.path.isdir(folderpath):
                os.makedirs(folderpath)
        # 把对应的文件复制到新的文件夹中
        input_file = inputpath + '/' + relativepath
        output_file = outputpath + '/' + relativepath
        print('复制文件:' + input_file)
        shutil.copyfile(input_file, output_file)


if __name__ == "__main__":
    os.chdir(sys.path[0]) # 修改当前工作目录为py脚本所在目录

    # 输入路径
    workpath = os.getcwd()
    inputpath = workpath
    outputpath = workpath
    if len(sys.argv) > 1 :
        inputpath = sys.argv[1]

    if len(sys.argv) > 2 :
        outputpath = sys.argv[2]
    print("workpath:" + workpath)
    print("inputpath:" + inputpath)
    print("outputpath:" + outputpath)

    # 生成输出文件夹
    outputfolder = outputpath + "/copy"
    if not os.path.isdir(outputfolder) :
        os.makedirs(outputfolder)

    # 读取file文件
    document = open(workpath + "/FilePaths.txt", "r");
    lists = document.readlines()
    for line in lists:
        string = line.replace('\n', '')
        path = string.replace(' ', '')
        CopyFileToOutputFolder(inputpath, outputfolder, path)

    print('文件复制完成')
