import html

from urllib.parse import urlencode

from bs4 import BeautifulSoup
from scrapy import Spider, Request
from scrapy.http import Response

from utils.articles import known_urls

from ..items import CanebiereItem


class CanebiereSpider(Spider):
	"""
	Lit les académies via l'API REST WordPress de horsjeu.net, de la plus récente à la plus ancienne.
	S'arrête à la première académie déjà présente dans data/articles (sauf avec `-a full=true`).
	"""
	name = 'canebiere_spider'
	allowed_domains = ['horsjeu.net']
	api_url = 'https://horsjeu.net/wp-json/wp/v2/posts'
	category_id = 1346  # https://horsjeu.net/category/france/lelite/la-canebiere-academie/
	per_page = 50

	def __init__(self, full: str = 'false', *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.full = full.lower() in ('1', 'true', 'yes')
		self.known = set() if self.full else known_urls()

	async def start(self):
		yield self.page_request(1)

	def page_request(self, page: int) -> Request:
		params = {
			'categories': self.category_id,
			'per_page': self.per_page,
			'page': page,
			'orderby': 'date',
			'order': 'desc',
			'_embed': 'author',
			'_fields': 'date_gmt,link,title,content,_links,_embedded',
		}
		return Request(f'{self.api_url}?{urlencode(params)}', callback=self.parse_page, cb_kwargs={'page': page})

	def parse_page(self, response: Response, page: int):
		for post in response.json():
			if post['link'] in self.known:
				self.logger.info(f"Déjà connue, on s'arrête là: {post['link']}")
				return
			yield self.to_item(post)

		if page < int(response.headers.get('X-WP-TotalPages', 0)):
			yield self.page_request(page + 1)

	@staticmethod
	def to_item(post: dict) -> CanebiereItem:
		body_html = post['content']['rendered']
		authors = post.get('_embedded', {}).get('author', [])

		item = CanebiereItem()
		item['title'] = html.unescape(post['title']['rendered'])
		item['date'] = f"{post['date_gmt']}+00:00"
		item['html'] = body_html
		item['full_text'] = BeautifulSoup(body_html, 'html.parser').get_text()
		item['url'] = post['link']
		item['author'] = authors[0]['name'].strip() if authors else None
		return item
