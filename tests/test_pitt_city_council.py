import json
from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import COMMITTEE, TENTATIVE
from freezegun import freeze_time

from city_scrapers.spiders.pitt_city_council import PittCityCouncilSpider

freezer = freeze_time("2019-02-25")
freezer.start()

with open(join(dirname(__file__), "files", "pitt_city_council.json"), "r") as f:
    test_response = json.load(f)

spider = PittCityCouncilSpider()
parsed_items = [item for item in spider.parse_legistar(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Standing Committee"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 2, 27, 10)


def test_end():
    assert parsed_items[0]["end"] == datetime(2019, 2, 27, 13)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == "Estimated 3 hour meeting length"


def test_id():
    assert parsed_items[0]["id"] == "pitt_city_council/201902271000/x/standing_committee"


def test_status():
    assert parsed_items[0]["status"] == TENTATIVE


def test_location():
    assert parsed_items[0]["location"] == {
        "location": "Council Chambers, 5th Floor",
        "address": "414 Grant Street, Pittsburgh, PA 15219",
        "name": "",
        "neighborhood": ""
    }


def test_source():
    assert parsed_items[0]["source"] == (
        "https://pittsburgh.legistar.com/MeetingDeta"
        "il.aspx?ID=681042&GUID=631BD673-830F-4759-"
        "9DDE-EB16B3F1E681&Options=info&Search="
    )


def test_links():
    assert parsed_items[2]["links"] == [{
        "href": (
            "https://pittsburgh.legistar.com/View.ashx?M="
            "A&ID=681276&GUID=78186660-60BC-459B-86C7-B97156416708"
        ),
        "title": "Agenda"
    }]


def test_classification():
    assert parsed_items[0]["classification"] == COMMITTEE


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
