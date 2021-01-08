from .base import *  # noqa

USER_AGENT = (
    "City Scrapers [production mode]. Learn more and say hello at cityscrapers.org"
)

# Configure item pipelines
ITEM_PIPELINES = {
    "city_scrapers_core.pipelines.MeetingPipeline": 300,
}

EXTENSIONS = {
    "scrapy.extensions.closespider.CloseSpider": None,
}

SPIDER_MIDDLEWARES = {
    "city_scrapers.middleware.CityScrapersWaybackMiddleware": 500,
}
