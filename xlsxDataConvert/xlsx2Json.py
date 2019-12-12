# -*- coding: utf-8 -*-

import os
import sys
import xlrd
import json

# 有效的起始列
BeginNcolsIndex = 0
# 有效的起始行
BeginNrowsIndex = 4

# 数据类型处理函数
def handleDataType(string):
    data = {}
    if string == "int" or string == "float" or string == "string":
        data["type"] = string
    else:
        string = string.replace('list<', '')
        string = string.replace('>', '')
        if string == "int" or string == "float" or string == "string":
            data["type"] = "list"
            data["value"] = string
        else:
            data["type"] = "dict"
            key_values = string.split(',')
            if len(key_values) == 2:
                key_type = key_values[0].split(':')
                if len(key_type) == 2:
                    data["key"] = key_type[0]
                    data["key_type"] = key_type[1]
                else:
                    print("error key")

                value_type = key_values[1].split(':')
                if len(value_type) == 2:
                    data["value"] = value_type[0]
                    data["value_type"] = value_type[1]
                else:
                    print("error value")
            else:
                print("类型错误")
    return data

def handleStringByType(value, ptype):
    if ptype == 'int':
        if value == '':
            return 0
        return int(value)
    elif ptype == 'float':
        if value == '':
            return 0
        return float(value)
    return value

# 解析dict数据
def handleDictData(string, ptype):
    data = []
    if string == '':
        return data
    key = ptype['key']
    key_type = ptype['key_type']

    value = ptype['value']
    value_type = ptype['value_type']

    data_list = string.split('&')
    for v in data_list:
        v_list = v.split(',')
        if len(v_list) == 2:
            d = {}
            d[key] = handleStringByType(v_list[0], key_type)
            d[value] = handleStringByType(v_list[1], value_type)
            data.append(d)
    return data

# 解析list数据
def handleListData(value, ptype):
    data = []
    if value == '':
        return data

    typeValue = ptype['value']
    data_list = value.split('&')
    for v in data_list:
        data.append(handleStringByType(v, typeValue))
    return data

# 单元格数据处理函数
def handleCellData(value, dataType):
    # print("cell=", value, dataType, dataType['type'])
    ptype = dataType["type"]
    if ptype == 'list':
        return handleListData(value, dataType)
    elif ptype == 'dict':
        return handleDictData(value, dataType)
    return handleStringByType(value, ptype)

# sheet数据处理
def HandleSheetData(sheet, index):
    isDict = False
    if sheet.cell_value(0, 0) == "dict":
        isDict = True
    # 总数据
    jsonData = []
    if isDict:
        jsonData = {}
    # 数据类型，第二行定义数据类型
    dataCellType = {}
    for h in range(0, sheet.ncols):
        dataCellType[h] = handleDataType(sheet.cell_value(2, h))
    # for key in dataCellType:
    #     print(str(key)+':'+ str(dataCellType[key]))

    dataCellKey = {}
    for h in range(0, sheet.ncols):
        dataCellKey[h] = sheet.cell_value(3, h)
    # for key in dataCellKey:
    #     print(str(key)+':'+ str(dataCellKey[key]))

    for w in range(BeginNrowsIndex, sheet.nrows):
        key = ""
        value = {}
        for h in range(BeginNcolsIndex, sheet.ncols):
            cell = sheet.cell_value(w, h)
            if isDict and h == 0:
                # 需要把key转成对应的类型
                dataType = dataCellType[h]
                if dataType != '':
                    key = handleStringByType(cell, dataType['type'])
            else:
                value[dataCellKey[h]] = handleCellData(cell, dataCellType[h])

        if isDict == True:
            jsonData[key] = value
        else:
            jsonData.append(value)
    return json.dumps(jsonData, indent=4,ensure_ascii=False)

def writeToFile(outpath, filename, data):
    # # 生成输出文件夹
    if not os.path.isdir(outpath) :
        os.makedirs(outpath)

    filepath = outpath + '/' + filename + '.json'
    # print("filepath = ", filepath)
    # print("data = ", data)
    document = open(filepath, 'w')
    document.write(data)
    document.close()

# 是否 excel 文件
def isExcelFile(path): 
    extension = os.path.splitext(path)[1]
    if extension == ".xls" or extension == ".xlsx" :
        return True
    return False

def handleExcel(path, outputpath):
    # 打开excel文件
    print("需要转换的文件名=", path)
    workbook = xlrd.open_workbook(path)
    # 获取所有sheet
    for index in range(workbook.nsheets):
        sheet = workbook.sheet_by_index(index)
        print(sheet.name, "列：", sheet.ncols, "行：", sheet.nrows)
        json_string = HandleSheetData(sheet, index)
        # 写入文件
        writeToFile(outputpath, sheet.name, json_string)

if __name__ == "__main__":
    os.chdir(sys.path[0]) # 修改当前工作目录为py脚本所在目录

    # 输入路径
    workpath = os.getcwd()
    outputpath = workpath
    if len(sys.argv) > 1 :
        outputpath = sys.argv[1]
    print("输出路径:" + outputpath)
    # 所有非隐藏文件
    for root, dirs, files in os.walk(workpath):
        files = [f for f in files if not f[0] == '.' and not f[0] == '~']
        for file_name in files:
            if isExcelFile(file_name):
                abspath = os.path.join(root, file_name)
                handleExcel(abspath, outputpath)
    print('数据转换完成')
