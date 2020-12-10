import datetime
import re

import scrapy
from utils.tool import get_community_name

class HzkeSpider(scrapy.Spider):
    name = 'hzke'
    allowed_domains = ['ke.com']
    start_urls = [
        'https://hz.ke.com/ershoufang/c1820027546685962/',    # 名门府
        # 'https://hz.ke.com/ershoufang/c188390937162697/',    # 春江悦茗
        'https://hz.ke.com/ershoufang/c187308876459783/',    # 华瑞晴庐
        'https://hz.ke.com/ershoufang/c1820028731118580/'    # 微风之城
    ]

    def parse(self, response):
        selectors = response.xpath('//a[@class="VIEWDATA CLICKDATA maidian-detail"]')
        for selector in selectors:
            try:
                href = selector.xpath('./@href').get()
                print(href)
                yield scrapy.Request(href, callback=self.parse_info)
            except Exception as e:
                print(e)
        hrefs = response.xpath('//div[@class="pagination_group_a"]/a/@href')

        # 下一页
        if self.start_urls.__contains__(response.url):
            for href in hrefs:
                try:
                    href = response.urljoin(href.get())
                    print(href)
                    if href.endswith('/') == False:
                        href = href + '/'
                    if self.start_urls.__contains__(href) == False:
                        yield scrapy.Request(href, callback=self.parse)
                except Exception as e:
                    print(e)


    def parse_info(self, response):
        item = {}
        try:
            item['source'] = 'beike'
            community_str = response.xpath('//div[@class="intro clear"]').get()
            item['community_name'] = get_community_name(community_str)
            item['house_num'] = response.xpath('string(//div[@class="houseRecord"]/span[@class="info"])').get().split('\n')[0].strip()

            price_data = response.xpath('//div[@data-component="overviewIntro"]//div[@class="content"]/div[2]')
            item['price'] = price_data.xpath('string(./span[@class="total"])').get().strip()
            item['unit_price'] = round(
                int(price_data.xpath('string(.//span[@class="unitPriceValue"])').get().strip()) / 10000, 2)

            info_data = response.xpath('//div[@id="introduction"]')
            infos1 = info_data.xpath('.//div[@class="content"]')[0].xpath('.//li')
            for info in infos1:
                info = info.get()
                if '楼层' in info:
                    if '高' in info:
                        item['floor'] = '高楼层'
                    elif '中' in info:
                        item['floor'] = '中楼层'
                    elif '低' in info:
                        item['floor'] = '低楼层'
                if '建筑面积' in info:
                    item['area'] = self.get_info(info).replace('㎡', '')

            infos2 = info_data.xpath('.//div[@class="content"]')[1].xpath('.//li')
            for info in infos2:
                info = info.get()
                if '挂牌' in info:
                    item['publish_time'] = self.get_info(info).replace('年', '-').replace('月', '-').replace('日', '')
                if '年限' in info:
                    item['status'] = self.get_info(info)
                if '核验' in info:
                    item['check_num'] = self.get_info(info)
            item['date'] = datetime.date.today()
        except Exception as e:
            print(e)

        yield item

    def get_info(self, info):
        info = re.findall(r'</span>(.+?)[\n|</li>|<div>]', info)[0].strip()
        return info