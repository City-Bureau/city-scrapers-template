from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pitt_ethics_board import PittEthicsBoardSpider

test_response = file_response(
    join(dirname(__file__), "files", "pitt_ethics_board.html"),
    url="http://pittsburghpa.gov/ehb/ehb-meetings",
)
spider = PittEthicsBoardSpider()

freezer = freeze_time("2020-02-09")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Ethics Hearing Board Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 2, 11, 16, 15)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == "pitt_ethics_board/202002111615/x/ethics_hearing_board_meeting"


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "City-County Building, Room 646",
        "address": "414 Grant St, Pittsburgh, PA 15219"
    }


def test_source():
    assert parsed_items[0]["source"] == "http://pittsburghpa.gov/ehb/ehb-meetings"


def test_links():
    url = 'https://apps.pittsburghpa.gov'
    url += '/redtail/images/'
    url += '8493_ETHICS_HEARING_BOARD_AGENDA_FEB_11.pdf'
    expected = [{'href': url, 'title': 'Agenda'}]
    assert parsed_items[0]["links"] == expected


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
