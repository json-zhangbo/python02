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
def __paqudata(threedTarg,targetUrl):

    # 调用浏览器
  try:

    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    chrome_options.add_argument('--user-data-dir=/Users/zhangbo/magicworkspace/website/data')
    #chrome_options.add_argument('--user-data-dir=/usr/local/share/chromedriver')
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')
    #chrome_options.set_headless()
    # 启动浏览器，获取网页源代码
    #browser = webdriver.Chrome(chrome_options=chrome_options)
    #browser.get(targetUrl)
    #li_data=browser.find_element_by_class_name("clear modelLst").find_elements('li')
    #print('--------')
    #print(li_data)

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    #print(PROJECT_ROOT)
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

    browser = webdriver.Chrome(executable_path=DRIVER_BIN)

    browser.get(targetUrl)
   # browser.maximize_window()
    wait = WebDriverWait(browser, 10)
    #wait.until(EC.presence_of_element_located((By.CLASS_NAME, "clear modelLst")))

    soup = BeautifulSoup(browser.page_source, 'html.parser')

    content=soup.findAll('ul',class_='clear modelLst')

    upFile(threedTarg,content)

    #当前时间戳10位
    #ztime.sleep(random.randint(1, 9))  # 设置时间间隔为随机几秒钟
    strTime=str(int(ztime.time()))

    searchParam=targetUrl[str(targetUrl).index("sk=")+3:]
    #print('参数=='+searchParam)
    payloadHeader = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': 'Hm_lvt_1d0389e32778cad3401b072f108fb294=1574745354,1574746224; '
                  'Hm_lvt_6d0c6f3521dfad65307b120c3dbc89bc=1574745199,1575599302,1575858201,1575863128; '
                  'BAIDU_SSP_lcr=http://www.zhizaoyun.wang/drawing/index.html; '
                  'Hm_lvt_39fb27686eb5c3825c44fce8952ce6d0=1575863128,1575870821,1575870853,1575870865;'
                  ' Hm_lvt_cff8684ae900a7d385ed4c9cb8ab829d=1575863130,1575870821,1575870853,1575870865; '
                  'Hm_lvt_ac5827d87107aa017ca84a83ac6bd1a1=1575863128,1575870821,1575870853,1575870865; '
                  'Hm_lvt_89885298c1eb20141ea8e35bf9ac8020=1574745218,1574746887,1575871123; '
                  'Hm_lpvt_89885298c1eb20141ea8e35bf9ac8020=1575871123; '
                  'Hm_lpvt_6d0c6f3521dfad65307b120c3dbc89bc='+strTime+'; '
                  'Hm_lpvt_39fb27686eb5c3825c44fce8952ce6d0='+strTime+';'
                  ' Hm_lpvt_cff8684ae900a7d385ed4c9cb8ab829d='+strTime+'; '
                  'Hm_lpvt_ac5827d87107aa017ca84a83ac6bd1a1='+strTime+'',
        'Host': 'search.zhizaoyun.wang',
        'Origin':'http://search.zhizaoyun.wang',
        'Referer': str(targetUrl),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    url = 'http://search.zhizaoyun.wang/nds_requests/ResourceSearch/GetResourceListByLabel'
    postdata1 = {"labelId" :  3,
        "startCount" :  0,
        "pageCount" :  20,
        "fileType" :  "",
        "firstAndSecondCategoryList" : "",
        "freeId" :  "",
        "isGetCount" :  "",
        "isModel" : 0,
        "isWap" :  False,
        "orderId" :  "",
        "searchContent" :  searchParam}

    #conn = requests.session()
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5733.400 QQBrowser/10.2.2019.400'}
    #repHtml = conn.post(url, data=json.dumps(postdata1), headers=payloadHeader,timeout=30)

    #通过request 访问
    #repHtml = requests.post(url,json.dumps(postdata1), headers=payloadHeader,timeout=30)

    #print(repHtml.text)
    #print(repHtml)
  finally:
    browser.close()
    browser.quit()
def upFile(threedTarg,content):
    print('开始打印 '+threedTarg+'内容')
    print(content)
    imgs=__getBeautifulSoup__(content).findAll('img')
    print(imgs)
    for img in __getBeautifulSoup__(imgs):
        src=__getBeautifulSoup__(img)

        print(img.src)
        strTime = str(int(ztime.time()))
        fileBathSavePath='/Users/zhangbo/magicworkspace/website/data/images'
        if src is None:
           return

        if os.path.exists(threedTarg):
           os.chdir(threedTarg)  # 切换路径至上面创建的文件夹
        else:
           os.mkdir(threedTarg)  # 创建文件夹
           os.chdir(threedTarg)  # 切换路径至上面创建的文件夹
           os.mkdir(threedTarg)
           os.chdir(threedTarg)

        img = requests.get(src)
        file_name = strTime+'.png'
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        f.close()
        print('保存图片结束')
