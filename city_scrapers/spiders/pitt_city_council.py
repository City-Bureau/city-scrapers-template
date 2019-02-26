from datetime import datetime, timedelta
from legistar.events import LegistarEventsScraper

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import Spider, LegistarSpider


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
                'event_description': self._parse_description(item),
                'start': self._parse_start(item),
                'end': self._parse_end(item),
                'all_day': self._parse_all_day(item),
                'location': self._parse_location(item),
                'sources': self._parse_sources(item),
                'documents': self._parse_documents(item)
            }
            data['status'] = self._generate_status(data, item['Meeting Location'])
            data['id'] = self._generate_id(data)
            yield data

    def _parse_documents(self, item):
        """
        Returns meeting details, agenda, minutes, video, if available.
        """
        documents = []
        details = item['Meeting Details']
        if type(details) == dict:
            documents.append({
                'note': 'Meeting Details',
                'url': details['url'],
                'media_type': 'text',
                'date': ''
            })
        agenda = item['Agenda']
        if type(agenda) == dict:
            documents.append({
                'note': 'Agenda',
                'url': agenda['url'],
                'media_type': 'text',
                'date': ''
            })
        minutes = item['Minutes']
        if type(agenda) == dict:
            documents.append({
                'note': 'Minutes',
                'url': minutes['url'],
                'media_type': 'text',
                'date': ''
            })
        video = item['Video']
        if type(video) == dict:
            documents.append({
                'note': 'Video',
                'url': video['url'],
                'media_type': 'video',
                'date': ''
            })
        return documents

    def _parse_location(self, item):
        """
        Parse or generate location.
        """
        location = item['Meeting Location'].split('/n')[0]
        address = ''
        if 'Council Chambers' in location:
            address = '414 Grant Street, Pittsburgh, PA 15219'
        return {
            'address': address,
            'location': location,
            'name': '',
            'neighborhood': ''
        }

    def _parse_all_day(self, item):
        """
        Parse or generate all-day status. Defaults to false.
        This currently isn't denoted on the council site; we can update this function if that changes.
        """
        return False

    def _parse_name(self, item):
        """
        Parse or generate event name.
        """
        name = item['Name']['label']
        if 'City Council' in name:
            name + ' : meeting'
        return name

    def _parse_start_datetime(self, item):
        """
        Return the start date and time as a datetime object.
        """
        time = item.get('Meeting Time', None)
        date = item.get('Meeting Date', None)
        if date and time:
            time_string = '{0} {1}'.format(date, time)
            return datetime.strptime(time_string, '%m/%d/%Y %I:%M %p')
        return None

    def _parse_start(self, item):
        """
        Parse the start date and time.
        """
        start_datetime = self._parse_start_datetime(item)
        if start_datetime:
            return {
                'date': start_datetime.date(),
                'time': start_datetime.time(),
                'note': ''
            }
        return {
            'date': None,
            'time': None,
            'note': ''
        }

    def _parse_end(self, item):
        """
        No end times are listed, so estimate the end time to
        be 3 hours after the start time.
        """
        start_datetime = self._parse_start_datetime(item)
        if start_datetime:
            return {
                'date': start_datetime.date(),
                'time': (start_datetime + timedelta(hours=3)).time(),
                'note': 'Estimated 3 hours after start time'
            }
        return {
            'date': None,
            'time': None,
            'note': ''
        }

    def _parse_sources(self, item):
        """
        Parse sources.
        """
        try:
            url = item['Name']['url']
        except:
            url = 'https://pittsburgh.legistar.com/Calendar.aspx'
        return [{'url': url, 'note': ''}]

    # def parse_legistar(self, events):
    #     """
    #     `parse_legistar` should always `yield` Meeting items.

    #     Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
    #     needs.
    #     """
    #     for event, _ in events:
    #         meeting = Meeting(
    #             title=event["Name"]["label"],
    #             description=self._parse_description(event),
    #             classification=self._parse_classification(event),
    #             start=self.legistar_start(event),
    #             end=self._parse_end(event),
    #             all_day=self._parse_all_day(event),
    #             time_notes=self._parse_time_notes(event),
    #             location=self._parse_location(event),
    #             links=self.legistar_links(event),
    #             source=self.legistar_source(event),
    #         )

    #         meeting["status"] = self._get_status(meeting)
    #         meeting["id"] = self._get_id(meeting)

    #         yield meeting

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        if item['Meeting Location'].split('/n')[1]:
            return item['Meeting Location'].split('/n')[0]
        else:
            return 'no description'

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED
