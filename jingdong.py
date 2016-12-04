#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-11-27 03:03:45
# Project: jingdonghui1

from pyspider.libs.base_handler import *
import re, random


class Handler(BaseHandler):
    crawl_config = {


        'headers': {
            'Accept': 'text/css,*/*;q=0.1',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'DNT':'1',
            'Host':'static.360buyimg.com',
            'If-Modified-Since':'Thu, 24 Nov 2016 19:06:40 GMT',
            'Referer':'http://item.jd.com/10253639028.html',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        }
    }

    def __init__(self):
        self.base_url = 'https://list.jd.com/list.html?cat=1315,1345,1364&page='
        self.page_num = 1
        self.total_num = 20
        self.comment = '#comment'
        self.comment_api = 'https://sclub.jd.com/comment/productPageComments.action?productId={0}&score=0&sortType=3&page={1}&pageSize=20&callback=fetchJSON_comment98vv35654'

    @every(minutes=24 * 60)
    def on_start(self):
        urlList = []
        while self.page_num <= self.total_num:
            url = self.base_url + str(self.page_num)
            # print url
            self.crawl(url, callback=self.index_page)
            self.page_num += 1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        urlList = []
        for each in response.doc('a[href^="https://item"]').items():
            # each = each.attr.href + self.comment
            # print each.attr.href
            ss = re.findall(r'\d+', each.attr.href)
            # print ss
            page = 5
            for i in range(page):
                urll = self.comment_api.format(ss[0], i)
                #print
                urlList.append(urll)
        for urlindex in random.sample(range(len(urlList)),len(urlList)):

            self.crawl(urlList[urlindex], callback=self.detail_page, fetch_type='js', auto_recrawl=True)

    @config(priority=2)
    def detail_page(self, response):
        # print response

        text = response.doc('body').text()
        text = text.replace('javascript:void(0);', '')
        data = re.findall('fetchJSON_comment98vv35654\((.*?)\}\);', text)
        res = {}
        if data:
            try:
                data = data[0] + '}'

                data = data.replace(' ', '')
                data = data.replace('":null', '":"null"')
                data = data.replace('":false', '":"false"')
                data = data.replace('":true', '":"true"')
                data = eval(data)
                for i in range(len(data['comments'])):
                    res.setdefault(i, {})
                    res[i] = data['comments'][i]['productSize'], \
                             data['comments'][i]['productColor'], \
                             data['comments'][i]['content'], \
                             data['comments'][i]['score'], \
                             data['comments'][i]['creationTime'], \
                             data['comments'][i]['referenceTime'], \
                             data['comments'][i]['userClientShow'], \
                             data['comments'][i]['userLevelName'], \
                             data['comments'][i]['userProvince'],

                referenceName = data['comments'][0]['referenceName']
                return {
                    referenceName: res,

                }
            except Exception as e:
                print
                '发生错误{}'.format(e)
                exit()
        else:
            return {}

