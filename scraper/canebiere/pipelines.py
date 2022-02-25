# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

from scrapy.exporters import JsonLinesItemExporter


class WriteItemPipeline(object):

    def __init__(self):
        self.filename = f"canebiere-{datetime.now().strftime('%Y%m%d%H%M')}.jsonl"

    def open_spider(self, spider):
        self.jsonfile = open(self.filename, 'wb')
        self.exporter = JsonLinesItemExporter(self.jsonfile)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.jsonfile.close()

    def process_item(self, item, spider):
        print('Process: {}'.format(item))
        self.exporter.export_item(item)
        return item
