from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from urllib.parse import urljoin
import scrapy
from datetime import datetime
from datetime import time

class AlleAssetDistrictSpider(CityScrapersSpider):
    name = "alle_asset_district"
    agency = "Allegheny Regional Asset District"
    timezone = "America/Chicago"
    allowed_domains = ["radworkshere.org"]
    start_urls = ["https://radworkshere.org/pages/whats-happening?cal=board-meetings"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
        needs.
        """
        for rel_url in response.css('#board-meetings .pages .post-title a::attr("href")').extract():
            url = urljoin(response.url, rel_url)
            yield scrapy.Request(url, callback=self.parse_meeting)

    def parse_meeting(self, response):
        up_startdate = response.css(".published::text").extract_first().strip()
        description = response.xpath("//div[@class='body-wizy']/p//text()").extract_first()
        p_startdate = datetime.strptime(up_startdate, "%a, %b %d, %Y")
        p_startdate = datetime.combine(p_startdate.date(), '00:00')
        print(p_startdate)
        print(p_startdate)
        meeting = Meeting(
            title = response.css(".post-title h1::text").extract_first(),
            location = {
                "name": response.xpath("(//div[@class='body-wizy']//div[@class='row'])[1]").css(".info p::text").extract_first(),
                "address": response.xpath("(//div[@class='body-wizy']//div[@class='row'])[2]").css(".info p::text").extract_first()
            },
            description = description,
            source = response.url
        )

        meeting["id"] = self._get_id(meeting)

        yield meeting


    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return ""

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        return None

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "",
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
