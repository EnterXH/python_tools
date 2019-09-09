# -*- coding: utf-8 -*-

import os
import sys
import xlrd
import json

#是否转成一个字典 True/False
IsDict = True

# 如果是字典 需要定义第几列为dic的key（作为key的列之前的内容无效）
# 如果不是一个字典，则是0
DictKey = 1
if not IsDict:
    DictKey = 0

# 当前行用来定义单元格的数据类型
# 基础类型：数字int 浮点数float 字符串 string
# 符合类型：数组list<int> 字典list<mode_type:int, move_value:string>
DataTypeLineIndex = 2

# 当前行作为key
KeyLineIndex = 3


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
    # 总数据
    jsonData = []
    if IsDict:
        jsonData = {}
    # 数据类型
    dataCellType = {}
    for h in range(DictKey-1, sheet.ncols):
        dataCellType[h] = handleDataType(sheet.cell_value(DataTypeLineIndex-1, h))
    # for key in dataCellType:
    #     print(str(key)+':'+ str(dataCellType[key]))

    dataCellKey = {}
    for h in range(DictKey, sheet.ncols):
        dataCellKey[h] = sheet.cell_value(KeyLineIndex-1, h)
    # for key in dataCellKey:
    #     print(str(key)+':'+ str(dataCellKey[key]))

    for w in range(KeyLineIndex, sheet.nrows):
        key = ""
        value = {}
        for h in range(0, sheet.ncols):
            cell = sheet.cell_value(w, h)
            if DictKey - 1 == h:
                # 需要把key转成对应的类型
                dataType = dataCellType[h]
                if dataType != '':
                    key = handleStringByType(cell, dataType['type'])
            else:
                value[dataCellKey[h]] = handleCellData(cell, dataCellType[h])

        if IsDict == True:
            jsonData[key] = value
        else:
            jsonData.append(value)
    return json.dumps(jsonData, indent = 4)

def writeToFile(outpath, filename, data):
    # 生成输出文件夹
    if not os.path.isdir(outpath) :
        os.makedirs(outpath)

    filepath = outpath + '/' + filename + '.json'
    print(filepath)
    document = open(filepath, 'w');
    document.write(data)
    document.close()

if __name__ == "__main__":
    os.chdir(sys.path[0]) # 修改当前工作目录为py脚本所在目录

    # 输入路径
    workpath = os.getcwd()
    xmlfile = sys.argv[1]
    outputpath = workpath
    if len(sys.argv) > 2 :
        outputpath = sys.argv[2]
    print("workpath:" + workpath)
    print("inputpath:" + xmlfile)
    print("outputpath:" + outputpath)

    # 打开excel文件
    workbook = xlrd.open_workbook(xmlfile)
    # 获取所有sheet
    for index in range(workbook.nsheets):
        sheet = workbook.sheet_by_index(index)
        print(sheet.name, "列：", sheet.ncols, "行：", sheet.nrows)
        json_string = HandleSheetData(sheet, index)

        # print(json_string)
        # 写入文件
        writeToFile(outputpath, sheet.name, json_string)

    print('数据转换完成')
