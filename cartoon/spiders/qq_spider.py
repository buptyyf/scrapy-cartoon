#encoding:utf-8
from scrapy import Spider
from scrapy.selector import Selector
import scrapy
from cartoon.items import CartoonItem
import re
import time
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class QQSpider(Spider):
    name = "qq"
    start_urls = [
        "http://ac.qq.com/Comic/comicInfo/id/540487",
        "http://ac.qq.com/Comic/ComicInfo/id/540490",
        "http://ac.qq.com/Comic/comicInfo/id/540489",
        "http://ac.qq.com/Comic/ComicInfo/id/540488",
        "http://ac.qq.com/Comic/ComicInfo/id/540491",
        "http://ac.qq.com/Comic/ComicInfo/id/543195",
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
        item['name'] = "".join(sel.css('h2.works-intro-title strong::text').extract()).strip()
        item['url'] = response.url
        item['hitNum'] = int("".join(sel.css('p.works-intro-digi>span:nth-of-type(2)>em::text').extract()).replace(',',''))

        item['collectionNum'] = int("".join(sel.css('em#coll_count::text').extract()).replace(',',''))
        
        #item['commentNum'] = "".join(sel.css('em.commen-ft-ts::text').extract()).strip()
        item['likeNum'] = int("".join(sel.css('strong#redcount::text').extract()).strip())
        item['caiNum'] = int("".join(sel.css('ul.works-vote-list>li:nth-of-type(2)>strong::text').extract()).strip())
        item['webName'] = "腾讯漫画"
        kid = response.url.split('/')[6]
        commentUrl = "http://ac.qq.com/Community/topicList?targetId=" + kid + "&page=1"
        request = scrapy.Request(commentUrl, callback = self.moreparse)
        request.meta['item'] = item
        return request

    def moreparse(self, response):
        item = response.meta['item']
        sel = Selector(response)
        item['commentNum'] = int(sel.css('em.commen-ft-ts::text').extract()[0])
        item['crawlTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return item