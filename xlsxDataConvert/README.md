<center>excel数据转换</center >
===
---

#### 环境需求
需要python3和xlrd模块

	> python3下载
		
	> mac环境可以通过 `pip install xlrd` 获取xlrd模块
		
	> win环境，自行搜索下载安装
	
		https://pypi.org/project/xlrd/
	
#### 使用
脚本执行会根据xlsx中的sheet名称生成不同的json文件

每个sheet对应一个json

	python FileCopy.py xlsx文件 #输出目录
	
	> 参数1 xlsx文件路径
	> 参数2 输出路径（如果不填则默认输出到脚本所在目录）

#### xlsx格式说明

* 第一行 可以写个描述，这一行没实际意义
* 第二行 定义当前列单元格的数据类型
	
	* int
	* float
	* string
	* list<string | int | float> 数组

			[
            	"101",
            	"102",
            	"103"
        	],
		
	* dict key-value键值对 list<key:string, value:int>

            {
                "monsterid": "101",
                " weight": 5
            },
	
* 第三行 数据的key

关卡ID | 章节 | 名字 | 可出现怪物ID列表 | 怪物出现权重
:-: | :-: | :-: | :-: | :-:
int   |int| string| list\<int> | list\<monsterid:string, weight:int>
level_id| chapter_id | name | monter_list | monster_weight 
10001 | 1 | 仙境 | 101&102&103 | 101,5&102,5&103,6
10002 | 2 | 沙漠 | 101&102&103 | 101,5&102,5&103,6
10003 | 3 | 机械 | 101&102&103 | 101,5&102,5&103,6

#### 输出格式介绍
* 输出的json可以是dict或者array
* 可以在py脚本中修改配置

	> array格式
	
	> IsDict = False
	
	> DictKey 如果xlsx表中前 N 列数据无效，则设置 DictKey = N
	
	--

	>  dict格式
	
	>  IsDict = True
	
	>  DictKey key在第 N 列, 则 DictKey = N   (key所在列的前面的是无效的)
	
		import os
		import sys
		import xlrd
		import json
		
		# 是否是一个字典 True/False
		IsDict = False
		
		# 如果是字典 需要定义第几列为dic的key（作为key的列之前的内容无效）
		# 如果不是一个字典，则是0
		DictKey = 0

--
### dict格式示例
~~~json
{
    "70001": {
        "chapter_id": 1,
        "name": 1.0,
        "monter_list": [
            101,
            102,
            103
        ],
        "monster_weight": [
            {
                "monsterid": "101",
                " weight": 5
            },
            {
                "monsterid": "102",
                " weight": 5
            },
            {
                "monsterid": "103",
                " weight": 6
            }
        ]
    },
    "70002": {
        "chapter_id": 1,
        "name": 1.0,
        "monter_list": [
            101,
            102,
            103
        ],
        "monster_weight": [
            {
                "monsterid": "101",
                " weight": 5
            },
            {
                "monsterid": "102",
                " weight": 5
            },
            {
                "monsterid": "103",
                " weight": 6
            }
        ]
    }
}
~~~

### array格式示例
	
~~~json
[
    {
        "level_id": 70001,
        "chapter_id": 1,
        "name": 1.0,
        "monter_list": [
            101,
            102,
            103
        ],
        "monster_weight": [
            {
                "monsterid": "101",
                " weight": 5
            },
            {
                "monsterid": "102",
                " weight": 5
            },
            {
                "monsterid": "103",
                " weight": 6
            }
        ]
    },
    {
        "level_id": 70002,
        "chapter_id": 1,
        "name": 1.0,
        "monter_list": [
            101,
            102,
            103
        ],
        "monster_weight": [
            {
                "monsterid": "101",
                " weight": 5
            },
            {
                "monsterid": "102",
                " weight": 5
            },
            {
                "monsterid": "103",
                " weight": 6
            }
        ]
    }
]
~~~
 
 


