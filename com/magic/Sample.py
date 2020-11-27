import re
import urllib
from datetime import time
import random
import time as ztime
import  requests
from bs4 import BeautifulSoup
import json
import redis

def __initRedis():
    pool=redis.ConnectionPool(host='106.13.187.194',password='123', port=6379, db=1)
    r = redis.Redis(connection_pool=pool)
    r.pubsub_channels('category')
    return r
def __goPage(menu,pageUrl,top):
    print('一级目录：'+menu)
    req = requests.get(url=pageUrl)
    req.encoding = 'utf-8'
    html = req.text
    features = "html.parser"
    secList=[]
    bf = BeautifulSoup(html, 'html.parser')
    for div in bf.findAll('div',class_="list-flout"):
        secName=div.div.h2.get_text()
        print('二级目录-----'+secName)
        treeList=[]
        secMeu = {'id': str(int(ztime.time())), 'name': secName.strip(), 'href': div.div.h2.a['href'], 'level': 2}
        for lis in div.ul:
            for li in lis:
                soup = BeautifulSoup(str(li),'html.parser')

                threeNode = {'id': str(int(ztime.time())), 'level': 3}
                if soup.find('img',class_='img-1') is not None:
                    threeNode['img']='http://www.zhizaoyun.com/brochure/'+soup.find('img',class_='img-1')['src']
                if soup.get_text().strip() != '':
                    #print('三级-------' + soup.a.get_text())
                    threeNode['name']=soup.a.get_text().strip()
                    treeList.append(threeNode)
        secMeu['children']=treeList
        secList.append(secMeu)
    top['children'] = secList
def __saveImg(path):
    pass
if __name__ == '__main__':
    redisOpt = __initRedis()
    menuTop={'通用机械零部件':'class01.html','工厂自动化零件':'class02.html','减速机/变速器':'class03.html','液压/气动元件':'class04.html','电机':'class05.html',
             '电工电气':'class06.html','电子元器件':'class07.html','刀具夹具模具':'class08.html','机床及附件':'class09.html','其它':'lass10.html'}
    target = 'http://www.zhizaoyun.com/brochure/'
    nodeList = []
    for k,v in menuTop.items():
        node = {}
        node = {'name': k}
        node['id'] = str(int(ztime.time()))
        node['href'] = target+'/'+v
        node['level'] = 1
        __goPage(k,target+v,node)
        nodeList.append(node)
    print(json.dumps(nodeList))
    redisOpt.setex('category_s', 600000, json.dumps(nodeList))
    redisOpt.close()