def savePic(self,url):
    heads={
        "Referer":self.url
    }
    os.mkdir('/')
def __getBeautifulSoup__(html):
    return BeautifulSoup(str(html), 'html.parser')
def __importData(data):
     # 打开数据库连接
     db = pymysql.connect("106.13.187.194", "root", "123456", "magic_material")
     db.ping(reconnect=True)
     cursor = db.cursor()
     i=0
     try:
         for item in data:
             i=i+1
             name=item["name"]

             print(cursor.rownumber)
             print('----------------')

             sql = 'INSERT INTO m_category(name,parent_id, category_order)VALUES ("'+name+'", 0, 1)'
             cursor.execute(sql)
             cateGoryPath='0|'+str(cursor.lastrowid)

             print(cursor.lastrowid)
             sqlupdate='update m_category set category_path="'+cateGoryPath+'"'+' where category_id='+str(cursor.lastrowid)
             sqlupdate.join(" where category_id=").join(str(cursor.lastrowid))
             print(sqlupdate)
             cursor.execute(sqlupdate)
             for sortSec in item['children']:
                 sqlSec='INSERT INTO m_category(name,parent_id, category_order)VALUES ("'+sortSec["name"]+'", cursor.lastrowid, 1)'
                 cursor.execute(sqlSec)
         db.commit()
         cursor.close()
     except:
         db.rollback()
     db.close()

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
    redisOpt=__initRedis()
    categoryDic={}
    target = 'http://www.zhizaoyun.wang/drawing/index.html'
    req = requests.get(url=target)
    req.encoding = 'utf-8'

    html = req.text
    features = "html.parser"
    bf = BeautifulSoup(html,'html.parser')
    texts = bf.find_all('div', class_='fenlei-list')
    #print(texts)
    #这里转化为BeautifulSoup 对象
    soup=BeautifulSoup(str(texts),'html.parser')

    alldivs=soup.div
    nodeList=[]
    print(len(alldivs))
    for div in alldivs:
        node = {}
        level1Nmae = __getBeautifulSoup__(div).a
        levle1Bop = BeautifulSoup(str(level1Nmae),'html.parser')
        node1Text = levle1Bop.get_text()

        # print(secondeLevel)
        if node1Text != 'None':
            node = {"name": node1Text}
            href = levle1Bop.a['href']
            print("一级目录：" + node1Text)
            print(href)

            if str(href).find("sk=") < 0:
                node['id']=str(int(ztime.time()))
                #continue
            else :
                node['id']=href[str(href).find("sk=") + 3:]


            node['href'] = href
            node['level'] = 1
            print(node)
             #redisOpt.hget(node1Text,href[str(href).index("sk=") + 3:],href)#加入reids 一级目录
        secondeLevel = __getBeautifulSoup__(div).findAll("div", class_="J_CatItem cat-item")

        i=0
        children = []
        for seconde in secondeLevel:
            if len(seconde)>0:

                h5=__getBeautifulSoup__(seconde).h5
                p=__getBeautifulSoup__(h5).findAll('p')
                secondHref=__getBeautifulSoup__(p[1]).a['href']
                secondText=__getBeautifulSoup__(p[0]).getText()
                #获得二级目录 以及href
                print('*********************')
                #print("二级目录："+secondText)
                #print("二级目录href："+secondHref)
                i=i+1

                secondNodes={'id':href[str(secondHref).find("sk=") + 3:],'name':secondText,'href':secondHref,'level':2}



                threeLevel = __getBeautifulSoup__(seconde).findAll('li')
                threeChildren = []
                # 开始获取三级目录
                for three in __getBeautifulSoup__(threeLevel):
                    if len(three) > 0 :
                        a=__getBeautifulSoup__(three).find('a')
                        if a is not None:
                          threeName=__getBeautifulSoup__(a).get_text()
                          threeHref=__getBeautifulSoup__(three).a["href"]
                          #print("三级目录:"+threeName)
                          #print(str(threeHref))
                          threeNode={'id':threeHref[str(threeHref).find("sk=") + 3:],'name':threeName,'href':str(threeHref),'level':3}
                          threeChildren.append(threeNode)
                          #__paqudata(__getBeautifulSoup__(a).get_text(),__getBeautifulSoup__(three).a["href"])
                secondNodes['children'] =threeChildren
                children.append(secondNodes)
                node['children']=children
        print('获取节点数据')

        if len(node) >0:
         #ßprint(node)
         nodeList.append(node)
    print(json.dumps(nodeList))
    redisOpt.set("category",json.dumps(nodeList))
    redisOpt.close()
    #__importData(nodeList)

