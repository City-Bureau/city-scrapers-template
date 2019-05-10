from datetime import timedelta

from city_scrapers_core.constants import CITY_COUNCIL, COMMITTEE
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import LegistarSpider


class PittCityCouncilSpider(LegistarSpider):
    name = "pitt_city_council"
    agency = "Pittsburgh City Council"
    timezone = "America/New_York"
    allowed_domains = ["pittsburgh.legistar.com"]
    start_urls = ["https://pittsburgh.legistar.com"]
    # Add the titles of any links not included in the scraped results
    link_types = []

    def parse_legistar(self, events):
        """
        `parse_legistar` should always `yield` Meeting items.

        Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
        needs.
        """
        for event, _ in events:
            start = self.legistar_start(event)
            title = event.get("Name")
            meeting = Meeting(
                title=title,
                description=self._parse_description(event),
                classification=self._parse_classification(title),
                start=start,
                end=self._parse_end(start),
                all_day=False,
                time_notes="Estimated 3 hour meeting length",
                location=self._parse_location(event),
                links=self.legistar_links(event),
                source=self._parse_source(event),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_end(self, start):
        return start + timedelta(hours=3)

    def _parse_description(self, item):
        """
        Parse or generate meeting description.
        In Pittsburgh's case the meeting info comes on a new line
        in the location section, italicized.
        """
        try:
            return item.get('Meeting Location').split('\n')[1].split('--em--')[1]
        except IndexError:
            return ""

    def _parse_location(self, item):
        """
        Parse or generate location.
        """
        location = item.get('Meeting Location').split('\n')[0]
        address = ''
        if 'Council Chambers' in location:
            address = '414 Grant Street, Pittsburgh, PA 15219'
        return {
            'address': address,
            'location': 'Council Chambers, 5th Floor',
            'name': '',
            'neighborhood': ''
        }

    def _parse_classification(self, title):
        """Parse or generate classification from allowed options."""
        if "committee" in title.lower():
            return COMMITTEE
        return CITY_COUNCIL

    def _parse_source(self, item):
        """Parse source from meeting details if available"""
        default_source = "{}/Calendar.aspx".format(self.base_url)
        if isinstance(item.get("Meeting Details"), dict):
            return item["Meeting Details"].get("url", default_source)
        return default_source
