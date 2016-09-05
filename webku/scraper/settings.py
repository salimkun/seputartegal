from __future__ import unicode_literals
# Scrapy settings for open_news project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import os, sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tegalku.settings")
sys.path.insert(0, os.path.join(PROJECT_ROOT, "D:/alim/projek/tegalku/webku")) #only for example_project


BOT_NAME = 'webku'
SPIDER_MODULES = ['dynamic_scraper.spiders', 'webku.scraper',]
USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')

#Scrapy 0.20+
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'
ELNETCONSOLE_HOST = '127.0.0.1' # defaults to 0.0.0.0 set so
TELNETCONSOLE_PORT = '6073'      # only we can see it.
TELNETCONSOLE_ENABLED = True

WEBSERVICE_ENABLED = True

LOG_ENABLED = True


ROBOTSTXT_OBEY = False

#Scrapy 0.20+
ITEM_PIPELINES = {
    'dynamic_scraper.pipelines.ValidationPipeline': 400,
    'webku.scraper.pipelines.DjangoWriterPipeline': 800,
}

DOWNLOAD_DELAY = 2.0


IMAGES_STORE = os.path.join(PROJECT_ROOT, '../thumbnails')

IMAGES_THUMBS = {
    'medium': (50, 50),
    'small': (25, 25),
}

HTTPERROR_ALLOW_ALL = True

RETRY_TIMES = 3

DOWNLOAD_TIMEOUT = 15

# Avoid in-memory DNS cache. See Advanced topics of docs for info
DNSCACHE_ENABLED = True

DSCRAPER_IMAGES_STORE_FORMAT = 'ALL'

DSCRAPER_LOG_ENABLED = True
DSCRAPER_LOG_LEVEL = 'INFO'
DSCRAPER_LOG_LIMIT = 5