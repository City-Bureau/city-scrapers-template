from city_scrapers_core.constants import NOT_CLASSIFIED, BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
import dateutil
from datetime import time, datetime

import re


class PittHousingSpider(CityScrapersSpider):
    name = "pitt_housing"
    agency = "Housing Authority of Pittsburgh"
    timezone = "America/New_York"
    start_urls = ["https://hacp.org/about/board-commissioners-minutes/"]
    meeting_row_pattern = re.compile(r"(?P<date>.*):(?P<location>.*)")
    default_start_time = time(hour=10, minute=30)

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for list_item in response.xpath("//section//ul//li"):
            list_item_text = list_item.xpath(".//text()").get()
            match = self.meeting_row_pattern.match(list_item_text)
            if match:
                date_str = match.group('date')
                location_str = match.group('location')
                meeting = Meeting(
                    title=self._parse_title(list_item),
                    description="",
                    classification=BOARD,
                    start=self._parse_start(date_str),
                    end=None,
                    all_day=False,
                    time_notes="",
                    location={'address': location_str.strip()},
                    links=[],
                    source=response.url
                )
                yield meeting

    def _parse_title(self, _):
        """Parse or generate meeting title."""
        return "Housing Authority of the City of Pittsburgh Board Meeting"

    def _parse_start(self, date_str):
        """Parse start datetime as a naive datetime object."""
        parsed_date = dateutil.parser.parse(date_str)
        return datetime.combine(parsed_date.date(), self.default_start_time)
