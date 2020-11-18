from scrapy import cmdline


name = 'hz5i5j'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())