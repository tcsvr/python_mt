# coding:utf-8
import re
content = '因经常牙龈出血，就团了这个洗牙套餐，因为有牙周上药，是进口的药，电话咨询才知道，个流程很仔细，牙上的结石在漱口的时候全掉下来了。洗完后真舒服。'
count = content.replace('电','44')  # 评论
count = count.replace('44','66')  # 评论

# count = re.sub("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9^，。]", "", content)
# count = re.sub("([^，。\u4e00-\u9fa5\u0030-\u0039]|[电咨])", "", content)
print(count)