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
    # "city_scrapers_core.pipelines.GCSDiffPipeline": 200,
    "city_scrapers_core.pipelines.MeetingPipeline": 300,
    "city_scrapers_core.pipelines.OpenCivicDataPipeline": 400,
}

# Uncomment one of the StatusExtension classes to write an SVG badge of each scraper's
# status to Azure, S3, or GCS after each time it's run.

# By default, this will write to the same bucket or container as the feed export, but
# this can be configured by adding a value in:
# CITY_SCRAPERS_STATUS_BUCKET for S3 or GCS, or
# CITY_SCRAPERS_STATUS_CONTAINER for Azure.

SENTRY_DSN = os.getenv("SENTRY_DSN")

EXTENSIONS = {
    # "city_scrapers_core.extensions.AzureBlobStatusExtension": 100,
    # "city_scrapers_core.extensions.S3StatusExtension": 100,
    # "city_scrapers_core.extensions.GCSStatusExtension": 100,
    "scrapy_sentry.extensions.Errors": 10,
    "scrapy.extensions.closespider.CloseSpider": None,
}

FEED_EXPORTERS = {
    "json": "scrapy.exporters.JsonItemExporter",
    "jsonlines": "scrapy.exporters.JsonLinesItemExporter",
}

FEED_FORMAT = "jsonlines"

# Uncomment S3, Azure, or GCS to write scraper results to static file storage as
# newline-delimited JSON files made up of OCD events following the meeting schema.

FEED_STORAGES = {
    # "s3": "scrapy.extensions.feedexport.S3FeedStorage",
    # "azure": "city_scrapers_core.extensions.AzureBlobFeedStorage",
    # "gcs": "scrapy.extensions.feedexport.GCSFeedStorage",
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

# GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# GCS_BUCKET = os.getenv("GCS_BUCKET")
# CITY_SCRAPERS_STATUS_BUCKET = GCS_BUCKET

# https://jansonh.github.io/scrapinghub-gcs/
# If "GOOGLE_APPLICATION_CREDENTIALS" is the credential rather than a path,
# we need to write a local file with the credential.
# (Important for certain providers, such as Github Actions integration.)
# Uncomment the following code block if using GCS.
# path = "{}/google-cloud-storage-credentials.json".format(os.getcwd())
# credentials_content = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# if not os.path.exists(credentials_content):
#    with open(path, "w") as f:
#        f.write(credentials_content)
#    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path


# Uncomment the FEED_URI for whichever provider you're using

# FEED_URI = (
#    "s3://{bucket}/%(year)s/%(month)s/%(day)s/%(hour_min)s/%(name)s.json"
# ).format(
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

# FEED_URI = (
#    "gs://{bucket}/%(year)s/%(month)s/%(day)s/%(hour_min)s/%(name)s.json"
# ).format(bucket=GCS_BUCKET)
