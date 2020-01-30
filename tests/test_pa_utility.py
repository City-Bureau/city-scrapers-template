from datetime import datetime
from os.path import dirname, join

import pytest
# from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pa_utility import PaUtilitySpider

url = "http://www.puc.pa.gov/about_puc/public_meeting_calendar/public_meeting_audio_summaries_.aspx"

spider = PaUtilitySpider()
test_response = file_response(join(dirname(__file__), "files", "pa_utility.html"), url=url)

freezer = freeze_time("2020-01-16")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_number_of_meetings():
    assert len(parsed_items) == 9


def test_title():
    assert parsed_items[0]["title"] == "Pennsylvania Public Utility Commission Public Meetings"


def test_description():
    assert parsed_items[0]["description"] == "None"


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 1, 16, 10, 0)


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)

# def test_time_notes():
#     assert parsed_items[0]["time_notes"] == "EXPECTED TIME NOTES"

# def test_id():
#     assert parsed_items[0]["id"] == "EXPECTED ID"

# def test_status():
#     assert parsed_items[0]["status"] == "EXPECTED STATUS"

# def test_location():
#     assert parsed_items[0]["location"] == {
#         "name": "EXPECTED NAME",
#         "address": "EXPECTED ADDRESS"
#     }

# def test_source():
#     assert parsed_items[0]["source"] == "EXPECTED URL"

# def test_links():
#     assert parsed_items[0]["links"] == [{
#       "href": "EXPECTED HREF",
#       "title": "EXPECTED TITLE"
#     }]

# def test_classification():
#     assert parsed_items[0]["classification"] == NOT_CLASSIFIED

# @pytest.mark.parametrize("item", parsed_items)
# def test_all_day(item):
#     assert item["all_day"] is False
