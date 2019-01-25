import unicodedata
from datetime import timedelta

from city_scrapers_core.constants import BOARD, COMMITTEE
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse
from lxml import html


class AllePortAuthoritySpider(CityScrapersSpider):
    name = "alle_port_authority"
    agency = "Port Authority of Allegheny County"
    timezone = "America/New_York"
    allowed_domains = ["www.portauthority.org"]
    start_urls = [
        "https://www.portauthority.org/paac/CompanyInfoProjects/BoardofDirectors/MeetingAgendasResolutions.aspx"  # noqa
    ]
    custom_settings = {'ROBOTSTXT_OBEY': False}

    def _get_address(self, response):
        address = (response.xpath('//table[1]//span/text()').extract()[0])
        return address

    def _build_datatable(self, response):
        alist_tbody = (response.xpath('//table[1]/tbody//td').extract())

        atable = []
        arow = []

        for item in alist_tbody:
            tree = html.fragment_fromstring(item)
            text = tree.text_content()

            url = tree.xpath('//a/@href')
            find_att_b = tree.xpath('//b/text()|//strong/text()')
            if len(find_att_b) >= 1:
                continue
            if url:
                arow.append('{name}: {url}'.format(name=text, url=url[0]))
            else:
                arow.append('{text}'.format(text=unicodedata.normalize("NFKD", text)))
            if len(arow) == 6:
                atable.append(arow)
                arow = []

        return atable

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
        needs.
        """
        address = self._get_address(response)
        atable = self._build_datatable(response)

        for row in atable:
            start = self._parse_start(row)
            meeting = Meeting(
                title=self._parse_title(row),
                description="",
                classification=self._parse_classification(row),
                start=start,
                end=self._parse_end(start),
                all_day=False,
                time_notes="Estimated 3 hour meeting length",
                location=self._parse_location(address),
                links=self._parse_links(row),
                source=response.url,
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            if not (meeting.get("start") and meeting.get("end")):
                continue
            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return item[0]

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        meeting_title = item[0].lower()
        if "committee" in meeting_title:
            return COMMITTEE
        return BOARD

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        if "cancel" in item[2].lower():
            return None

        if not item[1].strip():
            if "stakeholder" in item[0].lower():
                time_str = "8:30 a.m."
            if "performance oversight" in item[0].lower():
                time_str = "9:00 a.m."
            else:
                time_str = "9:30 a.m."
        else:
            time_str = item[1]
        date_str = "{} {}".format(self.year, item[2])
        return parse("{} {}".format(date_str, time_str))

    def _parse_end(self, start):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return start + timedelta(hours=3)

    def _parse_location(self, address):
        """Parse or generate location."""
        room = "Neal H. Holmes Board Room"
        street = "345 Sixth Avenue, Fifth Floor"
        city = "Pittsburgh, PA 15222"

        if not (room in address and street in address):
            raise ValueError("The address for this meeting has changed")

        return {
            "address": ", ".join([room, street, city]),
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        documents = []
        details = item[5]
        if details.startswith("Minutes: http"):
            documents.append({"title": "Minutes", "href": details.split(' ')[-1]})
        agenda = item[3]
        if agenda.startswith("Agenda: http"):
            documents.append({"title": "Agenda", "href": agenda.split(' ')[-1]})
        resolution = item[4]
        if resolution.startswith("Resolutions: http"):
            documents.append({"title": "Resolution", "href": resolution.split(' ')[-1]})
        return documents
