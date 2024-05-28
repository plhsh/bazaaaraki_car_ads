from typing import List

import requests

from api.district import District


class BazarakiApi:
    def __init__(self, url="https://www.bazaraki.com",
                 url_section="car-motorbikes-boats-and-parts/cars-trucks-and-vans/year_min---70"):
        self.url = url
        self.url_section = url_section

    def get_cars(self, districts: List[District], price_min: int, price_max: int, page: int, q: str) -> str:
        _url = f"{self.url}/{self.url_section}"
        _districts = list(map(lambda district: district.value, districts))
        # Создание базового словаря параметров
        _params = {
            # "cities": _districts,
            "price_min": price_min,
            "price_max": price_max,
            # "q": q
        }
        # Добавление ключа 'page', если page больше 1
        if page > 1:
            _params["page"] = page

        return requests.post(url=_url, params=_params).text


# r = BazarakiApi()
# page = r.get_cars([District.PAPHOS], 6000, 30000, 1, "")
# print(type(page))
# print(page)
