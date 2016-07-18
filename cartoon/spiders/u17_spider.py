#encoding:utf-8
from scrapy import Spider
from scrapy.selector import Selector

from cartoon.items import CartoonItem
import re
import subprocess
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class UyqSpider(Spider):
    name = "u17"
    start_urls = [
        "http://www.u17.com/comic/113468.html",
        "http://www.u17.com/comic/113472.html",
        "http://www.u17.com/comic/113473.html",
        "http://www.u17.com/comic/114661.html",
        "http://www.u17.com/comic/125731.html",
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
        item['name'] = "".join(sel.css('h1.fl::text').extract()).strip()
        item['url'] = response.url
        item['hitNum'] = "".join(sel.css('div.line1>i::text').extract()).strip()
        searchObj = re.search(u'(.*)万', item['hitNum'])
        if searchObj:
            item['hitNum'] = int(float(searchObj.group(1)) * 10000)
        else:
            item['hitNum'] = int(item['hitNum'])
        item['collectionNum'] = int("".join(sel.css('a.btn_stored span i::text').extract()).strip())
        item['commentNum'] = -1 #int("".join(sel.css('i.panel_comment_total::text').extract()).strip()) #threadId得不到，抓不到
        item['likeNum'] = -1
        item['caiNum'] = -1
        item['webName'] = "有妖气"
        item['crawlTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return item