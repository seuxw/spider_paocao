#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 创建数据库表及数据库配置文件

import configparser
import os

import pymysql

# 待连接数据库基础信息
database_info = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "passwd": "",
    "db": "spider_data",
    "charset": "utf8"
}


def create_database(path, passwd):
    """创建数据库表."""
    os.system(
        "mysql -u root -p{passwd} < {path}create_database.sql".format(path=path, passwd=passwd))


def create_database_cfg(path, passwd):
    """创建数据库配置文件."""
    CONFIG_FILE = "{path}database.cfg".format(path=path)
    conf = configparser.ConfigParser()
    database_info["passwd"] = passwd
    conf.read_dict({"DATABASE_INFO": database_info})
    conf.write(open(CONFIG_FILE, 'w'))


def connect_test(path):
    """数据库连接测试."""
    conf = configparser.ConfigParser()
    conf.read("{path}database.cfg".format(path=path))
    conn = pymysql.connect(host=conf["DATABASE_INFO"]["host"], port=int(conf["DATABASE_INFO"]["port"]), user=conf["DATABASE_INFO"]["user"],
                           passwd=conf["DATABASE_INFO"]["passwd"], db=conf["DATABASE_INFO"]["db"], charset=conf["DATABASE_INFO"]["charset"])
    cur = conn.cursor()
    cur.execute("select * from s_paocao limit 1")
    conn.commit()
    conn.close()
    cur.close()
    return 0


def init_database(passwd=None):
    """初始化数据库及配置文件."""
    if passwd:
        path = "./database/"
    else:
        passwd = input("请输入数据库root密码：")
        path = ""
    create_database(path, passwd)
    create_database_cfg(path, passwd)
    if connect_test(path) == 0:
        print("Success create database.")


if __name__ == "__main__":
    init_database()
