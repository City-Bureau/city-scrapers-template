from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.city_planning import CityPlanningSpider

test_response = file_response(
    join(dirname(__file__), "files", "city_planning.html"),
    url="http://pittsburghpa.gov/dcp/notices",
)
spider = CityPlanningSpider()

freezer = freeze_time("2019-03-15")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()

#def test_tests():
#assert False
"""
Uncomment below
"""


def test_title():
    assert parsed_items[0]["title"
                           ] == "Inclusionary Zoning Interim Planning Overlay District (IPOD-6)\xa0"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 4, 23, 14, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


# def test_id():
#     assert parsed_items[0]["id"] == "EXPECTED ID"

# def test_status():
#     assert parsed_items[0]["status"] == "EXPECTED STATUS"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": '',
        "address": '200 Ross Street, 1st Floor Conference Room'
    }


# def test_source():
#     assert parsed_items[0]["source"] == "EXPECTED URL"


def test_links():
    assert parsed_items[0]["links"] == [{
        "href": "http://pittsburghpa.gov/dcp/ipod6",
        "title": "here"
    }]


def test_classification():
    assert parsed_items[0]["classification"] == NOT_CLASSIFIED


# @pytest.mark.parametrize("item", parsed_items)
# def test_all_day(item):
#     assert item["all_day"] is False
