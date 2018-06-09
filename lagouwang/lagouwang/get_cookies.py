# --*-- coding:utf8 --*--

from selenium import  webdriver
from scrapy.selector import Selector
import time

def login_lagou():
    browser = webdriver.Chrome(executable_path=r"D:\Richard\python\unit_test\drivers\chromedriver.exe")
    browser.get("https://passport.lagou.com/login/login.html")
    browser.find_element_by_css_selector("body > section > div.left_area.fl > div:nth-child(2) > form > div:nth-child(1) > input").send_keys("1010512178@qq.com")
    browser.find_element_by_css_selector("body > section > div.left_area.fl > div:nth-child(2) > form > div:nth-child(2) > input").send_keys("lo911027")
    browser.find_element_by_css_selector("body > section > div.left_area.fl > div:nth-child(2) > form > div.input_item.btn_group.clearfix > input").click()
    cookie_dict = {}
    time.sleep(3)
    Cookies = browser.get_cookies()
    for cookie in Cookies:
        cookie_dict[cookie['name']] = cookie['value']

    return cookie_dict