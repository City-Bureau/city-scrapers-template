import json  # interact with the Tribe Events API
import re  # parse strings
import urllib.request  # pull info from the website
from datetime import datetime  # convert utc time to datetime
from html.parser import HTMLParser  # clean up HTML

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider

# Downloads the json list dictating what pages are to be crawled:
json_url = 'http://www.ura.org/events.json'
url = urllib.request.urlopen(json_url)
json_events = json.loads(url.read().decode())


# Accepts an iso_8601 string, returns an equivalent datetime object.
# This method does not change its' output according to the local timezone.
def _pittsburgh_iso_to_datetime(iso_string):
    expression = '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
    expression += 'T[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]'
    time_regex = re.compile(expression)
    shortened_8601_string = re.findall(time_regex, iso_string)[0]
    format = '%Y-%m-%dT%H:%M:%S.%f'
    datetime_string = datetime.strptime(shortened_8601_string, format)
    return datetime_string


# Helper class for strip_tags
class MLStripper(HTMLParser):
    # original author: eloff
    # source: https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


# Accepts an html string, returns a string without any html tags.
# For example, strip_tags("<h1>foo</h1>") will return just "foo".
def strip_tags(html):
    # original author: eloff
    # source: https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# Returns an array of urls representing meeting detail pages
def get_ura_urls():
    urls = []
    base = 'https://www.ura.org/events/housing-opportunity-fund-advisory-board-meeting?day='
    searchKey = 'Housing Opportunity Fund Advisory Board Meeting'
    for event in json_events:
        if searchKey in event['title']:
            candidate = _pittsburgh_iso_to_datetime(event['start'])
            month = str(candidate.month)
            day = str(candidate.day)
            year = str(candidate.year)
            date_url_query_parameter = month + '-' + day + '-' + year
            urls.append(str(base + date_url_query_parameter))
    return urls


class PittHousingOppSpider(CityScrapersSpider):
    name = "pitt_housing_opp"
    agency = "Housing Opportunity Fund Advisory Board Pittsburgh"
    timezone = "America/New_York"
    allowed_domains = ["www.ura.org"]
    start_urls = get_ura_urls()

    def parse(self, item):
        """
        `parse` should always `yield` Meeting items.
        Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
        needs.
        """
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
            source=self._parse_source(item),
        )

        meeting["status"] = self._get_status(meeting)
        meeting["id"] = self._get_id(meeting)

        yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return strip_tags(item.xpath('//*[@id="main"]/div/div[1]/div/h2').get())

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        desc = item.xpath('//*[@id="main"]/div/div[2]/div[2]/div[1]').get()
        return re.sub('\n', '', strip_tags(desc))

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return BOARD

    def _parse_date(self, item):
        """Parse the date as a string. Helper function to _parse_start and _parse_end."""
        date_xpath = '//*[@id="main"]/div/div[1]/div/div[1]/div[1]'
        date_pair = strip_tags(item.xpath(date_xpath).get()).split('.')
        month = date_pair[0]
        day = date_pair[1]
        year_xpath = '//*[@id="main"]/div/div[1]/div/div[1]/div[2]'
        year = strip_tags(item.xpath(year_xpath).get())
        return year + '-' + month + '-' + day

    def _parse_times_helper(self, item):
        """Parse the start/end times as an array"""
        times_xpath = '//*[@id="main"]/div/div[1]/div/div[2]/div[1]'
        times_raw = strip_tags(item.xpath(times_xpath).get())
        expression = '(.[0-9]:[0-9][0-9].(A|P|a|p).?(M|m).?)'
        times_clean = re.findall(expression, times_raw)
        return times_clean

    def _parse_start_time_of_day(self, item):
        return re.sub(' ', '', self._parse_times_helper(item)[0][0])

    def _parse_end_time_of_day(self, item):
        return re.sub(' ', '', self._parse_times_helper(item)[1][0])

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        date = self._parse_date(item)
        start_time = self._parse_start_time_of_day(item)
        date_string = str(date) + ' ' + str(start_time)
        return datetime.strptime(date_string, '%Y-%m-%d %I:%M%p')

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        date = self._parse_date(item)
        end_time = self._parse_end_time_of_day(item)
        date_string = str(date) + ' ' + str(end_time)
        return datetime.strptime(date_string, '%Y-%m-%d %I:%M%p')

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        venue_name = strip_tags(item.xpath('//*[@id="main"]/div/div[1]/div/div[2]/div[2]').get())
        xpath = '//*[@id="main"]/div/div[1]/div/div[2]/div[3]'
        venue_address = re.sub('\n', ', ', strip_tags(item.xpath(xpath).get()))
        return {
            "address": venue_address,
            "name": venue_name,
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
