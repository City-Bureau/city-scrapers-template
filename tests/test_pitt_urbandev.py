from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pitt_urbandev import PittUrbandevSpider

test_response = file_response(
    join(dirname(__file__), "files", "pitt_urbandev.html"),
    url="https://www.ura.org/pages/board-meeting-notices-agendas-and-minutes",
)
spider = PittUrbandevSpider()

freezer = freeze_time("2020-01-25")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]


def test_description():
    assert parsed_items[0]["description"] == "Rescheduled board meeting"


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 1, 16, 14, 0)


def test_id():
    assert parsed_items[0]["id"] == "pitt_urbandev/202001161400/x/ura_board_meeting"


def test_status():
    assert parsed_items[0]["status"] == "cancelled"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Lower Level Conference Room",
        "address": "412 Boulevard of the Allies, Pittsburgh, PA 15219"
    }


def test_source():
    ref = "https:"
    ref = ref + "//www.ura.org/pages/board-meeting"
    ref = ref + "-notices-agendas-and-minutes"
    assert parsed_items[0]["source"] == ref


def test_links():
    ref = "https://www.ura.org/media"
    ref = ref + "/W1siZiIsIjIwMjAvMDEvMTQvNnhia3RoM"
    ref = ref + "zdrN19KQU5VQVJZXzIwMjBfVVJBX1JFU0"
    ref = ref + "NIRURVTEVEX1JFR1VMQVJfQk9BUkRfTUVF"
    ref = ref + "VElOR19OT1RJQ0UucGRmIl1d/JANUARY%202020"
    ref = ref + "-%20URA%20RESCHEDULED%20REGULAR%20BOARD%20ME"
    ref = ref + "ETING%20NOTICE.pdf"
    assert parsed_items[0]["links"][0] == {
        "href": ref,
        "title": "Notice of Rescheduled Board Meeting - January 16, 2020"
    }


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False


freezer.stop()
