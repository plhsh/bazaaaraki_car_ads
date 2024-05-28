from typing import List
from api.bazaraki_api import BazarakiApi
from api.district import District
from scrapper.ad import Ad
from scrapper.scrapper import Scrapper
from db.db_config import db_connection
from logs.log_config import setup_logging
import logging

setup_logging()


class AdsManager:
    def __init__(self, api: BazarakiApi, scrapper: Scrapper): #, ads_db: AdsDatabase, subs_db: SubscriptionsDatabase):
        self._api = api
        self._scrapper = scrapper

    def _get_cars_ads(self) -> List[Ad]:
        logging.info("Scrapping and parsing data ...")
        result = []
        district = District.PAPHOS
        min_price = 6000
        max_price = 30000
        query = ""
        page = 1
        next_page_exists = True
        while next_page_exists:
            cars_html = self._api.get_cars([district], min_price, max_price, page, query)
            scr_data, next_page_exists = self._scrapper.scrap(cars_html)
            result.extend(scr_data)
            page += 1
        db_connection.insert_or_update_ads_to_db(result)
        return result


def main():
    m = AdsManager(BazarakiApi(), Scrapper())
    res = m._get_cars_ads()
    print(f"Ads found: {len(res)}\n\n\n")
    for car in res:
        print(car)
