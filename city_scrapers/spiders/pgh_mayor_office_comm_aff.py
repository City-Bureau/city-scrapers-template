from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from scrapy import Request
from scrapy import FormRequest
from json import loads
from datetime import datetime

class PghMayorOfficeCommAffSpider(CityScrapersSpider):
    name = "pgh_mayor_office_comm_aff"
    agency = "Pittsburgh Mayor's Office of Community Affairs"
    timezone = "US/Eastern"
    allowed_domains = ["nextdoor.com"]
    start_urls = ["https://nextdoor.com/login/"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
        needs.
        """
        token = response.xpath("//div[@class='login-form']//*[@name='csrfmiddlewaretoken']/@value").extract_first()

        username = USERNAME_GOES_HERE
        password = PASSWORD_GOES_HERE

        data = {
            "username": username, 
            "password": password, 
            "remember_me": "on", 
            "next": "/profile/2376387/", 
            "csrfmiddlewaretoken":token, 
            "social_id": "", 
            "social_network": "", 
            "link_account_version": "0"
            }

        headers = {
            "Accept":"text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"en-US,en;q=0.5",
            "Connection":"keep-alive",
            "Content-Length":"217",
            "Content-Type":"application/x-www-form-urlencoded",
            "Host":"nextdoor.com",
            "Referer":"https://nextdoor.com/login/?ucl=1",
            "Upgrade-Insecure-Requests":"1",
            "origin": "https://nextdoor.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
        }

        formReq = FormRequest.from_response(
            response,
            formdata=data,
            headers=headers,
            callback=self._authenticated
            )
        yield formReq

    def _authenticated(self, response):
        url = "https://nextdoor.com/api/profile/2376387/activity/posts/"
        req = Request(url, callback=self._get_posts)
        yield req


    def _get_posts(self, response):
        jsonData = loads(response.body_as_unicode())
        activities = jsonData["activities"]
        for item in activities:
            if "meeting" in item["message_parts"][1]["text"].lower():
                url = "https://nextdoor.com/web/feeds/post/"+str(item["post_id"])+"/"
                req = Request(url, callback=self._get_post)
                yield req
        if jsonData["show_more"]:
            url = "https://nextdoor.com/api/profile/2376387/activity/posts/?next_page="
            req = Request(url+jsonData["next_page"], callback=self._get_posts)
            yield req

    def _get_post(self, response):
        jsonData = loads(response.body_as_unicode())
        item = jsonData["posts"][0]
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

        yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        title = item["subject"]
        return title

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        description = item["body"]
        return description

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        creation_date = item["creation_date"]
        creation_date = datetime.utcfromtimestamp(creation_date)
        now_words = ["today","tonight"]
        tom_words = ["tomorrow"]
        if any(word in item["subject"].lower() for word in now_words):
            return creation_date
        elif any(word in item["subject"].lower() for word in tom_words):
            return creation_date + datetime.timedelta(days=1)
        else:
            return creation_date

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return datetime.now()

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
