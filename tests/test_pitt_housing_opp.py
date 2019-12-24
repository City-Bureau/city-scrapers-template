from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pitt_housing_opp import PittHousingOppSpider

test_response = file_response(
    join(dirname(__file__), "files", "pitt_housing_opp.html"),
    url="https://www.ura.org/events/housing-opportunity-fund-advisory-board-meeting",
)
spider = PittHousingOppSpider()

freezer = freeze_time("2019-03-13")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Housing Opportunity Fund Advisory Board Meeting"


def test_description():
    test_string = 'The Housing Opportunity Fund (HOF) was '
    assert test_string in parsed_items[0]["description"]


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 4, 4, 9, 0)


def test_end():
    assert parsed_items[0]["end"] == datetime(2019, 4, 4, 11, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


id = "pitt_housing_opp/201904040900/x"
id += "/housing_opportunity_fund_advisory_board_meeting"


def test_id():
    assert parsed_items[0]["id"] == id


def test_status():
    assert parsed_items[0]["status"] == "tentative"


address = 'City-County Building, Fifth Floor, 414 Grant Street, '
address += 'Pittsburgh, PA 15219'
location = {'address': address, 'name': 'City Council Chambers'}


def test_location():
    assert parsed_items[0]["location"] == location


source_url = "https://www.ura.org/events/housing-opportunity-fund-advisory-board-meeting"


# todo this should append the specific date at the
# end of the url to fetch the specific event
# time of day...
def test_source():
    assert parsed_items[0]["source"] == source_url


def test_links():
    assert parsed_items[0]["links"] == [{'href': '', 'title': ''}]


def test_classification():
    assert parsed_items[0]["classification"] == "Board"


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
