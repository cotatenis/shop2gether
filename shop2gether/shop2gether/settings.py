BOT_NAME = 'shop2gether'
VERSION = '0-9-0'
SPIDER_MODULES = ['shop2gether.spiders']
NEWSPIDER_MODULE = 'shop2gether.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

MAGIC_FIELDS = {
    "timestamp": "$isotime",
    "spider": "$spider:name",
    "url": "$response:url",
}
SPIDER_MIDDLEWARES = {
    "scrapy_magicfields.MagicFieldsMiddleware": 100,
}

SPIDERMON_ENABLED = True

EXTENSIONS = {
    'shop2gether.extensions.SentryLogging' : -1,
    'spidermon.contrib.scrapy.extensions.Spidermon': 500,
}

ITEM_PIPELINES = {
    "shop2gether.pipelines.DiscordMessenger" : 100,
    "shop2gether.pipelines.Shop2ImagePipeline" : 200,
    "shop2gether.pipelines.GCSPipeline": 300,
    "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 400,
}

SPIDERMON_VALIDATION_MODELS = (
    'shop2gether.validators.Shop2GetherItem',
)

SPIDERMON_SPIDER_CLOSE_MONITORS = (
'shop2gether.monitors.SpiderCloseMonitorSuite',
)

SPIDERMON_VALIDATION_DROP_ITEMS_WITH_ERRORS = True
SPIDERMON_PERIODIC_MONITORS = {
'shop2gether.monitors.PeriodicMonitorSuite': 60, # time in seconds
}
SPIDERMON_CUSTOM_MIN_ITEMS = {
    'shop2-adidas' : 110,
    'shop2-nike-female' : 20,
    'shop2-nike-male' : 100
}

SPIDERMON_SENTRY_DSN = ""
SPIDERMON_SENTRY_PROJECT_NAME = ""
SPIDERMON_SENTRY_ENVIRONMENT_TYPE = ""
#THROTTLE
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 5

#GCP
GCS_PROJECT_ID = ""
GCP_CREDENTIALS = ""
GCP_STORAGE = ""
GCP_STORAGE_CRAWLER_STATS = ""
#FOR IMAGE UPLOAD
IMAGES_STORE = f''
IMAGES_THUMBS = {
    '400_400': (400, 400),
}

#DISCORD
DISCORD_WEBHOOK_URL = ""
DISCORD_THUMBNAIL_URL = ""
SPIDERMON_DISCORD_WEBHOOK_URL = ""
#LOG
LOG_LEVEL = "INFO"