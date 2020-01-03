import re
from datetime import datetime

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class AlleHealthSpider(CityScrapersSpider):
    name = "alle_health"
    agency = "Allegheny County Board of Health"
    timezone = "America/Chicago"
    allowed_domains = ["www.alleghenycounty.us"]
    start_urls = [
        "https://www.alleghenycounty.us/Health-Department/Resources" +
        "/About/Board-of-Health/Public-Meeting-Schedule.aspx"
    ]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """

        unicode_text = response.text
        #        page_encoding = response.encoding

        paragraphs = re.findall(r'<p.*?</p>', unicode_text, re.S)

        next_event_src = [p for p in paragraphs if re.search(' next ', p)][0]
        next_event_date_re = r'>[^<>]*?([a-zA-Z]*\s+\d+,\s+20[12]\d)'
        print("L33: agency is |" + AlleHealthSpider.agency + "|")

        try:
            next_event_date1 = re.search(next_event_date_re, next_event_src)
            if not next_event_date1:
                raise RuntimeError('Error1')
            next_event_date_str = next_event_date1.group(1)
            next_event_time_re = r'>[^<>]*at\s+(\d+:\d\d\s*[apAP][mM])'
            next_event_time1 = re.search(next_event_time_re, next_event_src)
            next_time = (next_event_time1 and next_event_time1.group(1)) or ''

            next_event_datetime1 = next_event_date_str + " " + next_time

            if ':' in next_event_datetime1:
                next_format = "%B %d, %Y %I:%M %p"
            else:
                next_format = "%B %d, %Y"

            print("L47: next_event_datetime1 is |" + str(next_event_datetime1) + "|")
            next_datetime = datetime.strptime(next_event_datetime1, next_format)
            if not next_datetime:
                raise RuntimeError('Error2')

            next_meeting = Meeting(
                title=AlleHealthSpider.agency + " " + next_event_datetime1,
                start=next_datetime,
                source=AlleHealthSpider.start_urls[0]
            )
            #                    next_meeting["status"] = self._get_status(next_meeting)
            next_meeting["id"] = self._get_id(next_meeting)
            yield next_meeting
        except RuntimeError:
            pass

        mlre = r'<h3>Upcoming Meetings.*?<ul.*?</ul>'
        meeting_list1 = re.search(mlre, unicode_text, re.S)
        meeting_list = (meeting_list1 and meeting_list1.group(0)) or ''
        meetings = re.findall(r'<li.*?</li>', meeting_list)

        for item in meetings:
            mdate1 = re.search('>([^<]+)', item)
            if mdate1:
                mdate2 = mdate1.group(1)

                try:
                    mdate = datetime.strptime(mdate2, "%B %d, %Y")
                    meeting = Meeting(
                        title=AlleHealthSpider.agency + " " + mdate2,
                        start=mdate,
                        source=AlleHealthSpider.start_urls[0]
                    )
                    #                    meeting["status"] = self._get_status(meeting)
                    meeting["id"] = self._get_id(meeting)
                    yield meeting
                except ValueError:
                    pass

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return ""

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        return None

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
        return {
            "address": "",
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
