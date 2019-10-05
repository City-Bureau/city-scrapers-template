import html  # clean up html strings (such as &amp)
import json  # interact with the Tribe Events API
from datetime import datetime  # convert utc time to datetime

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


# remove html encoding and convert to a string object
def clean(my_json_string):
    return str(html.unescape(my_json_string))


class PaDevelopmentSpider(CityScrapersSpider):
    name = "pa_development"
    agency = "PA Department of Community & Economic Development"
    timezone = "America/New_York"
    allowed_domains = ["dced.pa.gov"]
    start_urls = ["https://dced.pa.gov/wp-json/tribe/events/v1/events"]

    def parse(self, response):
        events = json.loads(response.text)['events']

        for item in events:
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
                source=self._parse_source(item),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return clean(item['title'])

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return clean(item['description'])

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return BOARD

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        start_time = datetime.strptime(item['start_date'], '%Y-%m-%d %H:%M:%S')
        return start_time

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return datetime.strptime(item['end_date'], '%Y-%m-%d %H:%M:%S')

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return item['all_day']

    def _get_street(self, item):
        try:
            return clean(item['venue']['address'])
        except KeyError:
            return ''

    def _get_city(self, item):
        try:
            return clean(item['venue']['city'])
        except KeyError:
            return ''

    def _get_state(self, item):
        try:
            return clean(item['venue']['state'])
        except KeyError:
            return ''

    def _get_zip(self, item):
        try:
            return clean(item['venue']['zip'])
        except KeyError:
            return ''

    def _parse_location(self, item):
        """Parse or generate location."""
        address = self._get_street(item)
        address += ', ' + self._get_city(item)
        address += ', ' + self._get_state(item)
        address += ', ' + self._get_zip(item)
        return {
            "address": address,
            "name": clean(item['venue']['venue']),
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, item):
        """Parse or generate source."""
        url = item['url']
        return url
