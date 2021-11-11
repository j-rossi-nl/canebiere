import logging

from scrapy import Spider, Request
from scrapy.http import Response

from ..items import CanebiereItem
import re


class CanebiereSpider(Spider):
	name = 'canebiere_spider'
	allowed_urls = ['https://horsjeu.net/']
	root_url = 'https://horsjeu.net/category/france/lelite/la-canebiere-academie/'
	start_urls = [root_url]

	custom_settings = {
		"LOG_ENABLED": False
	}

	def parse(self, response):
		self.logger.setLevel(logging.WARN)
		# This is the default callback for the starting page
		# Parse the starting page as a result page
		yield Request(url=response.url, callback=self.parse_result_page, dont_filter=True)

	def parse_result_page(self, response):
		# This function parses the search result page
		# Link to 'Previous Page' (read all pages from last to first)
		previous = response.xpath("//div[@class='nav-previous']/a/@href").get()
		yield Request(url=previous, callback=self.parse_result_page)

		# All articles on this results pages
		articles = response.xpath("//h2[@class='entry-title']/a/@href").getall()
		for article in articles:
			yield Request(url=article, callback=self.parse_article)

	def parse_article(self, response: Response):
		article_title = response.xpath("//h1[@class='entry-title']/text()").get()
		article_body_html_xpath = response.xpath("//div[@class='mag-content']")
		article_body_html = article_body_html_xpath.get()
		article_body_text = ' '.join(article_body_html_xpath.xpath(".//text()").getall())

		article_date = response.xpath("//time[@class='entry-date published updated']/text()").get()
		article_nb_commentaires = response.xpath("//span[@class='comments-link']/a/text()").get()
		article_author = response.xpath("//a[@class='url fn n']/text()").get()

		item = CanebiereItem()
		item['title'] = article_title
		item['date'] = article_date
		try:
			item['nb_commentaires'] = int(re.match(r'(?P<nbcomments>\d+)[^0-9]+', article_nb_commentaires).group('nbcomments'))
		except AttributeError:
			item['nb_commentaires'] = -1
		item['html'] = article_body_html
		item['full_text'] = article_body_text
		item['url'] = response.url
		item['author'] = article_author
		yield item
