from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_horriblesubs.spiders.HS import HSSpider

process = CrawlerProcess(settings=get_project_settings())
print("Enter a horriblesubs.info url")
url = input()
print("Enter file name (without extension)")
title = input()
print("\n\n\n")

# process.crawl(HSSpider, title="dororo",
#               url="https://horriblesubs.info/shows/dororo/")
process.crawl(HSSpider, title=title,
              url=url)
process.start()
