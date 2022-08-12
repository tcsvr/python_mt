import requests
import parsel
import csv
import re
from lxml import etree
from scrapy import Selector
import json
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="is_shenzhen90_com"
)

mycursor = mydb.cursor()



# mycursor.execute("CREATE TABLE ba_review_system (id int auto_increment primary key,comments text(0),picurls text(0),status int(1),platform varchar(120),editor int(1))") # 创建表

# sql = "insert into ba_review_system (comments, platform) values ('评论测试','博爱测试')"# 插入数据
# mycursor.execute(sql)
#或者写成:
#sql = "insert into biao1 (id,name,passwd) values (%s,%s,%s)"
#val = ('1','admin','admin')
#mycursor.execute(sql,val)



sql = "SELECT * FROM ba_review_system WHERE comments like '%带保持器阶%' "# 查询数据
mycursor.execute(sql)
myresult = mycursor.fetchall()
if myresult:
    print("已存在")
    print(myresult)
else:
    print("不存在")
#     sql = "insert into ba_review_system (comments, platform) values ('评论测试!','博爱测试')"
#     mycursor.execute(sql)
#     print(mycursor.rowcount, "record(s) affected")


# mycursor.execute("DELETE FROM ba_review_system WHERE comments = ''")# 删除数据
# mydb.commit()
# print(mycursor.rowcount, "record(s) affected")


# mycursor.execute("UPDATE ba_review_system SET status=0 ")# 更新数据
# mydb.commit()#要有
# print(mycursor.rowcount, "record(s) affected")

  
    
mydb.commit()

# print(mycursor.rowcount, "record inserted.")


# mycursor.execute("SHOW TABLES")

# for x in mycursor:
#   print(x)
# f =open('5.csv', 'w', newline='')

# csv_writer = csv.DictWriter(f, fieldnames=[
#         '评论',
#         '图片',
#         # '人均消费',
#         # '口味',
#         # '环境',
#         # '服务',
#         # '地址',
#         # '电话',
#         # '详情页',
# ])
# csv_writer.writeheader()
# for x in range(100):
#     url = 'https://www.meituan.com/ptapi/poi/getcomment?id=164671400&offset='+str(x)+'0&pageSize=10&mode=0&starRange=&userId=&sortType=1'
#     # url = 'https://i.meituan.com/general/platform/mttgdetail/mtdealcommentsgn.json?dealid=39104699&limit=10&offset='+str(x)+'0&sorttype=0&tag='
#     # print(url)
#     headers = {

#         'Host': 'www.meituan.com',
#         'Referer': 'https://www.meituan.com/jiankangliren/164671400/',
#         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
#         "Cookie": 'uuid=81307fee033648d7ac6c.1659496378.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=18261b12718c8-021c6ac6508cb-3b3d5203-1fa400-18261b12719c8; ci=30; mtcdn=K; client-id=7940752b-d92b-48e5-9761-4e3186d753c9; qruuid=7481365a-e0d8-4578-a937-c696e08bb7bc; token2=GCW8DV9xDfaFUtJOsf-y8WxtcSsAAAAAEBMAAG-zkdh6hQ4fmHIJlweOthjXKIUVp4i71MKd_UZw3pEzW9EwAQyV7UJkw72f8eNJTw; oops=GCW8DV9xDfaFUtJOsf-y8WxtcSsAAAAAEBMAAG-zkdh6hQ4fmHIJlweOthjXKIUVp4i71MKd_UZw3pEzW9EwAQyV7UJkw72f8eNJTw; lt=GCW8DV9xDfaFUtJOsf-y8WxtcSsAAAAAEBMAAG-zkdh6hQ4fmHIJlweOthjXKIUVp4i71MKd_UZw3pEzW9EwAQyV7UJkw72f8eNJTw; u=2298740210; n=3%E8%AA%90844; unc=3%E8%AA%90844; firstTime=1659496749157; _lxsdk_s=18261b1271a-020-ec4-fbe%7C%7C70'

#     }

#     response = requests.get(url, headers=headers)
#     selector = parsel.Selector(response.text)

#     # title = selector.css('.seller-name::text').get()  # 店名
#     count = selector.css('p::text').extract()
#     # print(count)
#     # res = re.sub("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]", "", count[0])
#     j = json.loads(count[0])
#     # print(type(j['comments'][0]))

#     con = (j['comments'])

#     for i in con:
#         # count = i['comment'].replace('\U0001f44d', '')  # 评论
#         count = re.sub("[^，。\\u4e00-\\u9fa5^a-z^A-Z^0-9^%&',.;=?$\x22]", "", i['comment'])   # 评论
#         print(i['comment'])
#         picUrls = i['picUrls']  # 评论
#     #     Price = count[i]['comment'] # 人均消费
#     #     item_list = selector_1.css('#comment_score .item::text').getall()  # 评价
#     #     taste = item_list[0].split(': ')[-1]  # 口味评分
#     #     environment = item_list[1].split(': ')[-1]  # 环境评分
#     #     service = item_list[-1].split(': ')[-1]  # 服务评分
#     #     address = selector_1.css('#address::text').get()  # 地址
#     #     tel = selector_1.css('.tel ::text').getall()[-1]  # 电话
