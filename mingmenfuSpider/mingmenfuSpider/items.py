# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MingmenfuspiderItem(scrapy.Item):
    check_num = scrapy.Field()    # 核验编码
    house_num = scrapy.Field()    # 我爱我家/贝壳 编码
    price = scrapy.Field()    # 价格
    unit_price = scrapy.Field()    # 单价
    floor = scrapy.Field()    # 楼层位置
    area = scrapy.Field()    # 面积
    date = scrapy.Field()    # 日期