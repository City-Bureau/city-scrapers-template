from datetime import timedelta

from city_scrapers_core.constants import CITY_COUNCIL, COMMITTEE, FORUM
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import LegistarSpider


class AlleCountySpider(LegistarSpider):
    name = "alle_county"
    agency = "Allegheny County Government"
    timezone = "America/New_York"
    allowed_domains = ["alleghenycounty.legistar.com"]
    start_urls = ["https://alleghenycounty.legistar.com"]

    def parse_legistar(self, events):
        """
        `parse_legistar` should always `yield` Meeting items.

        Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
        needs.
        """
        for event, _ in events:
            start = self.legistar_start(event)
            meeting = Meeting(
                title=event["Name"]["label"],
                description="",
                classification=self._parse_classification(event),
                start=start,
                end=self._parse_end(start),
                all_day=False,
                time_notes="Estimated 3 hour meeting length",
                location=self._parse_location(event),
                links=self.legistar_links(event),
                source=self.legistar_source(event),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        meeting_loc_str = item["Meeting Location"].lower()
        if "hearing" in meeting_loc_str:
            return FORUM
        if "committee" in meeting_loc_str:
            return COMMITTEE
        return CITY_COUNCIL

    def _parse_end(self, start):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return start + timedelta(hours=3)

    def _parse_location(self, item):
        """Parse or generate location."""
        addr_str = ""
        room = item.get("Meeting Location")
        if room:
            addr_str += room + ", "
        addr_str += "436 Grant Street, Pittsburgh, PA 15219"
        return {
            "address": addr_str,
            "name": "",
        }
