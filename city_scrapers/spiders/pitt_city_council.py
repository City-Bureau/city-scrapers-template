from datetime import datetime, timedelta

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.spiders import LegistarSpider
from legistar.events import LegistarEventsScraper


class PittCityCouncilSpider(LegistarSpider):
    name = "pitt_city_council"
    agency = "Pittsburgh City Council"
    timezone = "America/New_York"
    allowed_domains = ["pittsburgh.legistar.com"]
    start_urls = ["https://pittsburgh.legistar.com"]
    # Add the titles of any links not included in the scraped results
    link_types = []

    def parse(self, response):
        """
        `parse` should always `yield` a dict that follows the `Open Civic Data
        event standard <http://docs.opencivicdata.org/en/latest/data/event.html>`.
        Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
        needs.
        """
        events = self._make_legistar_call()
        return self._parse_events(events)

    def _make_legistar_call(self, since=None):
        les = LegistarEventsScraper(requests_per_minute=0)
        les.EVENTSPAGE = 'https://pittsburgh.legistar.com/Calendar.aspx'
        les.BASE_URL = 'https://pittsburgh.legistar.com'
        if not since:
            since = datetime.today().year
        return les.events(since=since)

    def _parse_events(self, events):
        for item, _ in events:
            name = self._parse_name(item)
            data = {
                '_type': 'event',
                'name': name,
                # OCD standard wants 'name', but city_scrapers_core wants 'title'
                'title': name,
                'description': self._parse_description(item),
                'timezone': self.timezone,
                'start': self._parse_start(item),
                'end': self._parse_end(item),
                'all_day': self._parse_all_day(item),
                'time_notes': 'Estimated three-hour meeting length',
                'location': self._parse_location(item),
                'source': self._parse_sources(item),
                'documents': self._parse_documents(item),
                'links': self.legistar_links(item),
                'classification': self._parse_classification(item),
            }
            data['status'] = self._get_status(data, item.get('Meeting Location'))
            data['id'] = self._get_id(data)
            yield data

    def _parse_documents(self, item):
        """
        Returns meeting details, agenda, minutes, video, if available.
        """
        documents = []
        details = item.get('Meeting Details')
        if type(details) == dict:
            documents.append({
                'note': 'Meeting Details',
                'url': details.get('url'),
                'media_type': 'text',
                'date': ''
            })
        agenda = item.get('Agenda')
        if type(agenda) == dict:
            documents.append({
                'note': 'Agenda',
                'url': agenda.get('url'),
                'media_type': 'text',
                'date': ''
            })
        minutes = item.get('Minutes')
        if type(minutes) == dict:
            documents.append({
                'note': 'Minutes',
                'url': minutes.get('url'),
                'media_type': 'text',
                'date': ''
            })
        video = item.get('Video')
        if type(video) == dict:
            documents.append({
                'note': 'Video',
                'url': video.get('url'),
                'media_type': 'video',
                'date': ''
            })
        return documents

    def _parse_location(self, item):
        """
        Parse or generate location.
        """
        location = item.get('Meeting Location').split('\n')[0]
        address = ''
        if 'Council Chambers' in location:
            address = '414 Grant Street, Pittsburgh, PA 15219'
        return {
            'address': address,
            'location': 'Council Chambers, 5th Floor',
            'name': '',
            'neighborhood': ''
        }

    def _parse_all_day(self, item):
        """
        Parse or generate all-day status. Defaults to false.
        This currently isn't denoted on the council site;
        we can update this function if that changes.
        """
        return False

    def _parse_name(self, item):
        """
        Parse or generate event name.
        """
        name = item.get('Name')
        if 'City Council' in name:
            name = name + ' : meeting'
        return name

    def _parse_start(self, item):
        """
        Return the start date and time as a localized datetime object.
        """
        time = item.get('Meeting Time', None)
        date = item.get('Meeting Date', None)
        if date and time:
            time_string = '{0} {1}'.format(date, time)
            return datetime.strptime(time_string, '%m/%d/%Y %I:%M %p')
        return None

    def _parse_end(self, item):
        """
        No end times are listed, so estimate the end time to
        be 3 hours after the start time.
        """
        return self._parse_start(item) + timedelta(hours=3)

    def _parse_sources(self, item):
        """
        Parse sources.
        """
        try:
            url = item.get('Meeting Details').get('url')
        except ValueError:
            url = 'https://pittsburgh.legistar.com/Calendar.aspx'
        return [{'url': url, 'note': ''}]

    def _parse_description(self, item):
        """
        Parse or generate meeting description.
        In Pittsburgh's case the meeting info comes on a new line
        in the location section, italicized.
        """
        try:
            return item.get('Meeting Location').split('\n')[1].split('--em--')[1]
        except IndexError:
            return 'no description'

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED
