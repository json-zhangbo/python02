import re
import urllib
from datetime import time
import random
import time as ztime
import  requests
import json
from bs4 import BeautifulSoup
import http.cookiejar
from urllib import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import redis
import pymysql
import com.magic.DBHelper

def __importItem(db,cursor,sql):
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    db.close()
def __showPage(target):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    # print(PROJECT_ROOT)
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    browser = webdriver.Chrome(executable_path=DRIVER_BIN)

    print('开始获取展示页')
    req = requests.get(url=target)
    html = req.text
    req.encoding = 'utf-8'
    features = "html.parser"
    soup = BeautifulSoup(html, features)
    try:
        for div in soup.find_all('div',class_='pic-cnt'):
            for a in div.find_all('a'):
                print(a.get('href'))

                browser.get(a.get('href'))
                xiazai=browser.find_element_by_class_name('browser')
                print(xiazai)
                #xiazai.click()
    finally:
      browser.close()
      browser.quit()
def __initRedis():
    pool=redis.ConnectionPool(host='106.13.187.194',password='123', port=6379, db=1)
    r = redis.Redis(connection_pool=pool)
    r.pubsub_channels('category')
    return r

if __name__ == '__main__':
    redisOpt = __initRedis()
    #browser = webdriver.PhantomJS()
    target = 'http://www.zhizaoyun.com/model/index.html'
    req = requests.get(url=target)
    req.encoding = 'utf-8'

    html = req.text
    features = "html.parser"
    bf = BeautifulSoup(html, 'html.parser')

    for div in bf.find_all('div',class_='cate-menu-box'):

        # 行业设备
        firsetMenu = div.li.h4.a.get_text()
        # 目录href
        firsetMenuHref = div.a['href']

        #一级目录下的热点分类
        host_words_herf=div.li.p.find_all('a')
        #print(host_words_herf)
        secRight=div.find_all('div',class_='cate-detail-left')
        children = []
        for secMeun in secRight:
            secs=secMeun.find_all('div',class_='J_CatItem cat-item')
            for sec in secs:
                secName=sec.h5.find_all('p')[0].get_text()
                secHref=sec.h5.find_all('p')[1].find('a').get('href')
                #print(sec.h5.p.find('a',class_='more-detail'))

                for lis in sec.find_all('ul'):
                    #print(lis)
                    for li in lis.find_all('a'):
                        print(li.get_text())
                        #href=li.get('href')
                        __showPage(li.get('href'))

    #redisOpt.set("Dcategory", json.dumps(nodeList))
    #redisOpt.setex('category_e',600000,1)
    #redisOpt.close()
