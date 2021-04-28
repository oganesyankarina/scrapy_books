import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    main_url = 'https://book24.ru'

    def __init__(self, search):
        super(Book24Spider, self).__init__()
        self.start_urls = [f'https://book24.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[contains(@class, "product-card__name smartLink")]/@href').getall()

        for link in links:
            yield response.follow(self.main_url + link, callback=self.process_item)

        next_page = response.xpath('//li[contains(@class, "pagination__button-item")]//a[contains(@class, "next")]/@href').get()
        if next_page:
            yield response.follow(self.main_url + next_page, callback=self.parse)

    def process_item(self, response: HtmlResponse):
        item = BookparserItem()
        item["url"] = response.url
        item["name"] = response.xpath('//h1//text()').get()
        item["author"] = response.xpath('//a[contains(@itemprop, "author")]//text()').getall()
        item["basic_price"] = response.xpath('//div[contains(@class,"item-actions__price-old")]//text()').get()
        item["discount_price"] = response.xpath('//b[contains(@itemprop,"price")]//text()').get()
        item["rating"] = response.xpath('//div[contains(@class,"rating__rate-value _bold")]//text()').get()
        yield item
