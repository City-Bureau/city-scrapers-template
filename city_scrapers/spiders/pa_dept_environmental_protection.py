import datetime
import re

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class PaDeptEnvironmentalProtectionSpider(CityScrapersSpider):
    name = "pa_dept_environmental_protection"
    agency = "PA Department of Environmental Protection"
    timezone = "America/New_York"
    allowed_domains = ["www.ahs.dep.pa.gov"]
    start_urls = ["http://www.ahs.dep.pa.gov/CalendarOfEvents/Default.aspx?list=true"]
    custom_settings = {'ROBOTSTXT_OBEY': False}

    # Things I need to work on currently:
    # Returning a list thing correctly for location
    #   The test for location indicates that
    # Setting up the tests correctly, and making sure they pass

    def parse(self, response):
        for meetingChunk in response.xpath('//div[@class = "centered_div padtop"]').getall():
            if '<strong>' in meetingChunk:
                meeting = Meeting(
                    title=self._parse_title(meetingChunk),
                    description=self._parse_description(meetingChunk),
                    location=self._parse_location(meetingChunk),
                    time_notes=self._parse_time_notes(meetingChunk),
                    start=self._parse_start(meetingChunk),
                    end=self._parse_end(meetingChunk),
                    links=self._parse_links(meetingChunk),
                    source=self._parse_source(meetingChunk),
                    classification=self._parse_classification(meetingChunk),

                    # classification=self._parse_classification(item),
                    # all_day=self._parse_all_day(item),
                )

                # meeting["status"] = self._get_status(meeting)
                # meeting["id"] = self._get_id(meeting)

                yield meeting

    def _parse_title(self, item):
        titleRegex = re.compile(r'(am|pm) : (.)+</td>')
        thisThing = titleRegex.search(item)
        return thisThing.group()[5:-5]

    def _parse_time_notes(self, item):
        return None

    def _parse_description(self, item):
        descriptionRegex = re.compile(r'Description:(.)+')
        thisThing = descriptionRegex.search(item)
        return thisThing.group()[97:-5]

    def _parse_location(self, item):
        descriptionRegex = re.compile('Location:</td>.*?</td>', re.DOTALL)
        thisThing = descriptionRegex.search(item)
        cleanString = thisThing.group()[91:].replace('\n', ' ')
        return {"name": "Untitled", "address": cleanString[:-5]}

    def _parse_links(self, item):
        linkRegex = re.compile(r'Web address(.)+.aspx(\w)*(\'|\")')
        linkThing = linkRegex.search(item)
        if linkThing is not None:
            linkThing = linkRegex.search(item)
            return [{"href": str(linkThing.group()[117:-1]), "title": "more info"}]
        return None

    def _parse_end(self, item):
        pmRegex = re.compile(r'to (\d)+:\d\d')
        pmThing = pmRegex.search(item)

        if pmThing is not None:
            dateRegex = re.compile(r'(\d)+/(\d)+/\d\d\d\d')
            dateThing = dateRegex.search(item)
            ds = dateThing.group().split("/")

            pmSplit = pmThing.group()[2:].split(":")
            pmSplit[0] = int(pmSplit[0])

            minutes = 0
            if int(pmSplit[1]) > 0:
                minutes = int(pmSplit[1])

            twelveHourRegex = re.compile(r'to (\d)+:\d\d [a-z][a-z]')
            twelveHourThing = twelveHourRegex.search(item)

            if twelveHourThing.group()[-2:] == "pm":
                if pmSplit[0] != 12:
                    pmSplit[0] += 12

            return datetime.datetime(int(ds[2]), int(ds[0]), int(ds[1]), pmSplit[0], minutes)

        return None

    def _parse_start(self, item):
        dateRegex = re.compile(r'(\d)+/(\d)+/\d\d\d\d')
        dateThing = dateRegex.search(item)
        ds = dateThing.group().split("/")

        amRegex = re.compile(r'(\d)+:\d\d')
        amThing = amRegex.search(item)
        amSplit = amThing.group().split(":")
        amSplit[0] = int(amSplit[0])

        twelveHourRegex = re.compile(r':\d\d [a-z][a-z]')
        twelveHourThing = twelveHourRegex.search(item)

        minutes = 0
        if int(amSplit[1]) > 0:
            minutes = int(amSplit[1])

        # Handles starts in the PM
        if twelveHourThing.group()[4:] == "pm":
            if amSplit[0] != 12:
                amSplit[0] += 12

        return datetime.datetime(int(ds[2]), int(ds[0]), int(ds[1]), amSplit[0], minutes)

    def _parse_classification(self, item):
        return NOT_CLASSIFIED

    def _parse_all_day(self, item):
        return False

    # Want to double check if this is appropriate code
    def _parse_source(self, response):
        return "http://www.ahs.dep.pa.gov/CalendarOfEvents/Default.aspx?list=true"
        # return response.url
