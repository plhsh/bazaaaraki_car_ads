from typing import List

from api.bazaraki_api import BazarakiApi
from api.district import District
# from db.ads import AdsDatabase
# from db.subscriptions import SubscriptionsDatabase
from scrapper.ad import Ad
from scrapper.scrapper import Scrapper
from db.db_config import db_connection


class AdsManager:
    def __init__(self, api: BazarakiApi, scrapper: Scrapper): #, ads_db: AdsDatabase, subs_db: SubscriptionsDatabase):
        self._api = api
        # self._ads_db = ads_db
        # self._subs_db = subs_db
        self._scrapper = scrapper

    # def request_updates(self) -> List[Ad]:
    #     remote = self._get_cars_ads()
    #     # local = self._ads_db.all()
    #     updates = list(filter(lambda ad: ad not in local, remote))
    #     self._ads_db.add_all(updates)
    #     return updates

    def _get_cars_ads(self) -> List[Ad]:
        result = []
        district = District.PAPHOS
        min_price = 5000
        max_price = 20000
        query = ""
        page = 1
        next_page_exists = True
        while next_page_exists:
            cars_html = self._api.get_cars([district], min_price, max_price, page, query)
            scr_data, next_page_exists = self._scrapper.scrap(cars_html)
            result.extend(scr_data)
            page += 1
        db_connection.insert_ads_to_db(result)
        return result


m = AdsManager(BazarakiApi(), Scrapper())
res = m._get_cars_ads()
print(f"Ads found: {len(res)}\n\n\n")
for car in res:
    print(car)