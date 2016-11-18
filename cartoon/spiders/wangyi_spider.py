#encoding:utf-8
from scrapy import Spider
from scrapy.selector import Selector
import scrapy
from cartoon.items import CartoonItem
import re
import subprocess
import json
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class WangyiSpider(Spider):
    name = "wangyi"
    start_urls = [
        "http://manhua.163.com/source/4529535265780105579",
        "http://manhua.163.com/source/4530855668140093100",
        "http://manhua.163.com/source/4530855668140092184",
        "http://manhua.163.com/source/4530855668140091759",
        "http://manhua.163.com/source/4545825141360102576",
        "http://manhua.163.com/source/4639712296520119584",
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
        csrfToken = sel.css("input#j-csrf::attr(value)").extract()[0].strip()
        name = "".join(sel.css('h1.m-source-title::text').extract()).strip()
        bookId = response.url.split("/")[-1]
        item = CartoonItem()
        item['name'] = "".join(sel.css('h1.m-source-title::text').extract()).strip()
        item['url'] = response.url
        item['hitNum'] = "".join(sel.css('div.g-cols--float>div.g-col:nth-of-type(1)>div.metadata:nth-of-type(2)::text').re(u'人气\：(.*)')).strip()
        searchObj = re.search(u'(.*)万', item['hitNum'])
        if searchObj:
            item['hitNum'] = int(float(searchObj.group(1)) * 10000)
        else:
            item['hitNum'] = int(item['hitNum'])
        item['collectionNum'] = -1
        item['likeNum'] = -1
        item['caiNum'] = -1
        item['webName'] = "网易漫画"
        item['crawlTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        commentApiUrl = "http://manhua.163.com/comment/"+bookId+"/comments?csrfToken="+csrfToken+"&bookId="+bookId+"&page=1"
        request = scrapy.Request(commentApiUrl, callback = self.moreparse)
        request.meta['item'] = item
        return request
    def moreparse(self, response):
        item = response.meta['item']
        data = json.loads(response.body_as_unicode())
        item['commentNum'] = data['commentCount']
        return item