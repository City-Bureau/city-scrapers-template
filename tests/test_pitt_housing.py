from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD, PASSED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pitt_housing import PittHousingSpider

test_response = file_response(
    join(dirname(__file__), "files", "pitt_housing.html"),
    url="https://hacp.org/about/board-commissioners-minutes/",
)
spider = PittHousingSpider()

freezer = freeze_time("2020-02-21")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]
freezer.stop()
    g

def test_title():
    expected_title = "Housing Authority of the City of Pittsburgh Board Meeting"
    for item in parsed_items:
        assert item["title"] == expected_title


def test_start():
    expected_start_dates_2020 = {
        datetime(year=2020, month=1, day=23, hour=10, minute=30),
        datetime(year=2020, month=2, day=27, hour=10, minute=30),
        datetime(year=2020, month=3, day=26, hour=10, minute=30),
        datetime(year=2020, month=4, day=23, hour=10, minute=30),
        datetime(year=2020, month=5, day=28, hour=10, minute=30),
        datetime(year=2020, month=6, day=25, hour=10, minute=30),
        datetime(year=2020, month=7, day=23, hour=10, minute=30),
        datetime(year=2020, month=9, day=24, hour=10, minute=30),
        datetime(year=2020, month=10, day=22, hour=10, minute=30),
        datetime(year=2020, month=12, day=17, hour=10, minute=30)
    }

    actual_start_dates_2020 = {
        meeting["start"]
        for meeting in parsed_items
        if meeting["start"].year == 2020
    }

    assert expected_start_dates_2020 == actual_start_dates_2020


def test_end():
    for item in parsed_items:
        assert item["end"] is None


def test_time_notes():
    for item in parsed_items:
        assert item["time_notes"] == ""


def test_location():
    expected_locations = [
        "200 Ross St, 9th floor conference room",
        "200 Ross St, 1st floor conference room",
        "200 Ross St, 1st floor conference room",
        "200 Ross St, 1st floor conference room",
        "200 Ross St, 1st floor conference room",
        "200 Ross St, 1st floor conference room",
        "200 Ross St, 1st floor conference room",
        "200 Ross St, 1st floor conference room",
        "200 Ross St, 1st floor conference room",
        "200 Ross St, 1st floor conference room",
    ]

    idx = 0
    for item in parsed_items:
        assert item["location"]["address"] == expected_locations[idx]
        idx += 1


def test_classification():
    for item in parsed_items:
        assert item["classification"] == BOARD


def test_all_day():
    for item in parsed_items:
        assert item["all_day"] is False

# The 'id' or 'source' fields aren't customized currently, so these are commented out.
# def test_id():
#     assert parsed_items[0]["id"] == "EXPECTED ID"

# def test_source():
#     assert parsed_items[0]["source"] == "EXPECTED URL"
