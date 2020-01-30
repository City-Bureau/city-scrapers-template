from datetime import datetime, time

from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse

url = "http://www.puc.pa.gov/about_puc/public_meeting_calendar/public_meeting_audio_summaries_.aspx"

# Pulled this information from the site's PDFs
ADDRESS = "400 North St, Harrisburg, PA 17120",
LOCATION_NAME = "MAIN HEARING ROOM NO. 1 SECOND FLOOR COMMONWEALTH KEYSTONE BUILDING",

# The meetings always seem to being at 10AM; this isn't reported on the page itself,
# but is derived from reading minutes/agenda pdfs.
DEFAULT_START_TIME = time(hour=10)


class PaUtilitySpider(CityScrapersSpider):
    name = "pa_utility"
    agency = "PA Public Utility Commission"
    timezone = "America/New_York"
    start_urls = [url]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
       """

        self.logger.info("PARSING")
        content = response.css('.center').xpath('.//text()').getall()
        # self.logger.warning(content)

        # this was necessary to make pytest consistent with scarpy
        content = [text.lstrip('\r') for text in content]
        # self.logger.warning(content)

        # the following text appears before the meeting dates are listed
        meeting_start_flag = '\n\tPublic Meeting Dates'

        for i, item in enumerate(content):
            if item == meeting_start_flag:
                break
        meeting_content = content[i + 1:]
        # self.logger.warning(meeting_content)

        # filter to text that includes the meet dates
        meeting_dates = [d for d in meeting_content if str.startswith(d, '\n\t')]
        # self.logger.warning(meeting_dates)

        for date_str in meeting_dates:
            # self.logger.info(date_str)

            meeting = Meeting(
                title=self._parse_title(date_str),
                description=self._parse_description(date_str),
                classification=self._parse_classification(date_str),
                start=self._parse_start(date_str),
                end=self._parse_end(date_str),
                all_day=False,
                time_notes=self._parse_time_notes(date_str),
                location=self._parse_location(date_str),
                links=self._parse_links(date_str),
                source=self._parse_source(response)
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return "Pennsylvania Public Utility Commission Public Meetings"

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return "None"

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return COMMISSION

    def _parse_start(self, date_str):
        """Parse start datetime as a naive datetime object."""
        return datetime.combine(parse(date_str), DEFAULT_START_TIME)

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
        """Seems like the meeting is always in the same place given the info in the Agenda PDFs."""
        return {
            "address": ADDRESS,
            "name": LOCATION_NAME,
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
