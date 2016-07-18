#encoding:utf-8
from scrapy import Spider
from scrapy.selector import Selector

from cartoon.items import CartoonItem
import re
import time
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SfacgSpider(Spider):
    name = "sfacg"
    start_urls = [
        "http://manhua.sfacg.com/mh/BiaoRen",
        "http://manhua.sfacg.com/mh/BLX",
        "http://manhua.sfacg.com/mh/DEE",
        "http://manhua.sfacg.com/mh/BRAVE",
        "http://manhua.sfacg.com/mh/MHSXDFH",
    ]

    def parse(self, response):
        cmd = 'phantomjs constructDom.js "%s"' % response.url
        stdout,stderr = subprocess.Popen(cmd,shell= True,stdout = subprocess.PIPE,stderr = subprocess.PIPE).communicate()
        #f = file('code.txt', 'w+')
        #f.writelines(stdout)
        #print (stdout)
        sel = Selector(text=stdout)
        #sel = Selector(response)
        item = CartoonItem()
        item['name'] = "".join(sel.css('ul.synopsises_font>li:nth-of-type(2)>span:nth-of-type(1)::text').extract()).strip()
        
        item['url'] = response.url
        item['hitNum'] = "".join(sel.css('ul.synopsises_font>li:nth-of-type(2)>span:nth-last-of-type(1)::text').extract()).strip()
        searchObj = re.search(u'(.*)万', item['hitNum'])
        if searchObj:
            item['hitNum'] = int(float(searchObj.group(1)) * 10000)
        else:
            item['hitNum'] = int(item['hitNum'])
        item['collectionNum'] = int("".join(sel.css('a#Mark2Pocket small::text').extract()).strip())
        item['commentNum'] = int(sel.css('div.wrap_left div.content_left2>span:nth-of-type(1)>span>a::text').re(u'全部(\d*)')[0])
        item['likeNum'] = int("".join(sel.css('a#DoLike small::text').extract()).strip())
        item['caiNum'] = -1
        item['webName'] = "sf互动传媒"
        item['crawlTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
        return item