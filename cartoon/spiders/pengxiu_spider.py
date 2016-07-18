#encoding:utf-8
from scrapy import Spider
from scrapy.selector import Selector
import scrapy
from cartoon.items import CartoonItem
import json
import re
import time
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class PengxiuSpider(Spider):
    name = "pengxiu"
    start_urls = [
        "http://www.pengxiu.com/look/876448/",
        "http://www.pengxiu.com/look/876408/",
        "http://www.pengxiu.com/look/876483/",
        "http://www.pengxiu.com/look/876367/",
        "http://www.pengxiu.com/look/877139/",
        "http://www.pengxiu.com/look/879269/",
    ]

    def parse(self, response):
        '''
        cmd = 'phantomjs constructDom.js "%s"' % response.url
        stdout,stderr = subprocess.Popen(cmd,shell= True,stdout = subprocess.PIPE,stderr = subprocess.PIPE).communicate()
        f = file('code.txt', 'w+')
        f.writelines(stdout)
        #print (stdout)
        sel = Selector(text=stdout)
        '''
        sel = Selector(response)
        item = CartoonItem()
        item['name'] = "".join(sel.css('div.weizhi::text').re(u'>>(.*)')).strip()
        item['url'] = response.url
        item['likeNum'] = -1
        item['caiNum'] = -1
        item['webName'] = "捧秀漫画"
        kid = response.url.split('/')
        commentApiUrl = "http://www.pengxiu.com/comment.do?doing=comment_web_ajaxlook2&kind=book&kid=" + kid[4]
        request = scrapy.Request(commentApiUrl, callback = self.moreparse)
        request.meta['item'] = item
        request.meta['kid'] = kid[4]
        return request

    def moreparse(self, response):
        item = response.meta['item']
        kid = response.meta['kid']
        data = json.loads(response.body_as_unicode())
        #if data['result'] == 1:
        item['commentNum'] = data['page']['result_count']
        infoApiUrl = "http://www.pengxiu.com/member.do?doing=member_web_getnumcallback&modelid=" + kid
        request = scrapy.Request(infoApiUrl, callback = self.endparse)
        request.meta['item'] = item
        return request

    def endparse(self, response):
        item = response.meta['item']
        data = json.loads(response.body_as_unicode())
        item['hitNum'] = data['allclick']
        item['collectionNum'] = data['shoucangshu']
        item['crawlTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return item