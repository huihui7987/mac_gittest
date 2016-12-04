#-*- coding:utf-8 -*-

# filename = '/Users/huihui/PycharmProjects/mac_gittest/json_comment.txt'
# with open(filename) as f:
#     lines = f.readlines()
# for line in lines:
#     print(line)

from bs4 import BeautifulSoup
import requests,lxml,re

url = 'https://sclub.jd.com/comment/productPageComments.action?productId=1470656924&score=0&sortType=3&page=3&pageSize=10&callback=fetchJSON_comment98vv157'
urlnew = 'http://club.jd.com/review/{0}-1-2-0.html'.format(productId)
def comment():
    """评论
    """
    #url = 'https://sclub.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=3&' \
    #      'page={}&pageSize=10&callback=fetchJSON_comment98vv157'.format(product_id, page)
    text = requests.get(url).text
    text = text.replace('javascript:void(0);', '')
    data = re.findall('fetchJSON_comment98vv157\((.*?)\}\);', text)
    res = []
    Resjson = {}
    if data:
        try:
            data = data[0] + '}'

            data = data.replace(' ', '')
            data = data.replace('":null', '":"null"')
            data = data.replace('":false', '":"false"')
            data = data.replace('":true', '":"true"')
            data = eval(data)
            #Resjson.setdefault('name',{})
            for i in range(len(data['comments'])):
                Resjson.setdefault(i,{})
                Resjson[i] = data['comments'][i]['productSize'],\
                             data['comments'][i]['productColor'],\
                             data['comments'][i]['content'],\
                             data['comments'][i]['score'],\
                             data['comments'][i]['creationTime'],\
                             data['comments'][i]['referenceTime'],\
                             data['comments'][i]['userClientShow'],\
                             data['comments'][i]['userLevelName'],\
                             data['comments'][i]['userProvince'],

                #Resjson.setdefault(i, data['comments'][i]['content'])
            referenceName0 = data['comments'][0]['referenceName']
            return {referenceName0:Resjson}

        except Exception as e:
            print('发生错误{}'.format(e))
            exit()
    else:
        return {}



data = comment()

print(data)

