# SPIDER_PAOCAO

[![GitHub release](https://img.shields.io/badge/version-v1.0.0(alpha%201)-brightgreen.svg)](https://github.com/seuxw/spider_paocao)
[![GitHub issues](https://img.shields.io/github/issues/seuxw/spider_paocao.svg)](https://github.com/seuxw/spider_paocao/issues)
[![GitHub stars](https://img.shields.io/github/stars/seuxw/spider_paocao.svg)](https://github.com/seuxw/spider_paocao/stargazers)
[![GitHub license](https://img.shields.io/github/license/seuxw/spider_paocao.svg)](https://github.com/seuxw/spider_paocao/blob/master/LICENSE)

东大小微体育系跑操爬虫。

## Table of Contents

+ Requirements
+ Quick Start
+ To Do List
+ History
+ License

## Requirements

爬虫基于python3，下列python依赖库是必须的，同时请安装好 [tesseract-ocr]("https://github.com/tesseract-ocr/tesseract/wiki") 和 [PhantomJS]("http://phantomjs.org/download.html") 并添加入PATH中：

+ pyyaml
+ requests
+ pymysql
+ pillow
+ pytesseract
+ gevent
+ selenium
+ PhantomJS

```bash
# 安装依赖库
pip3 install pyyaml
pip3 install requests
pip3 install pymysql
pip3 install pillow
pip3 install pytesseract
pip3 install gevent
pip3 install selenium
```

+ 对于Linux用户，如果遇到 Permission denied 安装失败，请加上sudo重试
+ 对于Windows用户，如果在安装中出现 “UnicodeDecodeError: 'utf-8' codec can't decode byte 0xce in position 72...” 问题,请使用在控制台输入"chcp 65001"命令，详情参照[此文章]("http://blog.csdn.net/zhyh1435589631/article/details/51303756")
+ 若执行pip3时出现 “Unable to create process using '"'” 请通过 “python3 -m pip install --upgrade pip” 命令升级你的pip
+ 如果您不想将tesseract加入PATH，请参考sele.py中的注释代码
+ 数据库版本为MySQL5.7，如果您使用其他版本的数据库，欢迎将使用中遇到的问题反馈给我们
+ 如果您在使用中遇到其他问题，都可加入此QQ群交流讨论 [小微测试交流群2017]("https://jq.qq.com/?_wv=1027&k=57ZMWxY")

## Quick Start

+ 首次使用时，请执行init.py进行项目初始化（包括数据库初始化和查询使用一卡通配置）。
+ 如果需要修改数据库配置，请修改/database/create_database.sql中相应语句，并执行create_database.py进行配置。
+ 如需再次修改查询使用一卡通配置，可直接修改根目录下spider.cfg或再次执行init.py
+ 请执行spider_paocao.py启动爬虫

## To Do List

+ 优化README描述
+ 用户查询跑操详情查询
+ Linux平台下测试（已完成0%）

## History

+ 更新日志180403
  > [ v1.0.0(alpha 1) ]
  >
  > 版本说明：
  >
  > 尚未完成Linux平台下测试，请勿在生产环境下使用
  >
  > 更新内容：
  >
  > + 通过Windows 10和Windows Server 2012 R2平台下测试
  > + 添加日志文件按日保存及自动删除功能
  > + 添加项目初始化环境并创建配置功能

+ 更新日志180330
  > [ v1.0.0(alpha) ]
  >
  > 欢迎使用东大小微体育系跑操爬虫，这是小微的第一个开源项目，感谢您的批评和指正。如需交流请加入QQ群 [小微测试交流群2017]("https://jq.qq.com/?_wv=1027&k=57ZMWxY")
  >
  > 版本说明：
  >
  > 尚未完成Windows和Linux平台下测试，请勿在生产环境下使用

## License

    The code in this repository is licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

**NOTE**: This software depends on other packages that may be licensed under different open source licenses.