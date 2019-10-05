from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pa_liquorboard import PaLiquorboardSpider

test_response = file_response(
    join(dirname(__file__), "files", "pa_liquorboard.html"),
    url="https://www.lcb.pa.gov/About-Us/Board/Pages/Public-Meetings.aspx",
)
spider = PaLiquorboardSpider()

freezer = freeze_time("2019-02-08")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_start():
    assert parsed_items[0]["start"] > datetime(2000, 1, 1, 0, 0)
