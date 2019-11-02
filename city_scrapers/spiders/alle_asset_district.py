import re
from datetime import datetime
from urllib.parse import urljoin

import scrapy
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class AlleAssetDistrictSpider(CityScrapersSpider):
    name = "alle_asset_district"
    agency = "Allegheny Regional Asset District"
    timezone = "America/New_York"
    allowed_domains = ["radworkshere.org"]
    start_urls = ["https://radworkshere.org/pages/whats-happening?cal=board-meetings"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
        needs.
        """

        res = response.css('#board-meetings .pages .post-title a::attr("href")')
        res_urls = res.extract()
        for rel_url in res_urls:
            url = urljoin(response.url, rel_url)
            yield scrapy.Request(url, callback=self.parse_meeting)

    def parse_meeting(self, response):
        meeting = Meeting(
            title=self._parse_title(response),
            location=self._parse_location(response),
            description=self._parse_description(response),
            source=self._parse_source(response),
            start=self._parse_start(response)
        )

        meeting["id"] = self._get_id(meeting)

        yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return item.css(".post-title h1::text").extract_first()

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return item.xpath("//div[@class='body-wizy']/p//text()").extract_first()

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        up_startdate = item.css(".published::text").extract_first().strip()
        p_startdate = datetime.strptime(up_startdate, "%a, %b %d, %Y")
        description = self._parse_description(item)
        TIME_REGEX = re.compile(r'\d{1,2}:\d{2}[AaPp][Mm]')
        tm_found = TIME_REGEX.search(description)
        if tm_found:
            up_starttime = tm_found[0]
            p_starttime = datetime.strptime(up_starttime, '%I:%M%p').time()
            startdatetime = datetime.combine(p_startdate, p_starttime)
        else:
            TIME2_REGEX = re.compile(r'\d{1,2}[AaPp][Mm]')
            tm_found = TIME2_REGEX.search(description)
            if tm_found:
                up_starttime = tm_found[0]
                p_starttime = datetime.strptime(up_starttime, '%I%p').time()
                startdatetime = datetime.combine(p_startdate, p_starttime)
            else:
                startdatetime = p_startdate
        return startdatetime

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
        add_row = item.xpath("(//div[@class='body-wizy']//div[@class='row'])[2]")
        address = add_row.css(".info p::text").extract_first()
        name_row = item.xpath("(//div[@class='body-wizy']//div[@class='row'])[1]")
        name = name_row.css(".info p::text").extract_first()
        return {
            "address": address,
            "name": name,
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
