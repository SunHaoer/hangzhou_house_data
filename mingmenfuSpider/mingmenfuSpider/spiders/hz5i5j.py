import datetime

import scrapy

class Hz5i5jSpider(scrapy.Spider):
    name = 'hz5i5j'
    allowed_domains = ['5i5j.com']
    start_urls = ['https://hz.5i5j.com/xq-ershoufang/100000000039911/']
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

    def parse_info(self, response):
        item = {}
        try:
            item['community_name'] = '名门府'
            data = response.xpath('//div[@class="main container"]')
            number_info_str = data.xpath('string(//span[@class="del-houseid"])').get()
            item['house_num'] = number_info_str.split('|')[0].split('：')[1].strip()
            if '核验编码' in number_info_str:
                item['check_num'] = number_info_str.split('|')[1].split('：')[1].strip()
            else:
                item['check_num'] = '-'
            item['source'] = '5i5j'
            item['price'] = data.xpath('string(//div[@class="de-price fl"])').get().replace('万', '').strip()
            item['unit_price'] = data.xpath('string(//div[@class="danjia"]/span)').get().strip()
            item['floor'] = data.xpath('string(//div[@class="jlyoubai fl jlyoubai1"]/p[@class="houseinfor2"])').get().split('/')[0].strip()
            item['area'] = data.xpath('string(//div[@class="jlyoubai fl jlyoubai2"]/p[@class="houseinfor1"])').get().replace('m²', '').strip()
            item['date'] = datetime.date.today()
        except Exception as e:
            print(e)

        yield item
