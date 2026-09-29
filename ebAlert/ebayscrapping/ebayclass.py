from typing import Generator

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from ebAlert import create_logger
from ebAlert.core.config import settings

log = create_logger(__name__)


class EbayItem:
    """Class ebay item"""
    def __init__(self, contents: Tag):
        self.contents = contents
        self._city = None
        self._distance = None
        self._extract_city_distance()

    @property
    def link(self) -> str:
        href = self.contents.get('data-href') or (self.contents.a.get('href') if self.contents.a else None)
        if href:
            return settings.URL_BASE + href
        else:
            return "No url found."

    @property
    def title(self) -> str:
        return self._text(self.contents.h3) or "No Title"

    @property
    def price(self) -> str:
        found = self.contents.find("p", class_=lambda c: c and "font-strong" in c and "text-secondary" in c
                                   and "line-through" not in c)
        return self._text(found) or "No Price"

    @property
    def description(self) -> str:
        found = self.contents.find("p", class_=lambda c: c and "text-onSurfaceSubdued" in c)
        description = self._text(found)
        if description:
            return description.replace("\n", " ")
        else:
            return "No Description"

    @property
    def id(self) -> int:
        return int(self.contents.get('data-adid') or 0)

    @property
    def city(self):
        return self._city or "No city"

    @property
    def distance(self):
        return self._distance

    def __repr__(self):
        return '{}; {}; {}'.format(self.title, self.city, self.distance)

    @staticmethod
    def _text(tag):
        if tag:
            return tag.get_text(" ", strip=True)

    def _extract_city_distance(self):
        # the location is the first span of the header row above the title
        span = self.contents.find("span")
        location = self._text(span)
        if location:
            self._city = location


class EbayItemFactory:
    def __init__(self, link):
        self.link = link
        web_pages = self.get_webpage()
        if web_pages:
            articles = self.extract_item_from_page(web_pages)
            self.item_list = [EbayItem(article) for article in articles]
        else:
            self.item_list = []

    def get_webpage(self) -> str:
        custom_header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
        }
        response = requests.get(self.link, headers=custom_header)
        if response and response.status_code == 200:
            # the server sends no charset, requests would fall back to ISO-8859-1
            response.encoding = "utf-8"
            return response.text
        else:
            print(f"<< webpage fetching error for url: {self.link}")

    @staticmethod
    def extract_item_from_page(text: str) -> Generator:
        cleaned_response = text.replace("&#8203", "")
        soup = BeautifulSoup(cleaned_response, "html.parser")
        result = soup.find(attrs={"id": "srchrslt-adtable"})
        if result:
            for item in result.find_all("article", attrs={"data-adid": True}):
                yield item
