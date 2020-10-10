# -*- coding: utf-8 -*-
import os
import sys
import shutil
def CopyFileToOutputFolder(inputpath, outputpath, relativepath):
    if os.path.exists(inputpath + '/' + relativepath):
        folders = relativepath.split('/')
        folders.pop()
        folderpath = outputpath
        for folder_name in folders:
            folderpath = folderpath + '/' + folder_name
            if not os.path.isdir(folderpath):
                os.makedirs(folderpath)
        input_file = inputpath + '/' + relativepath
        output_file = outputpath + '/' + relativepath
        print('复制文件:' + input_file)
        shutil.copyfile(input_file, output_file)

if __name__ == "__main__":
    os.chdir(sys.path[0])

    workpath = os.getcwd()
    inputpath = workpath
    outputpath = workpath
    if len(sys.argv) > 1 :
        inputpath = sys.argv[1]

    if len(sys.argv) > 2 :
        outputpath = sys.argv[2]

    outputfolder = outputpath + "/copy"
    if not os.path.isdir(outputfolder) :
        os.makedirs(outputfolder)

    document = open(workpath + "/config.txt", "r")
    lists = document.readlines()
    for line in lists:
        string = line.replace('\n', '')
        path = string.replace(' ', '')
        CopyFileToOutputFolder(inputpath, outputfolder, path)

    print('copy finish')
