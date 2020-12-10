import datetime

import scrapy
from utils.tool import get_community_name

class Hz5i5jSpider(scrapy.Spider):
    name = 'hz5i5j'
    allowed_domains = ['5i5j.com']
    start_urls = [
        'https://hz.5i5j.com/xq-ershoufang/100000000039911/',    # 名门府
        'https://hz.5i5j.com/xq-ershoufang/100000000000680/',    # 华瑞晴庐
        'https://hz.5i5j.com/xq-ershoufang/100000000001941/',    # 微风之城
        # 'https://hz.5i5j.com/xq-ershoufang/100000000044155/',    # 望海潮
        # 'https://hz.5i5j.com/xq-ershoufang/100000000044713/'    # 璟隽名邸

    ]
    info_url = 'https://hz.5i5j.com'
    encoding = 'utf-8'

    def parse(self, response):
        selectors = response.xpath('//ul[@class="pList"]')[0].xpath('./li')
        for selector in selectors:
            try:
                href = selector.xpath('./div[2]/div[1]/p[2]/a[2]/@href').get().split('#')[0]
                print(href)
                yield scrapy.Request(self.info_url + href, callback=self.parse_info)
            except Exception as e:
                print(e)

        # 下一页
        hrefs = response.xpath('//div[@class="pageSty rf"]/a')
        for href in hrefs:
            try:
                if '下' in href.get():
                    href = response.urljoin(href.xpath('./@href').get())
                    print(href)
                    yield scrapy.Request(href, callback=self.parse)
                    break
            except Exception as e:
                print(e)

    def parse_info(self, response):
        item = {}
        try:
            item['source'] = '5i5j'
            data = response.xpath('//div[@class="main container"]')
            community_str = data.xpath('string(.//div[@class="zushous"]/ul[1]/li[1])').get()
            item['community_name'] = get_community_name(community_str)
            number_info_str = data.xpath('string(.//span[@class="del-houseid"])').get()
            item['house_num'] = number_info_str.split('|')[0].split('：')[1].strip()
            if '核验编码' in number_info_str:
                item['check_num'] = number_info_str.split('|')[1].split('：')[1].strip()
            else:
                item['check_num'] = '-'
            item['price'] = data.xpath('string(.//div[@class="de-price fl"])').get().replace('万', '').strip()
            item['unit_price'] = data.xpath('string(.//div[@class="danjia"]/span)').get().strip()
            item['floor'] = data.xpath('string(.//div[@class="jlyoubai fl jlyoubai1"]/p[@class="houseinfor2"])').get().split('/')[0].strip()
            item['area'] = data.xpath('string(.//div[@class="jlyoubai fl jlyoubai2"]/p[@class="houseinfor1"])').get().replace('m²', '').strip()
            item['publish_time'] = data.xpath('string(.//div[@class="saleinfo"]//div[@class="clear jysx"]//ul[1]//li[1]/span)').get().strip()

            infos = data.xpath('.//div[@class="tag-nowts"]//ul[1]/li')
            for info in infos:
                info = info.get()
                if '税费' in info:
                    if '未满两年' in info or '未满二年' in info:
                        item['status'] = '未满两年'
                    elif '未满五年' in info:
                        item['status'] = '未满五年'
                    elif '已满五年' in info:
                        item['status'] = '已满五年'
                    elif '已满两年' in info or '已满二年' in info:
                        item['status'] = '已满两年'
                    break

            item['date'] = datetime.date.today()
        except Exception as e:
            print(e)

        yield item
