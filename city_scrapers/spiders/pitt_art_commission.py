from datetime import datetime, time

from city_scrapers_core.constants import CANCELLED, COMMISSION
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class PittArtCommissionSpider(CityScrapersSpider):
    name = "pitt_art_commission"
    agency = "City of Pittsburgh Art Commission"
    timezone = "America/New_York"
    start_urls = ["https://pittsburghpa.gov/dcp/art-commission-schedule"]

    # Even though the tables storing the meeting information seem to have 4 columns,
    # there are 3 additional invisible columns; hence we expect 7 columns in each row.
    expected_column_count = 7

    # The meetings always seem to being at 2PM; this isn't reported on the page itself,
    # but is derived from reading minutes/agenda pdfs.
    default_start_time = time(hour=14)

    def parse(self, response):
        """
        Parse Meeting items from the Art Commission website.

        Meeting objects are extracted from an HTML table. Each row has information about the date of
        the meeting, along with a few potential links to relevant meeting documents.
        """

        meeting_rows = response.xpath("//table//tr[@class='data']")
        for row in meeting_rows:
            columns = row.xpath(".//td")
            if len(columns) != self.expected_column_count:
                continue

            date_str = columns[1].xpath(".//text()").get()
            cancelled_str = columns[6].xpath(".//text()").get()

            meeting = Meeting(
                title=self._parse_title(row),
                description=self._parse_description(row),
                classification=self._parse_classification(row),
                start=self._parse_start(date_str),
                end=self._parse_end(row),
                all_day=self._parse_all_day(row),
                time_notes=self._parse_time_notes(row),
                location=self._parse_location(row),
                links=self._parse_links(row),
                source=self._parse_source(response),
            )

            if cancelled_str and "cancelled" in cancelled_str.lower():
                meeting["status"] = CANCELLED
            else:
                meeting["status"] = self._get_status(meeting)

            meeting["id"] = self._get_id(meeting)
            yield meeting

    def _parse_title(self, row):
        """Parse or generate meeting title."""
        return "Art Commission of Pittsburgh Monthly Meeting"

    def _parse_description(self, row):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, row):
        """Parse or generate classification from allowed options."""
        return COMMISSION

    def _parse_start(self, date_str):
        """Parse start datetime as a naive datetime object.

        Note that we currently use a fixed start time, since this information is not available
        from the webpage, save through looking at PDF downloads.
        """
        return datetime.combine(datetime.strptime(date_str, "%m/%d/%Y"), self.default_start_time)

    def _parse_end(self, row):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, row):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, row):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, row):
        """Parse or generate location."""

        # There is no indication of the meeting place on the page itself, but this seems to be the
        # common location, as described in the meeting minutes/agenda pdf downloads.
        return {
            "location": "1st Floor Hearing Room",
            "address": "200 Ross Street, Pittsburgh, PA, 15219",
            "name": "",
        }

    def _parse_links(self, table_row):
        return [{
            "href": link.xpath(".//@href").get(),
            "title": link.xpath(".//text()").get()
        } for link in table_row.xpath(".//a")]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
