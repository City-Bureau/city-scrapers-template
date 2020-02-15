import re

import dateutil.parser
from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class AlleFinanceDevSpider(CityScrapersSpider):
    name = "alle_finance_dev"
    agency = "Allegheny County Finance and Development Commission"
    timezone = "America/Chicago"
    root_url = "https://alleghenycounty.us"
    start_urls = [root_url + "/economic-development/authorities/meetings-reports/fdc/meetings.aspx"]
    TIME = "9:30 am"
    ADDRESS = "112 Washington Place, Pittsburgh, PA 15219"
    NAME = "One Chatham Center, Suite 900"
    ADDRESS_PATTERN = "112 washington place"

    def parse(self, response):
        # Check that the time has not changed:
        time_info = response.xpath(
            '/html/body/form/div[3]/div[3]/section' +
            '/div[1]/div[2]/div/div/div/div/table/tbody/tr[1]/td[2]'
        ).get()
        if self.TIME not in time_info.lower():
            raise ValueError("Time has changed.")

        # Check that the location has not changed:
        location_info = response.xpath(
            '/html/body/form/div[3]/div[3]' +
            '/section/div[1]/div[2]/div/div/div/div/table/tbody/tr[2]/td[2]'
        ).get()
        if self.ADDRESS_PATTERN not in location_info.lower():
            raise ValueError("Meeting location has changed.")

        # Get the list of meeting dates:
        meeting_soup = response.xpath(
            '/html/body/form/div[3]/div[3]/section' +
            '/div[1]/div[2]/div/div/div/div/table/tbody/tr[3]/td[2]'
        ).get()
        # Clean up the list of meeting dates:
        meeting_soup = re.sub('\r', '', meeting_soup)
        meeting_soup = re.sub('\n', '', meeting_soup)
        meeting_soup = re.sub('\xa0', '', meeting_soup)
        meeting_soup = re.sub('</p>', '', meeting_soup)
        meeting_soup = meeting_soup.lower()
        meetings = meeting_soup.split('<p><p>')[1:]
        pattern = (
            u'(january|february|march|april|may|june|' +
            'july|august|september|october|december) ' + '(\\d*),( )*(\\d\\d\\d\\d)'
        )
        meetings = re.findall(pattern, meeting_soup)

        for item in meetings:
            meeting = Meeting(
                title=self._parse_title(),
                description=self._parse_description(),
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(),
                links=self._parse_links(),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self):
        """Parse or generate meeting title."""
        return self.agency + " Meeting"

    def _parse_description(self):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return COMMISSION

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        return dateutil.parser.parse(item[0] + ' ' + item[1] + ' ' + item[-1] + ' ' + self.TIME)

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self):
        """Parse or generate location."""
        return {
            "address": self.ADDRESS,
            "name": self.NAME,
        }

    def _parse_links(self):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
