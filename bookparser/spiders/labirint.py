import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    main_url = 'https://www.labirint.ru'

    def __init__(self, search):
        super(LabirintSpider, self).__init__()
        self.start_urls = [f'https://www.labirint.ru/search/{search}/?stype=0']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[contains(@class, "product-title-link")]/@href').getall()

        for link in links:
            yield response.follow(self.main_url + link, callback=self.process_item)

        next_page = response.xpath('//div[contains(@class, "pagination-next")]/a/@href').get()
        if next_page:
            url = self.start_urls[0] + next_page[8:]
            yield response.follow(url, callback=self.parse)

    def process_item(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').get()
        item = BookparserItem()
        item["url"] = response.url
        item["name"] = name
        item["author"] = response.xpath('//a[contains(@data-event-label,"author")]//text()').getall()
        item["basic_price"] = response.xpath('//span[contains(@class,"buying-priceold-val-number")]//text()').get()
        item["discount_price"] = response.xpath('//span[contains(@class,"buying-pricenew-val-number")]//text()').get()
        item["rating"] = response.xpath('//div[contains(@id,"rate")]//text()').get()
        yield item
