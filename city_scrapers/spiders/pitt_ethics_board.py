import re

import dateutil.parser
from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class PittEthicsBoardSpider(CityScrapersSpider):
    name = "pitt_ethics_board"
    agency = "Pittsburgh Ethics Hearing Board"
    timezone = "America/Chicago"
    start_urls = ["http://pittsburghpa.gov/ehb/ehb-meetings"]
    LOCATION = {
        "address": "414 Grant St, Pittsburgh, PA 15219",
        "name": "City-County Building, Room 646",
    }
    # This will be used to raise an error in the event that the
    # location has changed.
    LOCATION_DESCRIPTION = "Meetings occur in Room 646 of the City-County Building"
    TITLE = "Ethics Hearing Board Meeting"

    def parse(self, response):
        # location_info describes the normal location of these meetings. If
        # that changes, an error should be thrown.
        location_info = response.xpath('//*[@id="article"]/div/div/div/p').get()
        if self.LOCATION_DESCRIPTION not in location_info:
            raise ValueError("Meeting location has changed")

        # The DOM splits meetings into 2020, 2019, and previous years.
        # Here we combine those separate buckets into one big list:
        meeting_soup = response.xpath('//*[@id="article"]/div/div/div').get()
        # We split the soup by the collapsing accordions
        # The [1:-1] slice is to get rid of the first and last elements of the list,
        # which were not relevant to our needs.
        meetings_split_by_accordions = meeting_soup.split('collapsing-content')[1:-1]

        # This represents all columns in all years containing meetings. Each index
        # represents a column in the DOM.
        all_columns = []
        for year_soup in meetings_split_by_accordions:
            year_columns = year_soup.split('col-lg-4')[1:]
            for year_column in year_columns:
                all_columns.append(year_column)

        # Now we go through each column and split it into meetings:
        meetings = []
        for column in all_columns:
            for meeting in column.split(r'<p><strong>')[1:]:
                meetings.append(meeting)

        for item in meetings:
            meeting = Meeting(
                title=self._parse_title(item),
                description=self._parse_description(item),
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return self.TITLE

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return BOARD

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        time_soup = item.split('</strong>')[0]
        start_time = dateutil.parser.parse(time_soup)
        return start_time

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
        return self.LOCATION

    def _parse_links(self, item):
        """Parse or generate links."""
        a_tags = item.split('href=')[1:]
        # Break the a_tags into hrefs and titles
        links = []
        for a_tag in a_tags:
            href = re.findall(r'\"[^\"]*\"', a_tag)[0].strip("\"")
            title = re.findall(r'>.*</a>', a_tag)[0].strip(">").strip("//a>").strip("<")
            links.append({"href": href, "title": title})

        return links

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
