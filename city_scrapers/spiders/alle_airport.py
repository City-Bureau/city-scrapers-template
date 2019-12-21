import re
from datetime import datetime

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class AlleAirportSpider(CityScrapersSpider):
    name = "alle_airport"
    agency = "Allegheny County Airport Authority"
    timezone = "America/New_York"
    allowed_domains = ["flypittsburgh.com"]
    start_urls = ["https://www.flypittsburgh.com/about-us/leadership"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """

        # I didn't know how to list defualt locations and time other than
        # hard code them in.
        # It was elsewhere in the page in a paragraph

        DEFAULT_LOCATION = [
            "Pittsburgh International Airport",
            "Conference Room A, 4th Flr Mezzanine, Landside Terminal",
            "Pittsburgh International Airport"
        ]
        DEFAULT_TIME = [11, 30, 0]

        print("\n\n\n\n\nBEGIN SPIDER\n\n\n\n")
        # takes page HTML and and parses into date time and location
        datetimeLocationList = self.responseProcessing(response, DEFAULT_LOCATION, DEFAULT_TIME)
        print(datetimeLocationList)
        print("\n\n\n\n\n")
        for dtL in datetimeLocationList:
            print("IN LOOP")
            meeting = Meeting(
                title="Allegheny County Airport Authority Board Meeting",
                description="",
                classification=self._parse_classification(dtL),
                start=dtL[0],
                end=None,
                all_day=self._parse_all_day(dtL),
                time_notes=self._parse_time_notes(dtL),
                location=self._parse_location(dtL),
                links=self._parse_links(response),
                source=self._parse_source(response),
            )
            # NOT SURE WHAT THESE DO
            # TODO: LOOK INTO AT NEXT MEETING
            # meeting["status"] = self._get_status(meeting)
            # meeting["id"] = self._get_id(meeting)
            yield meeting
            print("AFTER YIELD")

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
        return item

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, dtL):
        """Parse or generate location."""
        return {
            "address": dtL[1][1],
            "name": dtL[1][0],
        }

    def _parse_links(self, response):
        """Parse or generate links."""
        # Extracts text content of <title> tag
        title = self.striphtml(response.xpath("//title").get()).strip()
        href = response.url
        return [{"href": href, "title": title}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url

    #################################################################
    # GENERAL STRING UTILS - FROM STACK OVERFLOW. LINK BELOW

    # Function to strip HTML tags from string
    # https://stackoverflow.com/questions/3398852/using-python-remove-html-tags-formatting-from-a-string
    def striphtml(self, data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)

    # Function to remove a list of substrings from a string
    def removeStrings(self, string, remList):
        for rem in remList:
            string = string.replace(rem, "")
        return string

    #################################################################
    # ALLEGHENY AIRPORT STRING PARSING FUNCTIONS - AUTHOR ALEK BINION

    # Function to determine if the line is a date by seeing
    # if a month is in the string
    def getDate(self, string):
        month_lst = [
            'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
            'October', 'November', 'December'
        ]
        for i in range(len(month_lst)):
            if month_lst[i].lower() in string.lower():
                # regex to remove all non-numeric chars from string
                # leaving the day in month of eveny
                day = re.sub('[^0-9]', '', string)
                if day == "":
                    return None
                # index + 1 is calandar month
                monthDay = [i + 1, int(day)]
                return monthDay
        return None

    # Function to check if the even was cancelled or moved
    def checkIfCancelledOrMoved(self, appointment, defaultTime):
        # Words used to indicated cancelled meetings
        cancelledWords = ["no board meeting", "cancel"]
        # If the listing contains any of the key cancelled word phrases, then
        # then list the even as cancelled with None list of length 3
        for word in cancelledWords:
            if word in appointment.lower():
                return None
        # This section deals with the way alt locations are listed
        information = appointment.split("–")
        information = [self.removeStrings(i, ["*", "(", ")"]).strip() for i in information]
        location = [information[1], ""]
        return location

    # function to handle processing of a response to date, time, location
    def responseProcessing(self, response, defaultLocation, defaultTime):
        datesString = ""
        # This section handles finding the board meeting dates section of html
        # on the pgh airport website.
        for val in response.css('strong').getall():
            if "board meeting dates" in val.lower():
                datesString = val
                break
        splitStr = datesString.split("<br>")
        # This is a list which will contain [datetime,location] items representing meetings
        datesList = []
        # this section parses through the html section containing event information
        for val in splitStr:
            # Returns data as a list if there is a valid date for meeting
            # returns None otherwise
            date = self.getDate(val)
            if date is not None:
                # This line removes tag information if present
                newStr = self.removeStrings(val.strip(), ["strong", "<", ">", "/"])
                dateLocation = []
                # Creates a date-time event given defaultTime and date.
                eventDateTime = datetime(
                    datetime.today().year, date[0], date[1], defaultTime[0], defaultTime[1],
                    defaultTime[2]
                )
                # If an "*" is present meeting is either moved or cancelled
                if "*" in newStr:
                    location = self.checkIfCancelledOrMoved(newStr, defaultTime)
                    if location is not None:
                        dateLocation = [eventDateTime, location]
                # If no "*" is present than meeting is at default location
                else:
                    dateLocation = [eventDateTime, defaultLocation]
                datesList.append(dateLocation)
        return datesList
