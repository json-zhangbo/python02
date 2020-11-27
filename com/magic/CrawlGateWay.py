import re
import  requests
from urllib import request

class Spider():
    url ='http://www.zhizaoyun.wang/drawing/index.html'
    root_pattern= '<div class="fenlei-list fenlei-nav-list fenlei-list-second fenlei-nav-list-second"></div>'
    name_pattern = '</li>([\s\S]*?)</a>'
    number_pattern = '<ul class="cat-detail">([\s\S]*?)</ul>'


    # 私有方法，获取数据
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')

        return htmls


    # 正则分析html
    def __analysis(self, htmls):
        root_html = re.findall(Spider.root_pattern, htmls)
        test=re.findall(r'<div class="fenlei-list fenlei-nav-list fenlei-list-second fenlei-nav-list-second">',htmls)
        print(test)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = {'name': name, 'number': number}
            anchors.append(anchor)
        return anchors

    # 精炼数据
    def __refine(self, anchors):
        l = lambda anchor: {'name': anchor['name'][0].strip(), 'number': anchor['number'][0]}
        return map(l, anchors)

    # 数据排序
    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    # 显示函数
    def __show(self, anchors):
        for rank in range(0, len(anchors)):
            print('rank' + str(rank + 1) + '  :  ' + anchors[rank]['name'] + '     ' + anchors[rank]['number'])

    # 入口方法（主方法）
    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        result = list(self.__refine(anchors))
        sorted_result = self.__sort(result)
        self.__show(sorted_result)


spider = Spider()
spider.go()