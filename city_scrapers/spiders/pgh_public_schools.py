from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from json import loads
from scrapy import Request
from datetime import datetime

class PghPublicSchoolsSpider(CityScrapersSpider):
    name = "pgh_public_schools"
    agency = "Pittsburgh Public Schools"
    timezone = "US/Eastern"
    allowed_domains = ["www.pghschools.org", "awsapieast1-prod2.schoolwires.com"]
    
    # start_urls = ["https://www.pghschools.org/calendar"]
    start_urls = ["https://www.pghschools.org/Generator/TokenGenerator.ashx/ProcessRequest"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
        needs.
        """
        json_response = loads(response.body_as_unicode())
        token = json_response["Token"]
        api_gateway = "https://awsapieast1-prod2.schoolwires.com/REST/api/v4/"
        api_function = "CalendarEvents/GetEvents/1?"
        start_date = "2019-02-01"
        end_date  = "2019-02-01"
        dates = "StartDate={}&EndDate={}".format(start_date,end_date)
        modules = "&ModuleInstanceFilter="
        category_filters="0-49-40-21-16-4-3-44-39-1-57-43-64-65-58-62-28-25-52-50-55-38-59-17-13-51-56-8-63-53-37-54-7-47-46-33-60-10-19-66-61-48-34-45-41-42-"
        category = "&CategoryFilter={}".format(category_filters)
        dbstream = "&IsDBStreamAndShowAll=true"
        url = api_gateway+api_function+dates+modules+category+dbstream
        req = Request(url, headers={"Authorization":"Bearer "+token, "Accept":"application/json"}, callback=self._parse_api)
        yield req

    def _parse_api(self,response):
        meetings = loads(response.body_as_unicode())
        for item in meetings:
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
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            return meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        title = item["Title"]
        return title

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        start_string = item["Start"]
        start_time = datetime.strptime(start_string, '%Y-%m-%dT%H:%M:%S')
        return start_time

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        end_string = item["End"]
        end_time = datetime.strptime(end_string, '%Y-%m-%dT%H:%M:%S')
        return end_time

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        all_day = item["AllDay"] == "True"
        return all_day

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
