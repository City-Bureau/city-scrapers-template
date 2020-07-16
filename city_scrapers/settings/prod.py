import os

from .base import *  # noqa

USER_AGENT = "City Scrapers [production mode]. Learn more and say hello at https://citybureau.org/city-scrapers"  # noqa

# Uncomment one of the following DiffPipeline classes to enable a diff pipeline that
# will deduplicate output UIDs based on City Scrapers IDs and list any meetings in the
# future which no longer appear in scraped results as cancelled.

# Configure item pipelines
ITEM_PIPELINES = {
    # "city_scrapers_core.pipelines.S3DiffPipeline": 200,
    # "city_scrapers_core.pipelines.AzureDiffPipeline": 200,
    "city_scrapers_core.pipelines.MeetingPipeline": 300,
    "city_scrapers_core.pipelines.OpenCivicDataPipeline": 400,
}

# Uncomment one of the StatusExtension classes to write an SVG badge of each scraper's
# status to Azure or S3 after each time it's run.

# By default, this will write to the same bucket or container as the feed export, but
# this can be configured by adding a value in the CITY_SCRAPERS_STATUS_BUCKET or
# CITY_SCRAPERS_STATUS_CONTAINER for S3 and Azure respectively.

SENTRY_DSN = os.getenv("SENTRY_DSN")

EXTENSIONS = {
    # "city_scrapers_core.extensions.AzureBlobStatusExtension": 100,
    # "city_scrapers_core.extensions.S3StatusExtension": 100,
    "scrapy_sentry.extensions.Errors": 10,
    "scrapy.extensions.closespider.CloseSpider": None,
}

FEED_EXPORTERS = {
    "json": "scrapy.exporters.JsonItemExporter",
    "jsonlines": "scrapy.exporters.JsonLinesItemExporter",
}

FEED_FORMAT = "jsonlines"

# Uncomment S3 or Azure to write scraper results to static file storage as
# newline-delimited JSON files made up of OCD events following the meeting schema.

FEED_STORAGES = {
    # "s3": "scrapy.extensions.feedexport.S3FeedStorage",
    # "azure": "city_scrapers_core.extensions.AzureBlobFeedStorage",
}

# Uncomment credentials for whichever provider you're using

# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# S3_BUCKET = os.getenv("S3_BUCKET")
# CITY_SCRAPERS_STATUS_CONTAINER = S3_BUCKET

# AZURE_ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME")
# AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")
# AZURE_CONTAINER = os.getenv("AZURE_CONTAINER")
# CITY_SCRAPERS_STATUS_CONTAINER = AZURE_CONTAINER

# Uncomment the FEED_URI for whichever provider you're using

# FEED_URI = "s3://{bucket}/%(year)s/%(month)s/%(day)s/%(hour_min)s/%(name)s.json".format(  # noqa
#     bucket=S3_BUCKET
# )

# FEED_URI = (
#     "azure://{account_name}:{account_key}@{container}"
#     "/%(year)s/%(month)s/%(day)s/%(hour_min)s/%(name)s.json"
# ).format(
#     account_name=AZURE_ACCOUNT_NAME,
#     account_key=AZURE_ACCOUNT_KEY,
#     container=AZURE_CONTAINER,
# )
