from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD, TENTATIVE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.alle_port_authority import AllePortAuthoritySpider

test_response = file_response(
    join(dirname(__file__), "files", "alle_port_authority.html"),
    url=(
        "https://www.portauthority.org/paac/CompanyInfoProjects/BoardofDirectors/MeetingAgendasResolutions.aspx"  # noqa
    ),
)
freezer = freeze_time("2019-01-23")
freezer.start()

spider = AllePortAuthoritySpider()
parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Annual Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 1, 25, 9, 30)


def test_end():
    assert parsed_items[0]["end"] == datetime(2019, 1, 25, 12, 30)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == "Estimated 3 hour meeting length"


def test_id():
    assert parsed_items[0]["id"] == "alle_port_authority/201901250930/x/annual_meeting"


def test_status():
    assert parsed_items[0]["status"] == TENTATIVE


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "",
        "address": "Neal H. Holmes Board Room, 345 Sixth Avenue, Fifth Floor, Pittsburgh, PA 15222"
    }


def test_source():
    assert parsed_items[0][
        "source"
    ] == "https://www.portauthority.org/paac/CompanyInfoProjects/BoardofDirectors/MeetingAgendasResolutions.aspx"  # noqa


def test_links():
    assert parsed_items[0]["links"] == []


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
