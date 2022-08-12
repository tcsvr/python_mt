import requests
from lxml import etree
from selenium import webdriver
import time
import numpy
import re
from fontTools.ttLib import TTFont  # 解析字体文件的包
from PIL import Image, ImageDraw, ImageFont  #绘制图片
from selenium.webdriver.chrome.options import Options
from aip import AipOcr
import os


url='http://www.dianping.com/shop/G7RgscHLjDjXY9hg'
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
wb=webdriver.Chrome(options=options)
wb.get(url)
re_text=wb.page_source

#数据读取并保存
dz=DZDP_HTML(re_text=re_text)
dc=dz.dict_dict#传入总字典
tree=etree.HTML(re_text)
data=get_datas_by_xpath(tree,dc)
json_str = json.dumps(data,indent=4,ensure_ascii=False)
with open('cs.json','w',encoding='utf-8') as f:
    f.write(json_str)
    
def get_fonts_css(re_text):
    # 传入selenium得到的网页内容 通过正则提取到各个字体对应的url链接
        css_gz=re.compile(r'(s3plus.meituan.net.*?.\.css)',re.S)
        css_url="http://"+css_gz.search(re_text).group(1)
        req=requests.get(url=css_url).text
        # return req.text

        url_gz=re.compile(r',url\("\/\/(s3plus.meituan.net.*?\.woff)',re.S)
        font_gz=re.compile('font-family: "PingFangSC-Regular-(.*?)";',re.S)
        url_list=re.findall(url_gz,req)
        font_list=re.findall(font_gz,req)
        font_url_dict={}
        for x,y in zip(url_list,font_list):
            font_url_dict[y]=x
        return font_url_dict#得到类型名:网址 的字典 件   
    
def down_fonts_url(font_url_dict):
    # 传入get_fonts_css得到的 字典 遍历后进行下载对应的woff文件
    for key,url in font_url_dict.items():
            url="http://"+url
            res=requests.get(url).content
            with open(key+".woff",'wb') as f:
                 print(key+".woff文件下载完成!")
                 f.write(res)


class DZDP_HTML(object):
    def __init__(self,re_text):
        super().__init__()
        dict=self.__get_fonts_css(re_text)
        self.__down_fonts_url(dict)

        self.num_dict=       self.__get_fonts_dict("num")
        self.dishname_dict=  self.__get_fonts_dict("dishname")
        self.review_dict=    self.__get_fonts_dict("review")
        self.hours_dict=     self.__get_fonts_dict("hours")
        self.address_dict=   self.__get_fonts_dict("address")
        self.shopdesc_dict=  self.__get_fonts_dict("shopdesc") 
        self.dict_dict={
            "num":self.num_dict,
            "dishname":self.dishname_dict,
            "review":self.review_dict,
            "hours":self.hours_dict,
            "address":self.address_dict,
            "shopdesc":self.shopdesc_dict
        }
      
    def __get_fonts_ocr(self,filename):
        APP_ID = ' '
        API_KEY = ' '
        SECRET_KEY = ' '
        aipOcr=AipOcr(APP_ID, API_KEY, SECRET_KEY)
        # 读取图片
        filePath = filename+".jpg"
        def get_file_content(filePath):
            with open(filePath, 'rb') as fp:
                return fp.read()
        # 定义参数变量
        optionss = {
            'detect_direction': 'true',
            'language_type': 'CHN_ENG',
        }
        # 网络图片文字文字识别接口
        result = aipOcr.webImage(get_file_content(filePath),optionss)
        return result

    def __get_fonts_dict(self,fontpath):

        font = TTFont(fontpath+'.woff')  # 打开文件
        codeList = font.getGlyphOrder()[2:]
        im = Image.new("RGB", (1800, 1000), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(fontpath+'.woff', 40)
        count = 15
        arrayList = numpy.array_split(codeList,count)   #将列表切分成15份，以便于在图片上分行显示

        for t in range(count):
            newList = [i.replace("uni", "\\u") for i in arrayList[t]]
            text = "".join(newList)
            text = text.encode('utf-8').decode('unicode_escape')
            dr.text((0, 50 * t), text, font=font, fill="#000000")
        im.save(fontpath+".jpg")
     
        dc={}#输出字典
        result=self.__get_fonts_ocr(fontpath)
        words_list=result['words_result']
        for array,word in zip(arrayList,words_list):
            for arra,wor in zip(array,word["words"]):
                # arra=str(arra)
                arra=arra.replace("uni", r"\u")
                dc[arra]=wor
        return dc

class_name_list=["shopdesc","address","hours","review","shopdesc","num"]

def get_true_words(lists,dc):
      add=""
      for n in lists:
        class_num=0
        class_name=n.xpath('.//@class')
        c=0
        #去除不属于class_name_list 就可以实现跟加密文字的一一对应确定用哪个字典解密
        while c<len( class_name):
            if  class_name[c] not in class_name_list:
                class_name.remove( class_name[c])
            else:
                c+=1    
        words=n.xpath('.//text()')
        for word in words:
            w =re.findall(u"[\ue000-\uf999]",word)#正则匹配到的说明是加密字 
            if w!=None and len(w)!=0:
                wo=word.encode('unicode_escape')
                wo=str(wo)[3:-1]
                if wo==None or wo=='' :
                    continue
                try:
                    c=class_name[class_num]
                    wo=dc[class_name[class_num]][wo]
                    add+=wo
                except BaseException:
                    print(BaseException)
                finally:
                    class_num+=1
            else:
                add+=word
      print(u'\xa0' in add)         
      add=add.replace(u'\xa0',u' ')
      return add

def get_datas_by_xpath(tree,dc):
    data={}
    #商家信息
    shop_name=tree.xpath('//h1[@class="shop-name"]')
    add=get_true_words(shop_name,dc)
    data["shop_name"]=add

    shop_address=tree.xpath('//div[@id="J_map-show"]/span[@class="item"]')
    add=get_true_words(shop_address,dc)
    data["shop_address"]=add

    shop_iphone=tree.xpath('//p[@class="expand-info tel"]')
    add=get_true_words(shop_iphone,dc)
    data["shop_iphone"]=add

    #用户信息
    li_list=tree.xpath('//ul[@class="comment-list J-list"]/li')
    i=0
    for li in li_list:
        data_user={}
        user_name=li.xpath('.//p[@class="user-info"]/a/text()')
        user_time=li.xpath('.//span[@class="time"]/text()')
        user_contont=li.xpath('.//p[@class="desc"]')
        add=get_true_words( user_contont,dc)
        data_user["user_name"]=user_name[0]
        data_user["user_time"]=user_time[0]
        data_user["user_contont"]=add
        data["user%s"%i]=data_user
        i+=1
    return data


