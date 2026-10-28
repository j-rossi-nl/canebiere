# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from utils.articles import write_articles


class WriteItemPipeline(object):
    """Accumule les académies et les range dans data/articles/<saison>.jsonl à la fin du crawl."""

    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        if not self.items:
            spider.logger.info('Aucune nouvelle académie')
            return
        for path in write_articles(self.items):
            spider.logger.info(f'Écrit: {path}')
        spider.logger.info(f'{len(self.items)} nouvelle(s) académie(s)')

    def process_item(self, item, spider):
        spider.logger.info(f"Nouvelle académie: {item['date']} {item['title']}")
        self.items.append(dict(item))
        return item
