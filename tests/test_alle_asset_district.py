from os.path import dirname, join

from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.alle_asset_district import AlleAssetDistrictSpider

test_response = file_response(
    join(dirname(__file__), "files", "alle_asset_district.html"),
    url="https://radworkshere.org/pages/whats-happening?cal=board-meetings",
)
spider = AlleAssetDistrictSpider()

freezer = freeze_time("2019-02-08")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()
