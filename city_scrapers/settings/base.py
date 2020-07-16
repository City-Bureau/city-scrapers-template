import os

# Scrapy settings for city_scrapers project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = "city_scrapers"

SPIDER_MODULES = ["city_scrapers.spiders"]
NEWSPIDER_MODULE = "city_scrapers.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "City Scrapers [development mode]. Learn more and say hello at https://www.citybureau.org/city-scrapers/"  # noqa

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Throttle results by default
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = float(os.getenv("AUTOTHROTTLE_START_DELAY", 1.0))
AUTOTHROTTLE_MAX_DELAY = float(os.getenv("AUTOTHROTTLE_MAX_DELAY", 30.0))
AUTOTHROTTLE_TARGET_CONCURRENCY = float(
    os.getenv("AUTOTHROTTLE_TARGET_CONCURRENCY", 1.0)
)

# Configure item pipelines
ITEM_PIPELINES = {
    "city_scrapers_core.pipelines.MeetingPipeline": 200,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware": 543,
}

SPIDER_MIDDLEWARES = {}

# Use commands from city_scrapers_core package

COMMANDS_MODULE = "city_scrapers_core.commands"

EXTENSIONS = {
    "scrapy.extensions.closespider.CloseSpider": None,
}

CLOSESPIDER_ERRORCOUNT = 5
