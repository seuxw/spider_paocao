#!/usr/bin/python3
# -*- coding: utf-8 -*-


import configparser
import logging
import os
import time

from PIL import Image
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def sele():
    """身份验证的JSID获取.

    Return:
        若获取成功，则返回JSID字符串，
        若获取失败，则返回空字符串""
    """
    logger = logging.getLogger("sele.py")
    logger.info("Start sele")

    try:
        # phantomjs请求头设置
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
        )

        # 此处取消PhantomJS的log输出，如需输出，请参考以下代码
        # driver = webdriver.PhantomJS(service_log_path='/yourpath/ghostdriver.log')  # 输出log到指定目录
        browser = webdriver.PhantomJS(
            desired_capabilities=dcap, service_log_path=os.path.devnull)  # 取消log输出
        browser.set_page_load_timeout(60)
        browser.set_script_timeout(60)

        # 测试时使用URL
        # browser.get("http://ids1.seu.edu.cn/amserver/UI/Login")
        browser.get("http://zccx.seu.edu.cn")
        browser.set_window_size(1200, 800)

        browser.get_screenshot_as_file("screen.png")
        element = browser.find_element_by_css_selector(
            "body > table:nth-child(2) > tbody > tr:nth-child(2) > td > table:nth-child(1) > tbody > tr:nth-child(5) > td:nth-child(4) > img")

        left = int(element.location['x'])
        top = int(element.location['y'])
        right = int(element.location['x'] + element.size['width'])
        bottom = int(element.location['y'] + element.size['height'])

        im = Image.open('screen.png')
        im = im.crop((left, top, right, bottom))

        # 加入下面一行代码，你可以选择不加入tesseract到你的PATH中
        # pytesseract.pytesseract.tesseract_cmd = '<full_path_to_your_tesseract_executable>'
        # 示例：pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

        code = pytesseract.image_to_string(im)

        im.close()

        elem1 = browser.find_element_by_id("IDToken1")
        elem2 = browser.find_element_by_id("IDToken2")
        elem3 = browser.find_element_by_name("inputCode")

        time.sleep(3)

        conf = configparser.ConfigParser()
        conf.read("spider.cfg")
        elem1.send_keys(conf["CARD_INFO"]["card_no"])
        elem2.send_keys(conf["CARD_INFO"]["card_passwd"])
        elem3.send_keys(code)

        login = browser.find_element_by_css_selector(
            "body > table:nth-child(2) > tbody > tr:nth-child(2) > td > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(5) > img")
        login.click()

        jsid = ""
        for i in browser.get_cookies():
            if i['name'] == 'JSESSIONID':
                jsid = i['value']
                break
        time.sleep(3)
        browser.quit()
        logger.info("Success sele")
        return jsid

    except Exception as e:
        logger.exception("A error happened in running sele.py")
        browser.quit()
        return ""


if __name__ == "__main__":
    print(sele())
