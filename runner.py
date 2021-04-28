from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from bookparser import settings
from bookparser.spiders.labirint import LabirintSpider
from bookparser.spiders.book24 import Book24Spider
from urllib import parse

def make_url(search):
    search = parse.quote_plus(search.encode("UTF-8"))
    url = f"https://www.labirint.ru/search/{search}/?stype=0"
    url = url.replace("+", "%20")
    print(url)
    return url


if __name__ == "__main__":
    search = input("Что ищем?: ")
    search = parse.quote_plus(search.encode("UTF-8"))
    search = search.replace("+", "%20")

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintSpider, search=search)
    process.crawl(Book24Spider, search=search)

    process.start()
