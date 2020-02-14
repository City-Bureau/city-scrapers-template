from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pa_liquorboard import PaLiquorboardSpider

test_response = file_response(
    join(dirname(__file__), "files", "pa_liquorboard.html"),
    url="https://www.lcb.pa.gov/About-Us/Board/Pages/Public-Meetings.aspx",
)
spider = PaLiquorboardSpider()

freezer = freeze_time("2020-01-02")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 2, 12, 11, 0)


def test_id():
    assert parsed_items[0]["id"] == "pa_liquorboard/202002121100/x/"


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Pennsylvania Liquor Control Board Headquarters",
        "address": "Room 117, 604 Northwest Office Building, Harrisburg, PA 17124"
    }


def test_source():
    ref = "https://www.lcb.pa.gov/About-Us/Board/Pages/Public-Meetings.aspx"
    assert parsed_items[0]["source"] == ref


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


def test_all_day():
    assert parsed_items[0]["all_day"] is False
