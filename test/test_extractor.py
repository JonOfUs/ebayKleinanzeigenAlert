from bs4 import BeautifulSoup

from ebAlert.ebayscrapping.ebayclass import EbayItemFactory, EbayItem


def test_item_extractor():
    with open("./test.html", "r", encoding="UTF-8") as f:
        all_items = [item for item in EbayItemFactory.extract_item_from_page(f.read())]
        assert len(all_items) == 27
        assert all_items[0].attrs["data-adid"] == "3500553575"


def test_ebay_item():
    with open("./test_article.html", "r", encoding="UTF-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        article = soup.find("article")
        item = EbayItem(article)
        print(item)
        assert item.link == 'https://www.kleinanzeigen.de/s-anzeige/niro-citybike-fahrrad-28-zoll-shimano-7-gang-neu/3500553575-217-4880'
        assert item.id == 3500553575
        assert item.title == 'NIRO Citybike Fahrrad, 28 Zoll, Shimano 7 Gang, Neu'
        assert item.price == '245 €'
        assert item.city == '36137 Großenlüder'
        assert item.distance is None
        assert item.description == "Neues Citybike mit allen Komponenten zur..."


if __name__ == "__main__":
    pass
