import logging

from scrapy import Spider, Request
from scrapy.http import Response

from ..items import CanebiereItem
import re

from bs4.element import Tag
from bs4 import BeautifulSoup

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
		# Link to 'Next Page' (read all pages from first to last)
		previous = response.xpath("//a[@class='next page-numbers']/@href").get()  
		yield Request(url=previous, callback=self.parse_result_page)

		# All articles on this results pages
		articles = response.xpath("//h3[@class='article-title article-title-1']/a/@href").getall()
		for article in articles:
			yield Request(url=article, callback=self.parse_article)

	def parse_article(self, response):
		article_title = response.xpath("//h1[@class='entry-title']/text()").get()
		article_body_html_xpath = response.xpath("//div[@class='entry-content']")
		article_body_html = article_body_html_xpath.get()
		
		article_soup = BeautifulSoup(article_body_html)
		
		# Remove the sharing footer
		sd: Tag = article_soup.find("div", **{"class": "sharedaddy sd-sharing-enabled"})
		if sd is not None:
			sd.decompose()

		# Remove the navigation footer
		nav: Tag = article_soup.find("nav", **{"class": "navigation post-navigation"})
		if nav is not None:
			nav.decompose()

		article_body_html = str(article_soup)
		article_body_text = article_soup.get_text()

		article_author = response.xpath("//span[@class='item-metadata posts-author']/a/text()").get().strip()
		article_date = response.xpath("//meta[@property='article:published_time']/@content").get()

		item = CanebiereItem()
		item['title'] = article_title
		item['date'] = article_date
		item['html'] = article_body_html
		item['full_text'] = article_body_text
		item['url'] = response.url
		item['author'] = article_author
		yield item
