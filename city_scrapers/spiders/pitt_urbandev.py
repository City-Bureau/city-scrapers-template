import re
from datetime import datetime

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider

BASE_URL = "https://www.ura.org"
EXPECTED_START_HOUR = "2 p.m."
EXPECTED_START_HOUR_AS_INT = 14
TITLE = "URA Board Meeting"


class PittUrbandevSpider(CityScrapersSpider):
    name = "pitt_urbandev"
    agency = "Urban Redevelopment Authority of Pittsburgh"
    timezone = "America/New_York"
    start_urls = ["https://www.ura.org/pages/board-meeting-notices-agendas-and-minutes"]

    def parse(self, response):
        soup = response.xpath("//*[@id=\"main\"]/section[3]").get().split("<div class=\"links\">")

        normal_location = self._parse_location(response)
        start_hour = self._parse_starting_hour(response)

        for i in range(1, len(soup)):
            item = soup[i]
            meeting = Meeting(
                title=self._parse_title(item),
                description=self._parse_description(item),
                classification=self._parse_classification(item),
                start=self._parse_start(item, start_hour),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=normal_location,
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return TITLE

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        # For the most robust string comparisons we convert to lower case.
        item_lowered = item.lower()
        if "regular board meeting" in item_lowered:
            return "Regular board meeting"
        elif "rescheduled board meeting" in item_lowered:
            return "Rescheduled board meeting"
        else:
            return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return BOARD

    def _parse_start(self, item, start_hour):
        try:
            """Parse start datetime as a naive datetime object."""
            raw = item.split('</h6>')[0]
            raw = re.sub("<h6>", "", raw)
            start_time = datetime.strptime(raw, '%B %d, %Y')

            if EXPECTED_START_HOUR in start_hour:
                start_time = start_time.replace(hour=EXPECTED_START_HOUR_AS_INT)
                return start_time
            else:
                return None
        except ValueError:
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

    def _parse_starting_hour(self, response):
        raw = response.xpath("//*[@id=\"main\"]/section[2]/div[1]/p[1]").get().lower()
        found_start_hour = ""
        if EXPECTED_START_HOUR in raw:
            found_start_hour = EXPECTED_START_HOUR
        return found_start_hour

    def _parse_location(self, response):
        """Parse or generate location."""
        raw = response.xpath("//*[@id=\"main\"]/section[2]/div[1]/p[1]").get().lower()
        expected_address = "412 Boulevard of the Allies, Pittsburgh, PA 15219"
        expected_room_name = "Lower Level Conference Room"
        found_address = ""
        found_room_name = ""

        if expected_address.lower() in raw:
            found_address = expected_address

        if expected_room_name.lower() in raw:
            found_room_name = expected_room_name

        return {
            "address": found_address,
            "name": found_room_name,
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        links = []
        try:
            raw_hrefs = re.findall(r'\/media\/[\S]*pdf', item)
            hrefs = []

            for href in raw_hrefs:
                hrefs.append(BASE_URL + href)

            raw_titles = re.split(r'.pdf', item)
            titles = []

            for i in range(1, len(raw_titles)):
                raw_title = raw_titles[i]
                raw_title = re.sub('\">', '', raw_title)
                raw_title = re.sub(r'<\/a', '', raw_title)
                clean_title = re.sub('>.*', '', raw_title)
                titles.append(clean_title)

            for j in range(0, len(hrefs)):
                links.append({"href": hrefs[j], "title": titles[j]})
        except TypeError:
            pass
        except KeyError:
            pass
        except AttributeError:
            pass

        return links

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
