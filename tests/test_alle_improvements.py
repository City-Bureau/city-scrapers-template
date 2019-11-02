from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.alle_improvements import AlleImprovementsSpider

test_response = file_response(
    join(dirname(__file__), "files", "alle_improvements.html"),
    url=(
        "https://www.county.allegheny.pa.us/economic-development/"
        "authorities/meetings-reports/aim/meetings.aspx"
    )
)
spider = AlleImprovementsSpider()

freezer = freeze_time("2019-06-06")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    expected = (
        "Authority For Improvements In Municipalities Board Of "
        "Directors Regular And Public Hearing"
    )

    assert parsed_items[0]["title"] == expected


# def test_description():
#   assert parsed_items[0]["description"] == "EXPECTED DESCRIPTION"


def test_num_items():
    assert len(parsed_items) == 12


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 1, 22, 10, 30)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


# def test_id():
#   assert parsed_items[0]["id"] == "EXPECTED ID"

# def test_status():
#     assert parsed_items[0]["status"] == "EXPECTED STATUS"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "One Chatham Center",
        "address": "Suite 900\n112 Washington Place\nPittsburgh, PA 15219"
    }


def test_source():
    expected = (
        "https://www.county.allegheny.pa.us/economic-development/"
        "authorities/meetings-reports/aim/meetings.aspx"
    )

    assert parsed_items[0]["source"] == expected


def test_links():
    assert len(parsed_items[0]["links"]) == 0

    assert parsed_items[1]["links"] == [
        {
            "href": (
                "https://www.county.allegheny.pa.us/economic-development/"
                "authorities/meetings-reports/aim/2019/02-26-19-agenda.aspx"
            ),
            "title": "Agenda 02-26-19"
        },
        {
            "href": (
                "https://www.county.allegheny.pa.us/economic-development/"
                "authorities/meetings-reports/aim/2019/02-26-19-minutes.aspx"
            ),
            "title": "Minutes 02-26-19"
        },
    ]


def test_classification():
    assert parsed_items[0]["classification"] == NOT_CLASSIFIED


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
