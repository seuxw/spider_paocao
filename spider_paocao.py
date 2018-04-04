#!/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser
import ctypes
import inspect
import json
import logging
import logging.config
import os
import re
import threading
import time

import gevent
from gevent import monkey, pool
monkey.patch_all()
import pymysql
import requests
import yaml

from sele import sele


ISOTIMEFORMAT = "'%Y-%m-%d %H:%M:%S'"


def get_paocao(page_str, JSID, get_paocao_list):
    """爬取用户跑操总次数.

    Args:
        page_str: 用于教工查询的跑操页面所对应的Url的pageStr参数，范围从1到50
        JSID: Sele获取的JSID参数，用于验证身份
        get_paocao_list: 用于保存查询结果的List容器，每个元素为('一卡通号', '性别', '入学年份')

    Return:
        通过引用get_paocao_list返回查询结果
        return 0: 获取跑操成功
        return -1: 获取跑操失败

    Raises:
        TODO(ZZccchen):
    """
    logger.info("Start get_paocao %d", page_str)
    paocao_url = "http://zccx.seu.edu.cn/SportWeb/gym/gymExercise/gymExercise_query_resultCnt.jsp?pageStr=%d" % (
        page_str)
    paocao_cook = requests.cookies.RequestsCookieJar()
    paocao_cook.set("JSESSIONID", JSID, domain="seu.edu.cn",
                    path="/", secure=False)
    paocao_cook.set("AMAuthCookie", "AQIC5wM2LY4SfcynM1CC9f%2BLwtQrnVpiyoTkY%2B96MOUyCdo%3D%40AAJTSQACMDE%3D%23",
                    domain="zccx.seu.edu.cn", path="/", secure=False)
    paocao_cook.set("amlbcookie", "01", domain="seu.edu.cn",
                    path="/", secure=False)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
        "Cookie": "JSESSIONID={jsid}; amlbcookie=01; iPlanetDirectoryPro=AQIC5wM2LY4SfcynM1CC9f%2BLwtQrnVpiyoTkY%2B96MOUyCdo%3D%40AAJTSQACMDE%3D%23".format(jsid=JSID)
    }

    paocao_req = requests.get(
        paocao_url, headers=headers, cookies=paocao_cook, timeout=60)

    paocao_text = paocao_req.text

    paocao_re = """<td width=.+align="center">(.+)</td>[.\n\s\D]+<td width=.+align="center">.+</td>[.\n\s\D]+<td width=.+align="center">(.+)</td>[.\n\s\D]+<td width=.+align="center">.+</td>[.\n\s\D]+<td width=.+align="center">.+</td>[.\n\s\D]+<td width=.+align="center">(.+)</td>[.\n\s\D]+<td width=.+align="center"><font style="cursor:hand;" color="blue" onClick="window.open"""
    i = re.findall(paocao_re, paocao_text)
    if i:
        get_paocao_list.extend(list(i))
        logger.info("Success get paocao %d", page_str)
        return 0
    else:
        logger.error("Fail get paocao %d", page_str)
        return 0


def get_paocao_info(cardNo, JSID):
    # TODO：用户跑操详情查询
    pass


def connect_database():
    """数据库连接方法."""
    logger.info("Connect database")
    conf = configparser.ConfigParser()
    conf.read("./database/database.cfg")
    conn = pymysql.connect(host=conf["DATABASE_INFO"]["host"], port=int(conf["DATABASE_INFO"]["port"]), user=conf["DATABASE_INFO"]["user"],
                           passwd=conf["DATABASE_INFO"]["passwd"], db=conf["DATABASE_INFO"]["db"], charset=conf["DATABASE_INFO"]["charset"])
    cur = conn.cursor()
    return conn, cur


def update_database(paocao_list):
    """数据库更新."""
    conn, cur = connect_database()

    logger.info("Start update database")
    if not paocao_list:
        logger.error("Empty paocao list")
        logger.error("Fail update database")
        return
    insert_into_sql = """
        insert into 
            s_paocao (card_no,count_paocao,modify_date) 
        values 
            {insert_part} 
        on duplicate key update 
            count_paocao=values(count_paocao), 
            modify_date=values(modify_date);
        """
    insert_part_item = "({card_no},{count_paocao},{modify_date})"

    insert_part = []
    for i in paocao_list:
        insert_part.append(
            insert_part_item.format(
                card_no=pymysql.escape_string(i[0]),
                count_paocao=pymysql.escape_string(i[2]),
                modify_date=time.strftime(ISOTIMEFORMAT, time.localtime())
            )
        )
    cur.execute(insert_into_sql.format(insert_part=",".join(insert_part)))
    conn.commit()
    logger.info("Success update database")
    cur.close()
    conn.close()
    logger.info("Disconnect database")


def start_logging(default_path="./log/logging.yaml", default_level=logging.INFO, env_key="LOG_CFG"):
    """logging模块配置."""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def loop_thread():
    """跑操爬虫线程."""
    try:
        logger.info("Start loop thread")
        jsid = sele()
        time.sleep(10)

        logger.info("Start gevent")
        task_list = []
        get_paocao_list = []
        p = pool.Pool(10)
        for i in range(1, 51):
            task_list.append(p.spawn(get_paocao, i, jsid, get_paocao_list))
        gevent.joinall(task_list)
        logger.info("Success gevent")
        update_database(get_paocao_list)
        logger.info("End loop thread")

    except Exception as e:
        logger.exception("Fail loop thread")


def stop_thread(thread):
    """未执行完线程终止."""
    tid = ctypes.c_long(thread.ident)
    exctype = SystemExit
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    logger.warning("Kill timeout loop thread")


def main():
    """主程序.

    每次执行时创建一个线程，执行完毕自动回收，
    当线程执行超时时，强行终止，
    超时时间为1200s
    """
    start_logging()
    global logger
    logger = logging.getLogger("spider_paocao.py")
    logger.info("Start main thread")
    while(True):
        t = threading.Thread(target=loop_thread)
        t.start()
        time.sleep(1200)
        if t.is_alive() == True:
            stop_thread(t)


if __name__ == "__main__":
    main()
