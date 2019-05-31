# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class ScrapyHorriblesubsPipeline(object):
    items = {}

    def process_item(self, item, spider):
        self.items = {**self.items, **item}
        return item

    def close_spider(self, spider):
        if self.items is not None:
            if "title"in self.items:
                file_name = self.items['title'] + ".json"
                del(self.items['title'])
            else:
                file_name = "magnets.json"
            with open(file_name, "w") as f:
                f.write(json.dumps(self.items, sort_keys=True, indent=4))
