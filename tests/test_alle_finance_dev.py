from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.alle_finance_dev import AlleFinanceDevSpider

root_url = "https://alleghenycounty.us"

test_response = file_response(
    join(dirname(__file__), "files", "alle_finance_dev.html"),
    url=root_url + "/economic-development/authorities/meetings-reports/fdc/meetings.aspx"
)
spider = AlleFinanceDevSpider()

freezer = freeze_time("2020-02-14")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == (
        "Allegheny County Finance and Development Commission Meeting"
    )


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 1, 28, 9, 30)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == (
        "alle_finance_dev/202001280930/x/" +
        "allegheny_county_finance_and_development_commission_meeting"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "One Chatham Center, Suite 900",
        "address": "112 Washington Place, Pittsburgh, PA 15219"
    }


def test_source():
    assert parsed_items[0]["source"] == (
        "https://alleghenycounty.us" +
        "/economic-development/authorities/meetings-reports/fdc/meetings.aspx"
    )


def test_links():
    assert parsed_items[0]["links"] == [{"href": "", "title": ""}]


def test_classification():
    assert parsed_items[0]["classification"] == COMMISSION


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
