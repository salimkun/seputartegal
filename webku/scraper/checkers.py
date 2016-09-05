from __future__ import unicode_literals
from dynamic_scraper.spiders.django_checker import DjangoChecker
from webku.models import Article


class ArticleChecker(DjangoChecker):
    
    name = 'article_checker'
    allowed_domains = ["en.wikinews.org"]
    start_urls = [
        "http://en.wikinews.org/wiki/Main_Page", (1)
    ]
	    
    def __init__(self, *args, **kwargs):
        self._set_ref_object(Article, **kwargs)
        self.scraper = self.ref_object.news_website.scraper
        #self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.checker_runtime
        super(ArticleChecker, self).__init__(self, *args, **kwargs)