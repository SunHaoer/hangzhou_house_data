# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime

import pymysql as pymysql

class MingmenfuspiderPipeline:

    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()


    def process_item(self, item, spider):
        item = self.init_item(item)

        try:
            sql = f'''
                            insert ignore into `house_info`(
                            `community_name`,
                            `check_num`,
                            `house_num`,
                            `source`,
                            `price`,
                            `unit_price`,
                            `floor`,
                            `area`,
                            `status`,
                            `publish_time`,
                            `date`
                            )
                            values ('%s','%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s')
                    ''' % tuple((item['community_name'], item['check_num'], item['house_num'], item['source'],
                                 item['price'], item['unit_price'], item['floor'], item['area'], item['status'], item['publish_time'], item['date']))

            self.cursor.execute(sql)
            self.db.commit()
            # logging.info(self.spider.name + ": " + "insert into mysql success")
        except Exception as e:
            print(e)

        return item

    def init_item(self, item):
        item.setdefault('community_name', '名门府')
        item.setdefault('check_num', '-')
        item.setdefault('house_num', '-')
        item.setdefault('source', '0')
        item.setdefault('price', '0')
        item.setdefault('unit_price', '0')
        item.setdefault('floor', '-')
        item.setdefault('area', '0')
        item.setdefault('status', '-')
        item.setdefault('publish_time', datetime.date.today())
        item.setdefault('date', datetime.date.today())
        return item
