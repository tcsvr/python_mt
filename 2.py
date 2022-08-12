# import requests
# import csv
# import sys
# import pymysql
# import json
# import re
# import parsel
# from bs4 import BeautifulSoup
# from lxml import etree

class DownComment:
    def __init__(self):
        print('111')
        # 爬取数据cookie user—agent
        self.headers = {
            'Host':'www.dianping.com',
            'Referer':'http://www.dianping.com/shop/H33O0wFvNMXGFlH8/review_all',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            "Cookie": '_lxsdk_cuid=18239333babc8-02ea566dfc9fb1-3b3d5203-1fa400-18239333babc8; _lxsdk=18239333babc8-02ea566dfc9fb1-3b3d5203-1fa400-18239333babc8; _hc.v=b018c517-1a1a-ccf4-99cf-688ee3dd297a.1658817036; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1658817037; WEBDFPID=v9uw0770x4uw5y77yzxxzu1y37z15y28817606591uz97958x89w9430-1658903487728-1658817087157EKCSUOQfd79fef3d01d5e9aadc18ccd4d0c95073024; dplet=14841b8927eb16a9c12d1ea5bd9a483b; dper=71f946ccbf29eced86284c799df9d3e5c27880e32819b3a8664b9d4a2531f32b73788d84d67a5ed76f05067875a1281d90ed9367b29f45d84f9063bf93099478f3f3a8c967ca806958d4abeae5d0a15b49ab678c4fa0b2c9c5a2c8f4e9c1c6a5; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_3476436004; ctu=70159c3dea4054244f82221ceea4a625075f3b70f5a599e75a7495cd06d9c4de; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1658892068; _lxsdk_s=1823da14764-010-ca6-8aa%7C%7C26'
        }
        # 爬取大众点评的url
        # self.url = None
        # # 页面返回的text
        # self.text = None
        # # css文件的内容
        # self.css_content = None
        # # css文件的url
        # self.css_url = None
        # # 取出的字体文件的内容
        # self.svg_content = None
        # # 用来存储每一个字的映射关系的列表
        # self.font_d_l = list()
        # # 用来存储坐标映射
        # self.position_l = list()
        # # 字体位置
        # self.position_list = list()
        # # 数据
        # self.data = list()
    # print('self')
    '''  
    def down_css(self):
        print('self.headers')
        # 下载css文件
        # 请求返回的text
        # response = requests.get(url=self.url, headers=self.headers)
        # selector = parsel.Selector(response.text)
      
        self.text = requests.get(self.url, headers=self.headers).text
        # 使用xpath取出所有link中的链接
        x = etree.HTML(self.text)
        print(x)
        css_list = x.xpath('//link/@href')
        self.css_url = 'https:' + str(re.findall('//s3plus\.meituan\.net.+?\.css', ' '.join(css_list))[0])
        
    
    def down_svg(self):

        # css请求返回的text
        self.css_content = requests.get(self.css_url, headers=self.headers).text
        # 使用正则取出
        svg_list = re.findall(r"background-image: url\((.+?)\);", self.css_content)
        svg_url = ["https:{}".format(svg) for svg in svg_list]

        # 下载最大的svg文件
        length_d_l = list()
        [length_d_l.append({"len": len(requests.get(svg).text), "content": requests.get(svg).text}) for svg in svg_url]
        self.svg_content = str([x["content"] for x in length_d_l if x["len"] == max([i["len"] for i in length_d_l])][0])


    
    def font_mapping(self):
    # 使用正则取出字
        font_list = re.findall(r'<text x=".*" y="(.*)">(.+?)</text>', self.svg_content)
        # 循环并将映射添加到列表中
        for num, i in enumerate(font_list):
            for x, v in enumerate(i[1]):
                self.font_d_l.append({
                    "value": v,
                    "x": x,
                    "y": (int(font_list[num - 1][0]) if font_list[num - 1][0] != '2495' else 0, int(i[0]))
                })
                
    def position_mapping(self):
        
        #位置映射
        # 使用正则取出字
        
        all_ = re.findall("\.(.+?){background:-(.+?)\.0px -(.+?)\.0px;}", self.css_content)
        [self.position_l.append({
            "class": i[0],
            "x": i[1],
            "y": i[2],
        }) for i in all_]
        
    def all_font_position(self):
        """
        所有字体位置
        :return:
        """
        x = etree.HTML(self.text)
        self.position_list = x.xpath('//svgmtsi/@class')
        
    def find_font(self, x, y):
        
        # 查询具体字体
        # :param x:
        # :param y:
        # :return:
        
        # 根据坐标返回对应的字体
        new_x = int(x) / 14
        for i in self.font_d_l:
            if int(i.get("x")) == int(new_x) and i.get('y')[0] < int(y) < i.get('y')[1]:
                return i.get('value')
            
        str_text = str(self.text)
        for position in self.position_list:
            for x in self.position_l:
                if x.get("class") == position:
                    str_text = str_text.replace('<svgmtsi class="{}"></svgmtsi>'.format(position),
                                                str(self.find_font(x.get('x'), x.get('y')))).replace("&#x0A;",
                                                                                                        '').replace(
                        "&#x20;", '')
                                                                                            
    def get_data(self, str_text):
        x = etree.HTML(str_text)
        # 取出所以li标签
        li = x.xpath('//div[@class="reviews-items"]/ul/li')
        print(len(li))
        for l in li:
            # 定义一个字典用来存储数据
            item = dict()
            # 口味评分
            flavor = l.xpath("./div/div/span/span[1]/text()")
            # 环境评分
            ambient = l.xpath("./div/div/span/span[2]/text()")
            # 服务评分
            service = l.xpath("./div/div/span/span[3]/text()")
            # 人均价格
            price = l.xpath("./div/div/span/span[4]/text()")
            # 发布时间
            times = l.xpath("./div[@class='main-review']/div/span[@class='time']/text()")
            # 短评论
            s_comment = l.xpath("div[@class='main-review']/div[@class='review-words']")
            # 长评论
            l_comment = l.xpath("div[@class='main-review']//div[@class='review-words Hide']")
            # 存储到字典中
            item["flavor"] = str(flavor[0]).replace('\n', '').replace(' ', '') if flavor else "暂无"
            item["ambient"] = str(ambient[0]).replace('\n', '').replace(' ', '') if ambient else "暂无"
            item["service"] = str(service[0]).replace('\n', '').replace(' ', '') if service else "暂无"
            item["price"] = str(price[0]).replace('\n', '').replace(' ', '') if price else "暂无"
            item["time"] = str(times[0]).replace('\n', '').replace(' ', '') if times else "暂无"
            # 判断此条评论为长评还是短评 然后存储到字典
            if l_comment:
                l_str = html.unescape((etree.tostring(l_comment[0]).decode()))
                l_com = re.findall('<div class="review-words Hide">(.+?)<div class="less-words">', l_str,
                                    re.DOTALL)[0]
                item["comment"] = l_com.replace('\n', '').replace(' ', '').replace('\t', '')
            elif s_comment:
                s_str = html.unescape((etree.tostring(s_comment[0]).decode()))
                s_com = re.findall('<div class="review-words">(.+?)</div>', s_str, re.DOTALL)[0]
                item["comment"] = s_com.replace('\n', '').replace(' ', '').replace('\t', '')
            else:
                item["comment"] = "该用户没有填写评论..."
            # 类中的列表 来存储保存后的字典
            self.data.append(item)          
    def save(self):
        """
        保存数据为csv文件
        :return:
        """
        pandas.DataFrame(self.data,
                    columns=["flavor", "ambient", "service", "price", "time", "comment"]).to_csv(
            'data.csv')
    '''                        
    def run(self):
        print("开始爬取")
        # self.url = url
        # 获取css
        # self.down_css()
        # 获取字体文件
        """ self.down_svg()
        # 添加字体映射
        self.font_mapping()
        # 添加位置映射
        self.position_mapping()
        # 获取所有加密字体位置
        self.all_font_position()
        # 查询对应字体 并替换
        str_text = str(self.text)
        for position in self.position_list:
            for x in self.position_l:
                if x.get("class") == position:
                    str_text = str_text.replace('<svgmtsi class="{}"></svgmtsi>'.format(position),str(self.find_font(x.get('x'),x.get('y')))).replace("&#x0A;",'').replace("&#x20;", '')
        # 获取数据
        self.get_data(str_text)
        # 保存文件
        self.save() """
        # 控制台打印数据
        # print(self.data)
        # with open("xx.html", "w")as f:
        #     f.write(self.text)
        # with open('xx.css', "w") as f:
        #     f.write(self.css_content)
        # with open("font.svg", "w") as f:   
        #     f.write(self.svg_content)                                                                                                             
def main():
# 创建爬虫对象
    down_spider = DownComment()
    # # 爬取5页数据
    down_spider.run('http://www.dianping.com/shop/H33O0wFvNMXGFlH8/review_all')
    
    # for i in range(1, 2):
    #     print('-----------当前为{}页---------------'.format(i))
    #     url = "http://www.dianping.com/shop/H33O0wFvNMXGFlH8/review_all/p{}".format(i)
    #     down_spider.run(url=url)
        