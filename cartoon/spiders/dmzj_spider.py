#encoding:utf-8
from scrapy import Spider
from scrapy.selector import Selector
import scrapy
from cartoon.items import CartoonItem
import subprocess
import re
import json
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DmzjSpider(Spider):
    name = "dmzj"
    allowed_domains = ["dmzj.com"]
    start_urls = [
        "http://www.dmzj.com/info/biaoren.html",
        "http://www.dmzj.com/info/bailangxi.html",
        "http://www.dmzj.com/info/jietan.html",
        "http://www.dmzj.com/info/brave.html",
        "http://www.dmzj.com/info/senlinrenjianshu.html",
        "http://www.dmzj.com/info/manhuashexdefuhuo.html",
    ]

    def parse(self, response):
        '''
        cmd = 'phantomjs constructDom.js "%s"' % response.url
        stdout,stderr = subprocess.Popen(cmd,shell= True,stdout = subprocess.PIPE,stderr = subprocess.PIPE).communicate()
        #f = file('code.txt', 'w+')
        #f.writelines(stdout)
        #print (stdout)
        sel = Selector(text=stdout)
        '''
        item = CartoonItem()
        item['url'] = response.url
        item['name'] = re.search(u'comic_name\s*=\s*\'(.*)\'', response.body).group(1)
        typeId = re.search(u'obj_id\s*=\s*\"(\d*)', response.body).group(1)
        infoApiUrl = "http://i.dmzj.com/ajax/ding?callback=json&typeid=" + typeId
        request = scrapy.Request(infoApiUrl, callback = self.moreparse)
        request.meta['typeId'] = typeId
        request.meta['item'] = item
        return request
        #sel = Selector(response)
        '''
        item = CartoonItem()
        item['name'] = "".join(sel.css('h1 a::text').extract()).strip()
        item['url'] = response.url
        item['hitNum'] = int("".join(sel.css('span#hits::text').extract()).strip())
        item['collectionNum'] = int("".join(sel.css('span#subscribe_amount::text').extract()).strip())
        item['commentNum'] = int("".join(sel.css('span#vote_amount::text').extract()).strip())
        item['likeNum'] = "".join(sel.css('p#top::text').extract()).strip()
        if item['likeNum'] != "":
            item['likeNum'] = int(item['likeNum'])
        else:
            item['likeNum'] = 0
        item['caiNum'] = "".join(sel.css('p#cai::text').extract()).strip()
        if item['caiNum'] != "":
            item['caiNum'] = int(item['caiNum'])
        else:
            item['caiNum'] = 0
        item['webName'] = "动漫之家"
        item['crawlTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        return item
        '''
    def moreparse(self, response):
        typeId = response.meta['typeId']
        #data = json.loads(response.body_as_unicode())
        item = response.meta['item']
        item['likeNum'] = re.search(u'ding\"\:\"*(\d*)', response.body).group(1)
        if item['likeNum'] == "":
            item['likeNum'] = 0
        else:
            item['likeNum'] = int(item['likeNum'])
        item['caiNum'] = re.search(u'cai\"\:\"*(\d*)', response.body).group(1)
        if item['caiNum'] == "":
            item['caiNum'] = 0
        else:
            item['caiNum'] = int(item['caiNum'])
        infoApiUrl = "http://www.dmzj.com/static/hits/" + typeId + ".json"
        request = scrapy.Request(infoApiUrl, callback = self.endparse)
        request.meta['item'] = item
        return request
    def endparse(self, response):
        data = json.loads(response.body_as_unicode())
        item = response.meta['item']
        item['hitNum'] = int(data['hits'])
        item['collectionNum'] =  int(data['sub_amount'])
        item['commentNum'] = int(data['vote_amount'])
        item['crawlTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        item['webName'] = "动漫之家"
        return item