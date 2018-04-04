#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 初始化运行环境及配置

import configparser

from database.create_database import init_database


def create_spider_cfg(card_no, card_passwd):
    """创建爬虫配置文件.

    创建爬虫调用的一卡通信息配置.

    Args:
        card_no: 待调用一卡通号
        card_passwd: 待调用一卡通密码
    """
    CONFIG_FILE = "spider.cfg"
    conf = configparser.ConfigParser()
    conf.add_section('CARD_INFO')
    conf.set('CARD_INFO', 'card_no', card_no)
    conf.set('CARD_INFO', 'card_passwd', card_passwd)
    conf.write(open(CONFIG_FILE, 'w'))


def run_create_database(database_passwd):
    """调用create_database.py配置数据库."""
    init_database(database_passwd)


if __name__ == "__main__":
    card_no = input("请输入待调用一卡通号：")
    card_passwd = input("请输入待调用一卡通密码：")
    database_passwd = input("请输入数据库root密码：")
    create_spider_cfg(card_no, card_passwd)
    run_create_database(database_passwd)
    print("Success set spider.cfg")
