import requests
import parsel
import csv


f =open('1.csv', 'w', newline='')

csv_writer = csv.DictWriter(f, fieldnames=[
        '店名',
        '评论',
        '人均消费',
        '口味',
        '环境',
        '服务',
        '地址',
        '电话',
        '详情页',
])
csv_writer.writeheader()
url = 'https://www.meituan.com/yiliao/6258501/'
headers = {

    'Host': 'www.meituan.com',
    'Referer': 'https://sz.meituan.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    "Cookie": '__mta=150895241.1659079262267.1659079262267.1659079262267.1; uuid=03d87f230f4d491aa397.1659079192.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=18248d36ed63-02185ce523eb69-3b3d5203-1fa400-18248d36ed8c8; webloc_geo=22.538428%2C114.118368%2Cwgs84; ci=30; qruuid=cf5b152e-76e6-46a8-b762-59794efd4395; token2=hH4Rhv98I7Lu5fdoMVwnNB-yhSAAAAAAEBMAACeOR9Zuit95eGQkwTkOg2ckkQFe5-CIfrhs7bmNvhXw0g4TkcfNdHBkk9MTq2Iciw; oops=hH4Rhv98I7Lu5fdoMVwnNB-yhSAAAAAAEBMAACeOR9Zuit95eGQkwTkOg2ckkQFe5-CIfrhs7bmNvhXw0g4TkcfNdHBkk9MTq2Iciw; lt=hH4Rhv98I7Lu5fdoMVwnNB-yhSAAAAAAEBMAACeOR9Zuit95eGQkwTkOg2ckkQFe5-CIfrhs7bmNvhXw0g4TkcfNdHBkk9MTq2Iciw; u=2298740210; n=3%E8%AA%90844; unc=3%E8%AA%90844; firstTime=1659079258884; _lxsdk_s=18248d36ed9-09e-840-026%7C%7C9'

}

response = requests.get(url=url, headers=headers)
selector = parsel.Selector(response.text)
href = selector.css('.shop-list ul li .pic a::attr(href)').getall()
print(href)
for index in href:
    html_data = requests.get(url=index, headers=headers).text
    selector_1 = parsel.Selector(html_data)
    title = selector_1.css('.shop-name::text').get()  # 店名
    count = selector_1.css('#reviewCount::text').get()  # 评论
    Price = selector_1.css('#avgPriceTitle::text').get()  # 人均消费
    item_list = selector_1.css('#comment_score .item::text').getall()  # 评价
    taste = item_list[0].split(': ')[-1]  # 口味评分
    environment = item_list[1].split(': ')[-1]  # 环境评分
    service = item_list[-1].split(': ')[-1]  # 服务评分
    address = selector_1.css('#address::text').get()  # 地址
    tel = selector_1.css('.tel ::text').getall()[-1]  # 电话
    dit = {
        '店名': title,
        '评论': count,
        '人均消费': Price,
        '口味': taste,
        '环境': environment,
        '服务': service,
        '地址': address,
        '电话': tel,
        '详情页': index,
    }
    csv_writer.writerow(dit)
    print(dit)