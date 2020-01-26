from .base import *

USER_AGENT = "City Scrapers [production mode]. Learn more and say hello at https://citybureau.org/city-scrapers"

# Configure item pipelines
ITEM_PIPELINES = {
    "city_scrapers_core.pipelines.DefaultValuesPipeline": 100,
    "city_scrapers_core.pipelines.S3DiffPipeline": 200,
    "city_scrapers_core.pipelines.MeetingPipeline": 300,
    "city_scrapers_core.pipelines.OpenCivicDataPipeline": 400,
}

SENTRY_DSN = os.getenv("SENTRY_DSN")

# Uncomment one of the StatusExtension classes to write an SVG badge of each scraper's status to
# Azure or S3 after each time it's run.

# By default, this will write to the same bucket or container as the feed export, but this can be
# configured by adding a value in the CITY_SCRAPERS_STATUS_BUCKET or CITY_SCRAPERS_STATUS_CONTAINER
# for S3 and Azure respectively.

EXTENSIONS = {
    "scrapy_sentry.extensions.Errors": 10,
    "city_scrapers_core.extensions.S3StatusExtension": 100,
    "scrapy.extensions.closespider.CloseSpider": None,
}

FEED_EXPORTERS = {
    "json": "scrapy.exporters.JsonItemExporter",
    "jsonlines": "scrapy.exporters.JsonLinesItemExporter",
}

FEED_FORMAT = "jsonlines"

FEED_STORAGES = {
    "s3": "scrapy.extensions.feedexport.S3FeedStorage",
}

# Uncomment credentials for whichever provider you're using

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

CITY_SCRAPERS_STATUS_BUCKET = "city-scrapers-pitt"

# Uncomment the FEED_URI for whichever provider you're using

FEED_URI = "s3://city-scrapers-pitt/%(year)s/%(month)s/%(day)s/%(hour_min)s/%(name)s.json"
