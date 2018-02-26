import scrapy

from Gmetacrawler.items import GmetacrawlerItem

class GMetaSpider(scrapy.Spider):
    name = "Gmeta"
    allow_domain = ["metacritic.com"]
    # 크롤링의 시작 URL
    start_urls = [
        "http://www.metacritic.com/browse/games/release-date/coming-soon/ps4/date"
    ]

    # link 리스트를 가져옴
    def parse(self, response):
        games = response.xpath('//*[@id="main"]/div[2]/div[2]/div[3]/div/ol/li')
        for game in games:
            link = 'http://www.metacritic.com'+game.xpath('./div/div[@class="basic_stat product_title"]/a/@href').extract()[0]
            print(link)
            yield scrapy.Request(link, callback=self.parse_page_contents)

    # 각페이지의 link로 접속하여 데이터를 가져옴
    def parse_page_contents(self, response):
        item = GmetacrawlerItem()
        item["title"] = response.xpath('//*[@id="main"]/div/div[1]/div[2]/a/span/h1/text()')[0].extract()
        # item["img"] = response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div/img')[0].extract()
        item["date"] = response.xpath('//*[@id="main"]/div/div[1]/div[3]/ul/li[2]/span[2]/text()').extract()
        yield item
