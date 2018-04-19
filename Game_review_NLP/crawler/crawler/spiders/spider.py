import scrapy
from crawler.items import CrawlerItem

class MakeError(Exception):

    def __str__(self):
        return "self check"

class C_Spider(scrapy.Spider):
    name = "critic"
    allow_domain = ["metacritic.com"]

    def start_requests(self):
        for i in range(0, 15+1):
            url = "http://www.metacritic.com/browse/games/release-date/available/ps4/date" + "?page={}".format(i)
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        games = response.xpath('//*[@id="main"]/div[1]/div[2]/div[3]/div/ol/li')

        for game in games:
            link = 'http://www.metacritic.com'+game.xpath('./div/div[@class="basic_stat product_title"]/a/@href').extract()[0] + '/critic-reviews'

            yield scrapy.Request(link, callback=self.parse_page_contents)

    def parse_page_contents(self, response):
        item = CrawlerItem()
        title = response.xpath('//*[@id="main"]/div[1]/div[2]/a/h1/text()')[0].extract()
        reviews = response.xpath('//*[@id="main"]/div[5]/div/ol/li')

        for review in reviews:

            item["title"] = title
            try:
                item["id"] = review.xpath('./div/div/div/div/div/div[1]/div[1]/div[1]/div[1]/a/text()')[0].extract()
                if not item["id"]:
                    raise MakeError()
            except:
                item["id"] = review.xpath('./div/div/div/div/div/div[1]/div[1]/div[1]/div[1]/text()')[0].extract()

            item["score"] = review.xpath('./div/div/div/div/ div/div[1]/div[1]/div[2]/div/text()')[0].extract()
            item["review"] = review.xpath('./div/div/div/div/div/div[1]/div[2]/text()')[0].extract()

            yield item

class Spider(scrapy.Spider):
    name = "user"
    allow_domain = ["metacritic.com"]

    def start_requests(self):
        for i in range(0, 15+1):
            url = "http://www.metacritic.com/browse/games/release-date/available/ps4/date" + "?page={}".format(i)
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        games = response.xpath('//*[@id="main"]/div[1]/div[2]/div[3]/div/ol/li')

        for game in games:
            link = 'http://www.metacritic.com'+game.xpath('./div/div[@class="basic_stat product_title"]/a/@href').extract()[0] + '/user-reviews?sort-by=most-helpful&num_items=100'

            yield scrapy.Request(link, callback=self.parse_page_contents)

    def parse_page_contents(self, response):
        item = CrawlerItem()
        title = response.xpath('//*[@id="main"]/div[1]/div[2]/a/h1/text()')[0].extract()
        reviews = response.xpath('//*[@id="main"]/div[5]/div[2]/div/ol/li')

        for review in reviews:

            item["title"] = title

            try:
                item["id"] = review.xpath('./div/div/div/div/div/div[1]/div[1]/div[1]/div[1]/a/text()')[0].extract()
                if not item["id"]:
                    raise MakeError()
            except:
                item["id"] = review.xpath('./div/div/div/div/div/div[1]/div[1]/div[1]/div[1]/text()')[0].extract()

            item["score"] = review.xpath('./div/div/div/div/ div/div[1]/div[1]/div[2]/div/text()')[0].extract()

            try:
                tmp = review.xpath('./div/div/div/div/div/div[1]/div[2]/span/span[1]/text()').extract()
                item["review"] = ''.join(tmp) #for muliple lines

                if not tmp: #for spoliers lines
                    tmp = review.xpath('./div/div/div/div/div/div[1]/div[2]/span/span[2]/text()').extract()
                    item["review"] = ''.join(tmp)

                    if not tmp:
                        raise MakeError()
            except:
                tmp = review.xpath('./div/div/div/div/div/div[1]/div[2]/span/text()').extract()
                item["review"] = ''.join(tmp)

            yield item
