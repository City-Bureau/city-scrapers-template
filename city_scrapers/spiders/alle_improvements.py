import datetime
import re
from urllib.parse import urljoin

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from scrapy.utils.response import get_base_url

RE_URL = re.compile(r'(?P<date>(\d{1,2}-\d{1,2}-\d{1,2}))-(?P<dtype>(\w+)).aspx')


def construct_dt(date_str, time_str):
    return datetime.datetime.strptime('{} {}'.format(date_str, time_str), '%B %d, %Y %I:%M %p')


class AlleImprovementsSpider(CityScrapersSpider):
    name = "alle_improvements"
    agency = "Allegheny County Authority for Improvements in Municipalities (AIM)"
    timezone = "America/New_York"
    allowed_domains = ["county.allegheny.pa.us"]
    start_urls = [
        (
            "https://www.county.allegheny.pa.us/economic-development/"
            "authorities/meetings-reports/aim/meetings.aspx"
        ),
    ]

    def parse(self, response):
        data = response.xpath("//table[@dropzone='copy']")

        time_str = self._parse_start_time(data)
        date_strs = self._parse_dates(data)
        location = self._parse_location(data)

        assert time_str is not None

        agenda_links, minute_links = self._parse_pdf_links(response)

        no_item = None

        for ds in date_strs:
            start = construct_dt(ds, time_str)

            meeting = Meeting(
                title=self._parse_title(no_item),
                description=self._parse_description(no_item),
                classification=self._parse_classification(no_item),
                start=start,
                end=self._parse_end(no_item),
                all_day=self._parse_all_day(no_item),
                time_notes=self._parse_time_notes(no_item),
                location=location,
                links=self._parse_links(ds, agenda_links, minute_links),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return (
            "Authority For Improvements In Municipalities Board Of Directors "
            "Regular And Public Hearing"
        )

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_dates(self, data):
        """Helper to extract list of meeting dates"""
        raw = data.xpath(".//td[contains(., 'Schedule')]/following-sibling::td//p/text()").extract()
        return [' '.join(r.strip().split()) for r in raw if r.strip()]

    def _parse_start_time(self, data):
        """Helper to extract time str of meeting"""
        tmp = data.xpath(".//td[contains(., 'Time')]/following-sibling::td/text()").extract_first()
        return ' '.join(tmp.split())

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
        raw = [
            r.strip() for r in
            item.xpath(".//td[contains(., 'Location')]/following-sibling::td/text()").extract()
        ]

        return {
            "address": '\n'.join(raw[1:]),
            "name": raw[0],
        }

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url

    def _parse_pdf_links(self, response):
        """Generate dict of (date, link) key values for agenda and minutes"""
        urls = response.xpath(
            '//a[contains(@href, "-minutes.aspx") or contains(@href, "-agenda.aspx")]/@href'
        ).extract()

        agendas = {}
        minutes = {}

        for url in urls:
            tmp = url.split('/')[-1]

            try:
                parsed = RE_URL.search(tmp).groupdict()
            except Exception:
                continue

            dtype = parsed.get('dtype')
            date = parsed.get('date')

            if dtype is None or date is None:
                continue

            full_url = urljoin(get_base_url(response), url)

            if dtype == 'minutes':
                minutes[date] = full_url
            elif dtype == 'agenda':
                agendas[date] = full_url

        return agendas, minutes

    def _parse_links(self, date_str, agenda_links, minute_links):
        links = []

        dsx = datetime.datetime.strptime(date_str, "%B %d, %Y").strftime('%m-%d-%y')

        if dsx in agenda_links:
            links.append({"href": agenda_links[dsx], "title": "Agenda {}".format(dsx)})

        if dsx in minute_links:
            links.append({"href": minute_links[dsx], "title": "Minutes {}".format(dsx)})

        return links
