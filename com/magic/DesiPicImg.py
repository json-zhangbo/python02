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

def __initRedis():
    pool=redis.ConnectionPool(host='106.13.187.194',password='123', port=6379, db=1)
    r = redis.Redis(connection_pool=pool)
    r.pubsub_channels('category')
    return r

if __name__ == '__main__':
    redisOpt = __initRedis()
    target = 'http://www.zhizaoyun.com/model/index.html'
    req = requests.get(url=target)
    req.encoding = 'utf-8'

    html = req.text
    features = "html.parser"
    bf = BeautifulSoup(html, 'html.parser')
    nodeList = []
    i=0
    for div in bf.find_all('div',class_='cate-menu-box'):
        node = {}
        # 行业设备
        firsetMenu = div.li.h4.a.get_text()
        # 目录href
        firsetMenuHref = div.a['href']
        node={'name':firsetMenu}
        node['id'] = str(int(ztime.time()))
        node['href'] = firsetMenuHref
        node['level'] = 1
        print(node)
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
                secondNodes = {'id': str(int(ztime.time())), 'name': secName,'href':secHref,'level':2}
                threeChildren = []

                for lis in sec.find_all('ul'):
                    #print(lis)
                    for li in lis.find_all('a'):
                        print(li.get_text())
                        print(li.get('href'))
                        threeNode={'id': str(int(ztime.time())),'name':li.get_text(),'href':li.get('href'),'level':3}
                        threeChildren.append(threeNode)
                        i=i+1
                secondNodes['children']=threeChildren
                print('end.........')
                children.append(secondNodes)
            node['children']=children
        nodeList.append(node)
    print(i)
    #redisOpt.set("Dcategory", json.dumps(nodeList))
    redisOpt.setex('category_e',600000,json.dumps(nodeList))
    redisOpt.close()