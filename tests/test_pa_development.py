from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pa_development import PaDevelopmentSpider

test_response = file_response(
    join(dirname(__file__), "files", "pa_development.json"), url="https://dced.pa.gov/events/"
)
spider = PaDevelopmentSpider()

freezer = freeze_time("2019-03-11")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Rescheduled – PEDFA Board Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 3, 13, 13, 0)


def test_end():
    assert parsed_items[0]["end"] == datetime(2019, 3, 13, 14, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == "pa_development/201903131300/x/_pedfa_board_meeting"


def test_status():
    assert parsed_items[0]["status"] == "cancelled"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Keystone Building 4th Floor, Conference Room 4 East",
        "address": "400 North Street, Harrisburg, PA, 17011"
    }


def test_source():
    assert parsed_items[0]["source"] == "https://dced.pa.gov/event/pedfa-board-meeting-2/"


def test_links():
    assert parsed_items[0]["links"] == [{"href": "", "title": ""}]


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
