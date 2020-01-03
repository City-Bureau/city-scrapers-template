from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import CANCELLED, COMMISSION, PASSED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pitt_art_commission import PittArtCommissionSpider

test_response = file_response(
    join(dirname(__file__), "files", "pitt_art_commission.html"),
    url="https://pittsburghpa.gov/dcp/art-commission-schedule",
)
spider = PittArtCommissionSpider()

freezer = freeze_time("2019-12-01")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]
freezer.stop()


def test_number_of_meetings():
    assert len(parsed_items) == 34


def test_title():
    expected_title = "Art Commission of Pittsburgh Monthly Meeting"
    for item in parsed_items:
        assert item["title"] == expected_title


def test_start():
    expected_start_dates_2019 = {
        datetime(year=2019, month=1, day=23, hour=14),
        datetime(year=2019, month=2, day=27, hour=14),
        datetime(year=2019, month=3, day=27, hour=14),
        datetime(year=2019, month=4, day=24, hour=14),
        datetime(year=2019, month=5, day=22, hour=14),
        datetime(year=2019, month=6, day=26, hour=14),
        datetime(year=2019, month=7, day=24, hour=14),
        datetime(year=2019, month=8, day=28, hour=14),
        datetime(year=2019, month=9, day=25, hour=14),
        datetime(year=2019, month=10, day=23, hour=14),
        datetime(year=2019, month=11, day=20, hour=14)
    }

    actual_start_dates_2019 = {
        meeting["start"]
        for meeting in parsed_items
        if meeting["start"].year == 2019
    }

    assert expected_start_dates_2019 == actual_start_dates_2019


def test_end():
    for item in parsed_items:
        assert item["end"] is None


def test_time_notes():
    for item in parsed_items:
        assert item["time_notes"] == ""


def test_location():
    for item in parsed_items:
        assert item["location"] == {
            "location": "1st Floor Hearing Room",
            "address": "200 Ross Street, Pittsburgh, PA, 15219",
            "name": "",
        }


def test_links():
    def link_name(file):
        return "http://apps.pittsburghpa.gov/redtail/images/{}".format(file)

    link_test_cases = [{
        "month": 1,
        "year": 2019,
        "links": [{
            "title": "January_2019_AC_Minutes.pdf",
            "href": link_name("5026_January_2019_AC_Minutes.pdf")
        }]
    }, {
        "month": 2,
        "year": 2019,
        "links": [{
            "title": "2-27-19_AC_Agenda.pdf",
            "href": link_name("4891_2-27-19_AC_Agenda.pdf")
        }, {
            "title": "February_2019_AC_Minutes.pdf",
            "href": link_name("5413_February_2019_AC_Minutes.pdf")
        }]
    }, {
        "month": 1,
        "year": 2018,
        "links": [{
            "title": "1_24_18_ACAgenda.pdf",
            "href": link_name("1440_1_24_18_ACAgenda.pdf")
        }, {
            "title": "1_24_18_AC_Minutes_with_SF_Interim_Report.pdf",
            "href": link_name("1877_1_24_18_AC_Minutes_with_SF_Interim_Report.pdf")
        }]
    }, {
        "month": 10,
        "year": 2019,
        "links": []
    }]

    for test_case in link_test_cases:
        matching_items = [
            item for item in parsed_items
            if item["start"].month == test_case["month"] and item["start"].year == test_case["year"]
        ]
        assert len(matching_items) == 1
        matching_item = matching_items[0]
        expected_links = test_case["links"]
        actual_links = matching_item["links"]
        assert len(actual_links) == len(expected_links)

        for expected in expected_links:
            found = False
            for actual in actual_links:
                if expected == actual:
                    found = True
                    break
            assert found


def test_classification():
    for item in parsed_items:
        assert item["classification"] == COMMISSION


def test_status():
    found_cancelled = False
    for item in parsed_items:
        if item["start"].month == 10 and item["start"].year == 2019:
            found_cancelled = True
            assert item["status"] == CANCELLED
        else:
            assert item["status"] == PASSED
    assert found_cancelled


def test_all_day():
    for item in parsed_items:
        assert item["all_day"] is False


# The 'id' or 'source' fields aren't customized currently, so these are commented out.
# def test_id():
#     assert parsed_items[0]["id"] == "EXPECTED ID"

# def test_source():
#     assert parsed_items[0]["source"] == "EXPECTED URL"
