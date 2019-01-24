import json
from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL, PASSED
from freezegun import freeze_time

from city_scrapers.spiders.alle_county import AlleCountySpider

freezer = freeze_time("2019-01-23")
freezer.start()

with open(join(dirname(__file__), "files", "alle_county.json"), "r") as f:
    test_response = json.load(f)

spider = AlleCountySpider()
parsed_items = [item for item in spider.parse_legistar(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "County Council"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 1, 22, 17, 0)


def test_end():
    assert parsed_items[0]["end"] == datetime(2019, 1, 22, 20, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == "Estimated 3 hour meeting length"


def test_id():
    assert parsed_items[0]["id"] == "alle_county/201901221700/x/county_council"


def test_status():
    assert parsed_items[0]["status"] == PASSED


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "",
        "address":
            "Regular Meeting, Fourth Floor, Gold Room, 436 Grant Street, Pittsburgh, PA 15219"
    }


def test_source():
    assert parsed_items[0][
        "source"
    ] == "https://alleghenycounty.legistar.com/DepartmentDetail.aspx?ID=26127&GUID=0B26890F-A762-408F-A03C-110A9BD4CAD9"  # noqa


def test_links():
    assert parsed_items[0]["links"] == [{
        "href":
            "https://alleghenycounty.legistar.com/View.ashx?M=A&ID=673968&GUID=2D730472-FA66-4E04-A43B-F169863AD1B7",  # noqa
        "title": "Agenda"
    }]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
