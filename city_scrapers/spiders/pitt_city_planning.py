# -*- coding: utf-8 -*-

import unicodedata
from datetime import timedelta

from city_scrapers_core.constants import BOARD, COMMITTEE
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse
from lxml import html


fetch("http://pittsburghpa.gov/dcp/notices")
title = response.css('div.col-md-12 p').extract()

#the events are all stored in the first 'div.col-md-12'
everything = response.css('div.col-md-12').extract()[0]


#ugly way to break everything up into a list of separate events, splitting by title location
events=[]
for i in range(0,len(title_index)-1):
    start=title_index[i]
    #for the last event, need to make the end point just the end of everything
    if i ==len(title_index)-1:
        end=len(everything)-len('<p><strong>')
    else:
        end=title_index[i+1]-len('<p><strong>')
    
    events.append(everything[start:end])


print(title)


for e in events:
    title=re.search('<strong>(.*?)</strong>',e).group(1)
    date=re.search('<li>(.*?)</li>',e).group(1)
    #cut e off after date, search for location in the remainder of the string
    e2=e[re.search('<li>(.*?)</li>',e).end():]
    location=re.search('<li>(.*?)</li>',e2).group(1)
    print("Event Name:",title)
    print("Date:",date)
    print("Location:",location)

class PittCityPlanningSpider(Spider):
    name = 'pitt_city_planning'
    agency_name = 'City of Pittsburgh Planning Commission'
    timezone = 'US/Eastern'
    allowed_domains = ['pittsburghpa.gov']
    start_urls = ['http://pittsburghpa.gov/dcp/notices']

    def parse(self, response):
        """
        `parse` should always `yield` a dict that follows the Event Schema
        <https://city-bureau.github.io/city-scrapers/06_event_schema.html>.

        Change the `_parse_id`, `_parse_name`, etc methods to fit your scraping
        needs.
        """
        for item in response.css('.eventspage'):

            data = {
                '_type': 'event',
                'name': self._parse_name(item),
                'event_description': self._parse_description(item),
                'classification': self._parse_classification(item),
                'start': self._parse_start(item),
                'end': self._parse_end(item),
                'all_day': self._parse_all_day(item),
                'location': self._parse_location(item),
                'documents': self._parse_documents(item),
                'sources': self._parse_sources(item),
            }

            data['status'] = self._generate_status(data, text='')
            data['id'] = self._generate_id(data)

            yield data

        # self._parse_next(response) yields more responses to parse if necessary.
        # uncomment to find a "next" url
        # yield self._parse_next(response)

    def _parse_next(self, response):
        """
        Get next page. You must add logic to `next_url` and
        return a scrapy request.
        """
        next_url = None  # What is next URL?
        return scrapy.Request(next_url, callback=self.parse)

    def _parse_name(self, item):
        """
        Parse or generate event name.
        """
        return ''

    def _parse_description(self, item):
        """
        Parse or generate event description.
        """
        return ''

    def _parse_classification(self, item):
        """
        Parse or generate classification (e.g. public health, education, etc).
        """
        return ''

    def _parse_start(self, item):
        """
        Parse start date and time.
        """
        return ''

    def _parse_end(self, item):
        """
        Parse end date and time.
        """
        return ''

    def _parse_all_day(self, item):
        """
        Parse or generate all-day status. Defaults to False.
        """
        return False

    def _parse_location(self, item):
        """
        Parse or generate location. Latitude and longitude can be
        left blank and will be geocoded later.
        """
        return {
            'address': '',
            'name': '',
            'neighborhood': '',
        }

    def _parse_documents(self, item):
        """
        Parse or generate documents.
        """
        return [{'url': '', 'note': ''}]

    def _parse_sources(self, item):
        """
        Parse or generate sources.
        """
        return [{'url': '', 'note': ''}]
