import os
from datetime import datetime
from json import loads

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from scrapy import FormRequest, Request


class PghMayorOfficeCommAffSpider(CityScrapersSpider):
    name = "pgh_mayor_office_comm_aff"
    agency = "Pittsburgh Mayor's Office of Community Affairs"
    timezone = "US/Eastern"
    allowed_domains = ["nextdoor.com"]
    start_urls = ["https://nextdoor.com/login/"]
    cookies = {}

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
        needs.
        """

        username = os.environ['NEXTDOOR_USERNAME']
        password = os.environ['NEXTDOOR_PASSWORD']

        data = {
            'scope': 'openid',
            'client_id': 'NEXTDOOR-WEB',
            'grant_type': 'password',
            'username': username,
            'password': password,
            'state': '71da7809-840e-4ef4-86d1-a13e9c0afa40191223'  # not sure what state does
        }

        headers = {
            ':authority': 'auth.nextdoor.com',
            ':method': 'POST',
            ':path': '/v2/token',
            ':scheme': 'https',
            'accept': 'application/json, text/plain , */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'origin': 'https://nextdoor.com',
            'referer': 'https://nextdoor.com/',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': (
                'Mozilla/5.0 (X11; CrOS x86_64 12 607.58.0) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.86 Safari/537.36'
            ),
            'device-fp': 'v1419700a0150af69fde242c19b64f916c',  # device fingerprint
            # (unfortunatly device-fp is needed)
            'device-id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaaaaaaaa'  # obviously faked
        }

        token_url = "https://auth.nextdoor.com/v2/token"

        formReq = FormRequest(
            token_url, formdata=data, headers=headers, callback=self._authenticated
        )
        yield formReq

    def _authenticated(self, response):
        url = "https://nextdoor.com/api/profile/2376387/activity/posts/"
        token = loads(response.text)
        self.cookies.update({'ndbr_at': token['access_token'], 'ndbr_idt': token['id_token']})
        req = Request(url, cookies=self.cookies, callback=self._get_posts)
        yield req

    def _get_posts(self, response):
        jsonData = loads(response.body_as_unicode())
        activities = jsonData["activities"]
        for item in activities:
            if "meeting" in item["message_parts"][1]["text"].lower():
                url = "https://nextdoor.com/web/feeds/post/" + str(item["post_id"]) + "/"
                req = Request(url, cookies=self.cookies, callback=self._get_post)
                yield req
        if jsonData["show_more"]:
            url = "https://nextdoor.com/api/profile/2376387/activity/posts/?next_page="
            req = Request(
                url + jsonData["next_page"], cookies=self.cookies, callback=self._get_posts
            )
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
        now_words = ["today", "tonight"]
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
