from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.alle_health import AlleHealthSpider

test_response = file_response(
    join(dirname(__file__), "files", "alle_health.html"),
    url="https://www.alleghenycounty.us/Health-Department/Resources/" +
    "About/Board-of-Health/Public-Meeting-Schedule.aspx",
)
spider = AlleHealthSpider()

freezer = freeze_time("2019-04-12")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()

# def test_tests():
#     print("Please write some tests for this spider or at least disable this one.")
#     assert False
"""
Uncomment below
"""


def test_title():
    #     print ("L35: title is |" + str(parsed_items[0]["title"]) + "|")
    assert parsed_items[0]["title"] == "Allegheny County Board of Health May 1, 2019 12:30 pm"


# def test_description():
#     assert parsed_items[0]["description"] == "EXPECTED DESCRIPTION"


def test_start():
    #    print("L44: start is |" + str(parsed_items[0]["start"]) + "|")
    assert parsed_items[0]["start"] == datetime(2019, 5, 1, 12, 30)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)

# def test_time_notes():
#     assert parsed_items[0]["time_notes"] == "EXPECTED TIME NOTES"

# def test_id():
#     assert parsed_items[0]["id"] == "EXPECTED ID"

# def test_status():
#     assert parsed_items[0]["status"] == "EXPECTED STATUS"

# def test_location():
#     assert parsed_items[0]["location"] == {
#         "name": "EXPECTED NAME",
#         "address": "EXPECTED ADDRESS"
#     }

# def test_source():
#     assert parsed_items[0]["source"] == "EXPECTED URL"

# def test_links():
#     assert parsed_items[0]["links"] == [{
#       "href": "EXPECTED HREF",
#       "title": "EXPECTED TITLE"
#     }]

# def test_classification():
#     assert parsed_items[0]["classification"] == NOT_CLASSIFIED

# @pytest.mark.parametrize("item", parsed_items)
# def test_all_day(item):
#     assert item["all_day"] is False
