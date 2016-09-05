from __future__ import unicode_literals
from dynamic_scraper.spiders.django_spider import DjangoSpider
from webku.models import NewsWebsite, Article
from webku.scraper.items import ArticleItem
from scrapy.http import Request

class ArticleSpider(DjangoSpider):
    
    name = 'article_spider'
    allowed_domains = ["en.wikinews.org"]
    start_urls = [
        "http://en.wikinews.org/wiki/Main_Page", (1)
    ]
    def __init__(self, *args, **kwargs):
        self._set_ref_object(NewsWebsite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = Article
        self.scraped_obj_item_class = ArticleItem
        super(ArticleSpider, self).__init__(self, *args, **kwargs)