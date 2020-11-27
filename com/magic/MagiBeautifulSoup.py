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

if __name__ == '__main__':
    target = 'http://search.zhizaoyun.wang/drawing.html?sk=6L2m5bqK'
    req = requests.get(url=target)
    req.encoding = 'utf-8'

    html = req.text
    features = "html.parser"
    bf = BeautifulSoup(request.urlopen(target),features)

    #bf = BeautifulSoup(html,features)
    soup = bf.select('.clear modelLst')
    # 这里转化为BeautifulSoup 对象
    print(soup)
    pass



