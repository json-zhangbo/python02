from urllib import request
from html.parser import HTMLParser

# 定义HTMLParser的子类,用以复写HTMLParser中的方法
class MyHTMLParser(HTMLParser):

    # 构造方法,定义data数组用来存储html中的数据
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []

    # 覆盖starttag方法,可以进行一些打印操作
    def handle_starttag(self, tag, attrs):
        pass
        # print("Start Tag: ",tag)
        # for attr in attrs:
        #   print(attr)

    # 覆盖endtag方法
    def handle_endtag(self, tag):
        pass

    # 覆盖handle_data方法,用来处理获取的html数据,这里保存在data数组
    def handle_data(self, data):
        if data.count('\n') == 0:
            self.data.append(data)


if __name__=="__main__":
    htmlFile=request.urlopen('http://search.zhizaoyun.wang/drawing.html?sk=5py65bqK')
    content = htmlFile.read()
    # 创建子类实例
    parser = MyHTMLParser()
    # 将html数据传给解析器进行解析
    parser.feed(content)

