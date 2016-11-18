#encoding:utf-8
from scrapy import Spider
from scrapy.selector import Selector
import scrapy
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
        sel = Selector(response)
        threadId = re.search(u'thread_id\s*\:\s*(\d*)', response.body).group(1)
        comicId = response.url.split("/")[-1].split(".")[0]
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
        item['likeNum'] = int("".join(sel.css('i#comic_month_ticket_num::text').extract()).strip())
        item['caiNum'] = -1
        item['webName'] = "有妖气"
        item['crawlTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        commentApiUrl = "http://www.u17.com/comment/ajax.php?mod=thread&act=get_comment_php_v4&sort=create_time&thread_id=" + threadId + "&page=1&comic_id=" +comicId
        request = scrapy.Request(commentApiUrl, callback = self.moreparse)
        request.meta['item'] = item
        return request
    def moreparse(self, response):
        sel = Selector(response)
        item = response.meta['item']
        item['commentNum'] = int(re.search(u'total\"\:(\d*)',response.body).group(1))
        return item