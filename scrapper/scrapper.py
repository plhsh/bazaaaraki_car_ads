import re
from typing import List, Tuple, Any

from bs4 import BeautifulSoup
from .ad import Ad


class Scrapper:

    def scrap(self, html: str) -> tuple[list[Ad], bool]:
        _soup = BeautifulSoup(html, 'html.parser')
        _announcements = _soup.body.find_all('div', attrs={'class': 'advert js-item-listing'})
        next_page_exists = True if _soup.find("a", class_="number-list-next js-page-filter number-list-line") else False
        return list(map(lambda announcement: self._as_ad(announcement), _announcements)), next_page_exists

    def _as_ad(self, announcement) -> Ad:
        _url = self._extract_url(announcement)
        return Ad(
            title=self._extract_title(announcement)[:-4],
            year=int(self._extract_title(announcement)[-4:]),
            price=self._extract_price(announcement),
            milage=int(self._extract_description(announcement)[0].rstrip(" km")),
            transmission=self._extract_description(announcement)[1],
            engine_type=self._extract_description(announcement)[2],
            id=int(re.search(r"/adv/(\d+)_", _url).group(1)),
            location_1=self._extract_location(announcement)[0],
            location_2=self._extract_location(announcement)[-1],
            date=self._extract_date(announcement),
            url=f"www.bazaraki.com{_url}"
        )

    @staticmethod
    def _extract_url(announcement) -> str:
        return announcement.find("a", attrs={"class": "mask"}).get("href")

    @staticmethod
    def _extract_price(announcement) -> int:
        res = announcement.find("a", class_="advert__content-price _not-title").find("span").text.strip()
        res = res.split("€")[1].strip()
        res = res.replace(".", "")
        return int(res)

    @staticmethod
    def _extract_title(announcement) -> str:
        return announcement.find("a", class_="advert__content-title").text.strip()

    @staticmethod
    def _extract_description(announcement) -> list[int | Any] | str:
        try:
            res = []
            features = announcement.find_all("div", class_="advert__content-feature")
            for feature in features:
                res.append(feature.div.text.strip())
            if len(res) == 0:
                return ["0", "", ""]
            if not str(res[0]).rstrip(" km").isdigit():
                # res[0] = "0"
                res = ["0", "", ""]
            return res
        except AttributeError:
            return ["0", "", ""]

    @staticmethod
    def _extract_date(announcement) -> str:
        return announcement.find("div", class_="advert__content-date").text.strip()

    @staticmethod
    def _extract_location(announcement) -> str:
        return announcement.find("div", class_="advert__content-place").text.strip().split(", ", 1)
